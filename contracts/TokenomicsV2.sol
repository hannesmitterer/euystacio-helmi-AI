// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/**
 * @title TokenomicsV2
 * @notice Core tokenomics contract for Sensisara Evolved cycle
 * @dev Manages token distribution across ethical researchers, validators, providers, and operators
 */
contract TokenomicsV2 is ERC20, Ownable, ReentrancyGuard {
    
    // Token allocation percentages (basis points: 10000 = 100%)
    uint256 public constant ETHICAL_RESEARCHERS_ALLOCATION = 3500;  // 35%
    uint256 public constant DAO_VALIDATORS_ALLOCATION = 2000;       // 20%
    uint256 public constant TRUSTED_PROVIDERS_ALLOCATION = 1500;    // 15%
    uint256 public constant OPERATORS_ALLOCATION = 2000;            // 20%
    uint256 public constant COMMUNITY_RESERVE_ALLOCATION = 1000;    // 10%
    
    // Pool balances
    uint256 public ethicalResearchersPool;
    uint256 public daoValidatorsPool;
    uint256 public trustedProvidersPool;
    uint256 public operatorsPool;
    uint256 public communityReservePool;
    
    // Authorized contracts for reward distribution
    mapping(address => bool) public authorizedDistributors;
    
    // Inflation control
    uint256 public maxAnnualInflation = 500; // 5% max annual inflation in basis points
    uint256 public lastInflationTimestamp;
    uint256 public constant INFLATION_PERIOD = 365 days;
    
    // Events
    event RewardDistributed(
        address indexed recipient,
        uint256 amount,
        RewardCategory category,
        string reason
    );
    
    event PoolRefilled(RewardCategory category, uint256 amount);
    event DistributorAuthorized(address indexed distributor, bool authorized);
    event InflationMinted(uint256 amount, uint256 timestamp);
    
    enum RewardCategory {
        EthicalResearchers,
        DAOValidators,
        TrustedProviders,
        Operators,
        CommunityReserve
    }
    
    /**
     * @notice Constructor
     * @param initialSupply Initial token supply
     */
    constructor(uint256 initialSupply) ERC20("Sensisara Token", "SENS") {
        require(initialSupply > 0, "Initial supply must be positive");
        
        _mint(address(this), initialSupply);
        
        // Allocate to pools
        ethicalResearchersPool = (initialSupply * ETHICAL_RESEARCHERS_ALLOCATION) / 10000;
        daoValidatorsPool = (initialSupply * DAO_VALIDATORS_ALLOCATION) / 10000;
        trustedProvidersPool = (initialSupply * TRUSTED_PROVIDERS_ALLOCATION) / 10000;
        operatorsPool = (initialSupply * OPERATORS_ALLOCATION) / 10000;
        communityReservePool = (initialSupply * COMMUNITY_RESERVE_ALLOCATION) / 10000;
        
        lastInflationTimestamp = block.timestamp;
    }
    
    /**
     * @notice Distribute reward to ethical researcher
     * @param recipient Address of the researcher
     * @param amount Amount of tokens to distribute
     * @param reason Reason for the reward (e.g., CID of validated dataset)
     */
    function distributeEthicalResearcherReward(
        address recipient,
        uint256 amount,
        string calldata reason
    ) external nonReentrant {
        require(authorizedDistributors[msg.sender], "Not authorized");
        require(recipient != address(0), "Invalid recipient");
        require(amount > 0, "Amount must be positive");
        require(ethicalResearchersPool >= amount, "Insufficient pool balance");
        
        ethicalResearchersPool -= amount;
        _transfer(address(this), recipient, amount);
        
        emit RewardDistributed(recipient, amount, RewardCategory.EthicalResearchers, reason);
    }
    
    /**
     * @notice Distribute reward to DAO validator
     * @param recipient Address of the validator
     * @param amount Amount of tokens to distribute
     * @param reason Reason for the reward (e.g., quorum participation)
     */
    function distributeDAOValidatorReward(
        address recipient,
        uint256 amount,
        string calldata reason
    ) external nonReentrant {
        require(authorizedDistributors[msg.sender], "Not authorized");
        require(recipient != address(0), "Invalid recipient");
        require(amount > 0, "Amount must be positive");
        require(daoValidatorsPool >= amount, "Insufficient pool balance");
        
        daoValidatorsPool -= amount;
        _transfer(address(this), recipient, amount);
        
        emit RewardDistributed(recipient, amount, RewardCategory.DAOValidators, reason);
    }
    
    /**
     * @notice Distribute reward to trusted provider
     * @param recipient Address of the provider
     * @param amount Amount of tokens to distribute
     * @param reason Reason for the reward (e.g., verified query count)
     */
    function distributeTrustedProviderReward(
        address recipient,
        uint256 amount,
        string calldata reason
    ) external nonReentrant {
        require(authorizedDistributors[msg.sender], "Not authorized");
        require(recipient != address(0), "Invalid recipient");
        require(amount > 0, "Amount must be positive");
        require(trustedProvidersPool >= amount, "Insufficient pool balance");
        
        trustedProvidersPool -= amount;
        _transfer(address(this), recipient, amount);
        
        emit RewardDistributed(recipient, amount, RewardCategory.TrustedProviders, reason);
    }
    
    /**
     * @notice Distribute reward to operator
     * @param recipient Address of the operator
     * @param amount Amount of tokens to distribute
     * @param reason Reason for the reward (e.g., successful retraining execution)
     */
    function distributeOperatorReward(
        address recipient,
        uint256 amount,
        string calldata reason
    ) external nonReentrant {
        require(authorizedDistributors[msg.sender], "Not authorized");
        require(recipient != address(0), "Invalid recipient");
        require(amount > 0, "Amount must be positive");
        require(operatorsPool >= amount, "Insufficient pool balance");
        
        operatorsPool -= amount;
        _transfer(address(this), recipient, amount);
        
        emit RewardDistributed(recipient, amount, RewardCategory.Operators, reason);
    }
    
    /**
     * @notice Authorize or deauthorize a contract to distribute rewards
     * @param distributor Address of the distributor contract
     * @param authorized Whether to authorize or deauthorize
     */
    function setAuthorizedDistributor(address distributor, bool authorized) external onlyOwner {
        require(distributor != address(0), "Invalid distributor");
        authorizedDistributors[distributor] = authorized;
        emit DistributorAuthorized(distributor, authorized);
    }
    
    /**
     * @notice Mint inflation tokens to community reserve (controlled annual inflation)
     * @param amount Amount to mint
     */
    function mintInflation(uint256 amount) external onlyOwner {
        require(block.timestamp >= lastInflationTimestamp + INFLATION_PERIOD, "Inflation period not elapsed");
        
        uint256 maxInflationAmount = (totalSupply() * maxAnnualInflation) / 10000;
        require(amount <= maxInflationAmount, "Exceeds max annual inflation");
        
        _mint(address(this), amount);
        communityReservePool += amount;
        lastInflationTimestamp = block.timestamp;
        
        emit InflationMinted(amount, block.timestamp);
    }
    
    /**
     * @notice Get pool balance for a category
     * @param category Reward category
     * @return Pool balance
     */
    function getPoolBalance(RewardCategory category) external view returns (uint256) {
        if (category == RewardCategory.EthicalResearchers) return ethicalResearchersPool;
        if (category == RewardCategory.DAOValidators) return daoValidatorsPool;
        if (category == RewardCategory.TrustedProviders) return trustedProvidersPool;
        if (category == RewardCategory.Operators) return operatorsPool;
        if (category == RewardCategory.CommunityReserve) return communityReservePool;
        return 0;
    }
    
    /**
     * @notice Withdraw community reserve tokens
     * @param recipient Address to receive tokens
     * @param amount Amount to withdraw
     */
    function withdrawCommunityReserve(address recipient, uint256 amount) external onlyOwner nonReentrant {
        require(recipient != address(0), "Invalid recipient");
        require(amount > 0, "Amount must be positive");
        require(communityReservePool >= amount, "Insufficient community reserve");
        
        communityReservePool -= amount;
        _transfer(address(this), recipient, amount);
        
        emit RewardDistributed(recipient, amount, RewardCategory.CommunityReserve, "Community reserve withdrawal");
    }
}
