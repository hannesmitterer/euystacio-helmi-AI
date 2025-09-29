// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract KarmaBond is Ownable {
    address public foundationWallet;
    IERC20 public governanceToken;

    uint256 public MATL = 10; // <=10%
    uint256 public R1 = 45;   // >=4.5% (scaled *10)

    mapping(address => uint256) public investments;

    constructor(address _foundationWallet, address _governanceToken) {
        foundationWallet = _foundationWallet;
        governanceToken = IERC20(_governanceToken);
    }

    function invest() external payable {
        require(msg.value > 0, "No ETH sent");
        investments[msg.sender] += msg.value;
    }

    function redeem(address investor) external onlyOwner {
        if (MATL <= 10 && R1 >= 45) {
            uint256 amount = investments[investor];
            investments[investor] = 0;
            payable(investor).transfer(amount);
        } else {
            uint256 amount = investments[investor];
            investments[investor] = 0;
            payable(foundationWallet).transfer(amount);
        }
    }
}