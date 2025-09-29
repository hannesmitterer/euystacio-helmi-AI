// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

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
        return balanceOf(user) * (contributionScore[user] + 1);
    }
}