// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

interface ITokenomicsV2Provider {
    function distributeTrustedProviderReward(address recipient, uint256 amount, string calldata reason) external;
}

/**
 * @title EcosystemInteractionModule (EIM)
 * @notice Manages trusted external service providers and query-based rewards
 * @dev Handles micro-rewards for verified queries and bonuses for high-value integrations
 */
contract EcosystemInteractionModule is Ownable, ReentrancyGuard {
    using ECDSA for bytes32;
    
    ITokenomicsV2Provider public tokenomics;
    
    // Trusted provider structure
    struct TrustedProvider {
        bool isActive;
        uint256 registrationTime;
        uint256 totalQueriesProcessed;
        uint256 totalRewardsEarned;
        string serviceType;         // e.g., "Ocean Protocol", "External Oracle"
        uint256 reputationScore;    // 0-100
    }
    
    // Query verification structure
    struct VerifiedQuery {
        address provider;
        bytes32 queryHash;
        uint256 timestamp;
        bool rewarded;
        QueryType queryType;
    }
    
    enum QueryType {
        Standard,
        HighValue,
        Premium
    }
    
    // Storage
    mapping(address => TrustedProvider) public trustedProviders;
    mapping(bytes32 => VerifiedQuery) public verifiedQueries;
    mapping(address => uint256) public providerNonces; // Nonce to prevent replay attacks
    address[] public providerList;
    
    // Reward parameters
    uint256 public microRewardPerQuery = 5 * 10**18;        // Standard query reward
    uint256 public highValueQueryBonus = 50 * 10**18;       // High-value query bonus
    uint256 public premiumQueryBonus = 200 * 10**18;        // Premium query bonus
    uint256 public integrationBonus = 1000 * 10**18;        // Bonus for new integrations
    
    // Reputation thresholds
    uint256 public minReputationForHighValue = 50;
    uint256 public minReputationForPremium = 80;
    
    // Events
    event ProviderRegistered(
        address indexed provider,
        string serviceType,
        uint256 timestamp
    );
    
    event ProviderStatusChanged(
        address indexed provider,
        bool isActive
    );
    
    event QueryVerified(
        bytes32 indexed queryHash,
        address indexed provider,
        QueryType queryType,
        uint256 timestamp
    );
    
    event RewardDistributed(
        address indexed provider,
        uint256 amount,
        QueryType queryType,
        string reason
    );
    
    event IntegrationBonusAwarded(
        address indexed provider,
        uint256 amount,
        string reason
    );
    
    event ReputationUpdated(
        address indexed provider,
        uint256 oldScore,
        uint256 newScore
    );
    
    /**
     * @notice Constructor
     * @param _tokenomics Address of TokenomicsV2 contract
     */
    constructor(address _tokenomics) {
        require(_tokenomics != address(0), "Invalid tokenomics");
        tokenomics = ITokenomicsV2Provider(_tokenomics);
    }
    
    /**
     * @notice Register a new trusted provider
     * @param provider Address of the provider
     * @param serviceType Type of service offered
     */
    function registerProvider(
        address provider,
        string calldata serviceType
    ) external onlyOwner {
        require(provider != address(0), "Invalid provider");
        require(!trustedProviders[provider].isActive, "Already registered");
        require(bytes(serviceType).length > 0, "Service type required");
        
        trustedProviders[provider] = TrustedProvider({
            isActive: true,
            registrationTime: block.timestamp,
            totalQueriesProcessed: 0,
            totalRewardsEarned: 0,
            serviceType: serviceType,
            reputationScore: 50  // Start with neutral reputation
        });
        
        providerList.push(provider);
        
        emit ProviderRegistered(provider, serviceType, block.timestamp);
    }
    
    /**
     * @notice Update provider active status
     * @param provider Address of the provider
     * @param isActive New active status
     */
    function setProviderStatus(address provider, bool isActive) external onlyOwner {
        require(trustedProviders[provider].registrationTime > 0, "Provider not registered");
        
        trustedProviders[provider].isActive = isActive;
        emit ProviderStatusChanged(provider, isActive);
    }
    
    /**
     * @notice Verify and reward a query
     * @param provider Address of the provider
     * @param queryData Query data to hash
     * @param queryType Type of query
     * @param signature Signature from provider
     */
    function verifyAndRewardQuery(
        address provider,
        bytes calldata queryData,
        QueryType queryType,
        bytes calldata signature
    ) external nonReentrant {
        require(trustedProviders[provider].isActive, "Provider not active");
        
        // Increment nonce to prevent replay attacks
        uint256 nonce = providerNonces[provider]++;
        
        // Create query hash with nonce
        bytes32 queryHash = keccak256(abi.encodePacked(queryData, provider, nonce));
        
        // Verify signature
        bytes32 messageHash = queryHash.toEthSignedMessageHash();
        address signer = messageHash.recover(signature);
        require(signer == provider, "Invalid signature");
        
        // Check not already rewarded
        require(!verifiedQueries[queryHash].rewarded, "Already rewarded");
        
        // Check reputation requirements for query type
        if (queryType == QueryType.HighValue) {
            require(
                trustedProviders[provider].reputationScore >= minReputationForHighValue,
                "Insufficient reputation for high-value"
            );
        } else if (queryType == QueryType.Premium) {
            require(
                trustedProviders[provider].reputationScore >= minReputationForPremium,
                "Insufficient reputation for premium"
            );
        }
        
        // Record query
        verifiedQueries[queryHash] = VerifiedQuery({
            provider: provider,
            queryHash: queryHash,
            timestamp: block.timestamp,
            rewarded: true,
            queryType: queryType
        });
        
        // Calculate reward
        uint256 rewardAmount = calculateQueryReward(queryType);
        
        // Update provider stats
        trustedProviders[provider].totalQueriesProcessed++;
        trustedProviders[provider].totalRewardsEarned += rewardAmount;
        
        // Distribute reward
        string memory reason = string(abi.encodePacked(
            "Query verified: ",
            queryTypeToString(queryType)
        ));
        tokenomics.distributeTrustedProviderReward(provider, rewardAmount, reason);
        
        emit QueryVerified(queryHash, provider, queryType, block.timestamp);
        emit RewardDistributed(provider, rewardAmount, queryType, reason);
    }
    
    /**
     * @notice Award integration bonus to provider
     * @param provider Address of the provider
     * @param reason Reason for the bonus
     */
    function awardIntegrationBonus(
        address provider,
        string calldata reason
    ) external onlyOwner nonReentrant {
        require(trustedProviders[provider].isActive, "Provider not active");
        
        trustedProviders[provider].totalRewardsEarned += integrationBonus;
        
        tokenomics.distributeTrustedProviderReward(provider, integrationBonus, reason);
        
        emit IntegrationBonusAwarded(provider, integrationBonus, reason);
    }
    
    /**
     * @notice Update provider reputation score
     * @param provider Address of the provider
     * @param newScore New reputation score (0-100)
     */
    function updateReputation(address provider, uint256 newScore) external onlyOwner {
        require(trustedProviders[provider].registrationTime > 0, "Provider not registered");
        require(newScore <= 100, "Invalid score");
        
        uint256 oldScore = trustedProviders[provider].reputationScore;
        trustedProviders[provider].reputationScore = newScore;
        
        emit ReputationUpdated(provider, oldScore, newScore);
    }
    
    /**
     * @notice Calculate reward amount based on query type
     * @param queryType Type of query
     * @return Reward amount
     */
    function calculateQueryReward(QueryType queryType) public view returns (uint256) {
        if (queryType == QueryType.Standard) {
            return microRewardPerQuery;
        } else if (queryType == QueryType.HighValue) {
            return microRewardPerQuery + highValueQueryBonus;
        } else if (queryType == QueryType.Premium) {
            return microRewardPerQuery + premiumQueryBonus;
        }
        return 0;
    }
    
    /**
     * @notice Set reward parameters
     */
    function setRewardParameters(
        uint256 _microReward,
        uint256 _highValueBonus,
        uint256 _premiumBonus,
        uint256 _integrationBonus
    ) external onlyOwner {
        microRewardPerQuery = _microReward;
        highValueQueryBonus = _highValueBonus;
        premiumQueryBonus = _premiumBonus;
        integrationBonus = _integrationBonus;
    }
    
    /**
     * @notice Set reputation thresholds
     */
    function setReputationThresholds(
        uint256 _minForHighValue,
        uint256 _minForPremium
    ) external onlyOwner {
        require(_minForHighValue <= 100 && _minForPremium <= 100, "Invalid thresholds");
        minReputationForHighValue = _minForHighValue;
        minReputationForPremium = _minForPremium;
    }
    
    /**
     * @notice Get provider details
     */
    function getProvider(address provider) external view returns (
        bool isActive,
        uint256 registrationTime,
        uint256 totalQueriesProcessed,
        uint256 totalRewardsEarned,
        string memory serviceType,
        uint256 reputationScore
    ) {
        TrustedProvider memory p = trustedProviders[provider];
        return (
            p.isActive,
            p.registrationTime,
            p.totalQueriesProcessed,
            p.totalRewardsEarned,
            p.serviceType,
            p.reputationScore
        );
    }
    
    /**
     * @notice Get total number of registered providers
     */
    function getProviderCount() external view returns (uint256) {
        return providerList.length;
    }
    
    /**
     * @notice Convert query type to string
     */
    function queryTypeToString(QueryType qType) internal pure returns (string memory) {
        if (qType == QueryType.Standard) return "Standard";
        if (qType == QueryType.HighValue) return "HighValue";
        if (qType == QueryType.Premium) return "Premium";
        return "Unknown";
    }
}
