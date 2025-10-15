// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

contract KarmaBond is Ownable {
    address public foundationWallet;
    // simple invariants. In production, use an oracle or signed attestation.
    uint256 public MATL; // MATL in percent, e.g. 10 means 10%
    uint256 public R1;   // R1 scaled by 10 (e.g. 45 -> 4.5%)

    mapping(address => uint256) public investments;
    event InvestmentMade(address indexed investor, uint256 amount);
    event Redeemed(address indexed investor, uint256 amount);
    event InvariantsUpdated(uint256 matl, uint256 r1);

    constructor(address _foundationWallet) {
        foundationWallet = _foundationWallet;
        MATL = 100; // default worst-case; owner should set realistic via oracle
        R1 = 0;     // default
    }

    receive() external payable {
        invest();
    }

    function invest() public payable {
        require(msg.value > 0, "Send ETH to invest");
        investments[msg.sender] += msg.value;
        emit InvestmentMade(msg.sender, msg.value);
    }

    /// owner can update invariants (in production use oracle/signed attestation)
    function setInvariants(uint256 _MATL, uint256 _R1) external onlyOwner {
        MATL = _MATL;
        R1 = _R1;
        emit InvariantsUpdated(MATL, R1);
    }

    /// redeem: only owner (DAO multisig) triggers actual payouts after checks
    function redeem(address investor) external onlyOwner {
        uint256 amount = investments[investor];
        require(amount > 0, "No investment");

        investments[investor] = 0;

        if (MATL <= 10 && R1 >= 45) {
            // invariants met -> return funds
            payable(investor).transfer(amount);
            emit Redeemed(investor, amount);
        } else {
            // invariants violated -> redirect to recirculation wallet
            payable(foundationWallet).transfer(amount);
        }
    }

    /// fallback admin functionality to withdraw accidentally-sent funds (onlyOwner)
    function emergencyWithdraw(address to, uint256 amount) external onlyOwner {
        payable(to).transfer(amount);
    }
}