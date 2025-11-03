// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title EUSDaoGovernance
 * @dev Governance contract with all permissions centralized under Seedbringer
 * Manages contribution scores and voting power
 */
contract EUSDaoGovernance is ERC20, Ownable {
    // Seedbringer identity seal
    bytes32 public immutable SEEDBRINGER_SEAL;
    address public seedbringerAddress;

    mapping(address => uint256) public contributionScore;

    event ContributionScoreUpdated(address indexed user, uint256 score);
    event SeedbringerUpdated(address indexed oldSeedbringer, address indexed newSeedbringer);

    modifier onlySeedbringer() {
        require(msg.sender == seedbringerAddress, "Only Seedbringer can call");
        _;
    }

    constructor(address _seedbringer) ERC20("Euystacio Stewardship", "EUS") {
        // Set Seedbringer seal: keccak256("hannesmitterer")
        SEEDBRINGER_SEAL = keccak256(abi.encodePacked("hannesmitterer"));
        seedbringerAddress = _seedbringer;
        
        // Transfer ownership to Seedbringer
        _transferOwnership(_seedbringer);
    }

    /**
     * @dev Mint tokens - only Seedbringer
     */
    function mint(address to, uint256 amount) external onlySeedbringer {
        _mint(to, amount);
    }

    /**
     * @dev Set contribution score for a user - only Seedbringer
     * This generates and manages contribution scores
     */
    function setContributionScore(address user, uint256 score) external onlySeedbringer {
        contributionScore[user] = score;
        emit ContributionScoreUpdated(user, score);
    }

    /**
     * @dev Batch set contribution scores - only Seedbringer
     */
    function batchSetContributionScores(
        address[] calldata users,
        uint256[] calldata scores
    ) external onlySeedbringer {
        require(users.length == scores.length, "Array length mismatch");
        
        for (uint256 i = 0; i < users.length; i++) {
            contributionScore[users[i]] = scores[i];
            emit ContributionScoreUpdated(users[i], scores[i]);
        }
    }

    /**
     * @dev Calculate voting power based on balance and contribution score
     * Formula: balance * (1 + contributionScore)
     */
    function votingPower(address user) public view returns (uint256) {
        return balanceOf(user) * (contributionScore[user] + 1);
    }

    /**
     * @dev Update Seedbringer address - only current Seedbringer
     */
    function updateSeedbringer(address newSeedbringer) external onlySeedbringer {
        require(newSeedbringer != address(0), "Invalid address");
        address oldSeedbringer = seedbringerAddress;
        seedbringerAddress = newSeedbringer;
        
        // Also transfer ownership
        _transferOwnership(newSeedbringer);
        
        emit SeedbringerUpdated(oldSeedbringer, newSeedbringer);
    }

    /**
     * @dev Get governance info for a user
     */
    function getGovernanceInfo(address user) external view returns (
        uint256 balance,
        uint256 contribution,
        uint256 voting
    ) {
        return (
            balanceOf(user),
            contributionScore[user],
            votingPower(user)
        );
    }
}