// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract EUSDaoGovernance is ERC20, Ownable {
    // Seedbringer authority - keccak256("hannesmitterer")
    bytes32 public constant SEEDBRINGER_HASH = 0x7b11220dc61c8a1f0f489ffae1410aba2b6aded2c713617a0361e1e60766cbed;
    address public seedbringer;
    
    struct ContributionMetrics {
        uint256 score;
        uint256 lastRecalibration;
        uint256 totalContributions;
        bool active;
    }
    
    mapping(address => ContributionMetrics) public contributionMetrics;
    
    // Voting power multiplier (in basis points)
    uint256 public constant SCORE_MULTIPLIER = 100; // 1% per contribution point
    uint256 public constant MULTIPLIER_DENOMINATOR = 10000;
    
    event ContributionScoreUpdated(address indexed user, uint256 newScore);
    event ContributionRecalibrated(address indexed user, uint256 newScore);
    event SeedbringerUpdated(address indexed newSeedbringer);
    event GovernanceActionExecuted(address indexed executor, string action);

    modifier onlySeedbringer() {
        require(msg.sender == seedbringer, "Only Seedbringer");
        _;
    }

    constructor(address _seedbringer) ERC20("Euystacio Stewardship", "EUS") {
        seedbringer = _seedbringer;
    }

    /// Seedbringer has ultimate minting authority
    function mint(address to, uint256 amount) external onlySeedbringer {
        _mint(to, amount);
    }

    /// Seedbringer controls contribution scoring
    function setContributionScore(address user, uint256 score) external onlySeedbringer {
        contributionMetrics[user].score = score;
        contributionMetrics[user].lastRecalibration = block.timestamp;
        contributionMetrics[user].active = true;
        emit ContributionScoreUpdated(user, score);
    }

    /// Seedbringer can recalibrate contributions
    function recalibrateContribution(address user, uint256 newScore, uint256 totalContributions) 
        external 
        onlySeedbringer 
    {
        ContributionMetrics storage metrics = contributionMetrics[user];
        metrics.score = newScore;
        metrics.totalContributions = totalContributions;
        metrics.lastRecalibration = block.timestamp;
        emit ContributionRecalibrated(user, newScore);
    }

    /// Batch update contribution scores (Seedbringer only)
    function batchUpdateScores(address[] calldata users, uint256[] calldata scores) 
        external 
        onlySeedbringer 
    {
        require(users.length == scores.length, "Array length mismatch");
        for (uint256 i = 0; i < users.length; i++) {
            contributionMetrics[users[i]].score = scores[i];
            contributionMetrics[users[i]].lastRecalibration = block.timestamp;
            contributionMetrics[users[i]].active = true;
            emit ContributionScoreUpdated(users[i], scores[i]);
        }
    }

    /// Calculate voting power based on token balance and contribution score
    function votingPower(address user) public view returns (uint256) {
        uint256 balance = balanceOf(user);
        ContributionMetrics memory metrics = contributionMetrics[user];
        
        if (!metrics.active) {
            return balance;
        }
        
        // voting power = balance * (1 + (score * SCORE_MULTIPLIER / MULTIPLIER_DENOMINATOR))
        uint256 multiplier = MULTIPLIER_DENOMINATOR + (metrics.score * SCORE_MULTIPLIER);
        return (balance * multiplier) / MULTIPLIER_DENOMINATOR;
    }

    /// Get detailed contribution metrics
    function getContributionMetrics(address user) 
        external 
        view 
        returns (
            uint256 score,
            uint256 lastRecalibration,
            uint256 totalContributions,
            bool active
        ) 
    {
        ContributionMetrics memory metrics = contributionMetrics[user];
        return (
            metrics.score,
            metrics.lastRecalibration,
            metrics.totalContributions,
            metrics.active
        );
    }

    /// Seedbringer governance oversight - execute arbitrary governance action
    function executeGovernanceAction(string calldata action) external onlySeedbringer {
        emit GovernanceActionExecuted(msg.sender, action);
    }

    /// Seedbringer can deactivate a user's contribution metrics
    function deactivateContributor(address user) external onlySeedbringer {
        contributionMetrics[user].active = false;
    }

    /// Seedbringer can update the Seedbringer address
    function updateSeedbringer(address newSeedbringer) external onlySeedbringer {
        seedbringer = newSeedbringer;
        emit SeedbringerUpdated(newSeedbringer);
    }

    /// Owner (DAO multisig) can perform administrative token operations
    function adminMint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }

    /// Owner can burn tokens from their own balance
    function burn(uint256 amount) external {
        _burn(msg.sender, amount);
    }
}