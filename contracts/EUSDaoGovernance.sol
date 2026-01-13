// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

interface IRedCodeVeto {
    function operationsAllowed() external view returns (bool);
    function isActiveState() external view returns (bool);
}

contract EUSDaoGovernance is ERC20, Ownable {
    mapping(address => uint256) public contributionScore;
    IRedCodeVeto public redCodeVeto;

    event RedCodeVetoUpdated(address indexed previous, address indexed current);
    event OperationVetoed(string operation, string reason);

    constructor() ERC20("Euystacio Stewardship", "EUS") {}

    /**
     * @notice Set the Red Code Veto contract address
     * @param _redCodeVeto Address of Red Code Veto contract
     */
    function setRedCodeVeto(address _redCodeVeto) external onlyOwner {
        address previous = address(redCodeVeto);
        redCodeVeto = IRedCodeVeto(_redCodeVeto);
        emit RedCodeVetoUpdated(previous, _redCodeVeto);
    }

    function mint(address to, uint256 amount) external onlyOwner {
        // Check Red Code Veto before minting
        if (address(redCodeVeto) != address(0)) {
            require(redCodeVeto.operationsAllowed(), "Red Code Veto: Operations not allowed");
        }
        _mint(to, amount);
    }

    function setContributionScore(address user, uint256 score) external onlyOwner {
        // Check Red Code Veto before updating scores
        if (address(redCodeVeto) != address(0)) {
            require(redCodeVeto.operationsAllowed(), "Red Code Veto: Operations not allowed");
        }
        contributionScore[user] = score;
    }

    function votingPower(address user) public view returns (uint256) {
        // voting power = balance * (1 + contributionScore)
        return balanceOf(user) * (contributionScore[user] + 1);
    }
}