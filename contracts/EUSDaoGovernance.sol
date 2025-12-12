// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title EUSDaoGovernance
 * @notice DAO Governance contract aligned with Cosimbiosi Basis Fundamentum in Eternuum
 * @dev Implements transparent, participatory governance respecting individual autonomy
 * 
 * ETHICAL PRINCIPLES:
 * - Transparency: All operations are visible and interpretable
 * - Universal Accessibility: Open participation for all stakeholders
 * - Individual Choice: No forced participation (Zero-Obligation - NRE-002)
 * - Dignity & Autonomy: Respects the inherent worth and self-determination of all participants
 * - Collaborative Harmony: Promotes sustainable cooperation between decentralized networks
 */
contract EUSDaoGovernance is ERC20, Ownable {
    mapping(address => uint256) public contributionScore;

    constructor() ERC20("Euystacio Stewardship", "EUS") {}

    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }

    function setContributionScore(address user, uint256 score) external onlyOwner {
        contributionScore[user] = score;
    }

    function votingPower(address user) public view returns (uint256) {
        // voting power = balance * (1 + contributionScore)
        return balanceOf(user) * (contributionScore[user] + 1);
    }
}