// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract EUSDaoGovernance is ERC20, Ownable {
    address public immutable SEEDBRINGER; // Exclusive governance authority
    bytes32 public immutable SEEDBRINGER_NAME_SEAL; // keccak256("hannesmitterer")
    
    mapping(address => uint256) public contributionScore;
    mapping(address => uint256) public bondContributions;
    mapping(address => uint256) public trancheDistributions;
    
    // Future-proofing: Seedbringer sustainment mechanism
    // NOTE: This represents 10000 ETH in wei. For production, use a stablecoin or oracle
    // to ensure the value approximates $10,000 USD regardless of ETH price fluctuations.
    uint256 public constant SEEDBRINGER_SUSTAINMENT_MONTHLY = 10000 * 10**18; // 10000 ETH (placeholder for $10,000 USD value)
    bool public sustainmentEnabled;
    uint256 public lastSustainmentTimestamp;
    
    event ContributionScoreUpdated(address indexed user, uint256 score);
    event BondContributionSynced(address indexed user, uint256 amount);
    event TrancheDistributionSynced(address indexed user, uint256 amount);
    event SustainmentToggled(bool enabled);
    event SustainmentPaid(address indexed seedbringer, uint256 amount, uint256 timestamp);

    constructor(address _seedbringer) ERC20("Euystacio Stewardship", "EUS") {
        SEEDBRINGER = _seedbringer;
        SEEDBRINGER_NAME_SEAL = keccak256(abi.encodePacked("hannesmitterer"));
        sustainmentEnabled = false;
        lastSustainmentTimestamp = block.timestamp;
    }
    
    /// Only Seedbringer can perform governance operations
    modifier onlySeedbringer() {
        require(msg.sender == SEEDBRINGER, "Only Seedbringer has governance authority");
        _;
    }

    function mint(address to, uint256 amount) external onlySeedbringer {
        _mint(to, amount);
    }

    function setContributionScore(address user, uint256 score) external onlySeedbringer {
        contributionScore[user] = score;
        emit ContributionScoreUpdated(user, score);
    }
    
    /// Sync bond contributions from KarmaBond contract
    function syncBondContribution(address user, uint256 amount) external onlyOwner {
        bondContributions[user] += amount;
        // Update contribution score based on bond contributions
        contributionScore[user] += amount / 10**18; // 1 point per ETH
        emit BondContributionSynced(user, amount);
    }
    
    /// Sync tranche distributions from TrustlessFundingProtocol
    function syncTrancheDistribution(address user, uint256 amount) external onlyOwner {
        trancheDistributions[user] += amount;
        emit TrancheDistributionSynced(user, amount);
    }

    function votingPower(address user) public view returns (uint256) {
        // voting power = balance * (1 + contributionScore)
        return balanceOf(user) * (contributionScore[user] + 1);
    }
    
    /// Toggle Seedbringer sustainment mechanism (only Seedbringer)
    function toggleSustainment(bool enabled) external onlySeedbringer {
        sustainmentEnabled = enabled;
        emit SustainmentToggled(enabled);
    }
    
    /// Process monthly sustainment payment (only if enabled)
    function processMonthlySustainment() external {
        require(sustainmentEnabled, "Sustainment not enabled");
        require(block.timestamp >= lastSustainmentTimestamp + 30 days, "Too early for sustainment");
        require(address(this).balance >= SEEDBRINGER_SUSTAINMENT_MONTHLY, "Insufficient balance");
        
        lastSustainmentTimestamp = block.timestamp;
        payable(SEEDBRINGER).transfer(SEEDBRINGER_SUSTAINMENT_MONTHLY);
        
        emit SustainmentPaid(SEEDBRINGER, SEEDBRINGER_SUSTAINMENT_MONTHLY, block.timestamp);
    }
    
    /// Allow contract to receive funds for sustainment
    receive() external payable {}
}