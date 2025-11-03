// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title KarmaBond
 * @dev Karma Bonds with minimum investment, flexible duration, and redemption fees.
 * Compatible with Red Code and Euystacio principles.
 */
contract KarmaBond is Ownable {
    address public foundationWallet;
    
    // Minimum investment: 100 USD equivalent in wei
    // For simplicity, using a fixed ETH amount that can be updated by owner
    // In production, this should be calculated via price oracle
    uint256 public minInvestmentUSD; // in USD cents (e.g., 10000 = 100 USD)
    uint256 public ethPriceUSD; // ETH price in USD cents (e.g., 200000 = 2000 USD)
    
    // Redemption fee: 5%
    uint256 public constant REDEMPTION_FEE_PERCENT = 5;
    uint256 public constant FEE_DENOMINATOR = 100;
    
    // Red Code compliance invariants
    uint256 public MATL; // MATL in percent, e.g. 10 means 10%
    uint256 public R1;   // R1 scaled by 10 (e.g. 45 -> 4.5%)

    struct Bond {
        uint256 amount;
        uint256 startTime;
        uint256 duration; // flexible duration in seconds, 0 means no lock
    }

    mapping(address => Bond) public bonds;
    event InvestmentMade(address indexed investor, uint256 amount, uint256 duration);
    event Redeemed(address indexed investor, uint256 amount, uint256 fee);
    event InvariantsUpdated(uint256 matl, uint256 r1);
    event PriceUpdated(uint256 ethPriceUSD);
    event MinInvestmentUpdated(uint256 minInvestmentUSD);

    constructor(address _foundationWallet, uint256 _ethPriceUSD) Ownable(msg.sender) {
        foundationWallet = _foundationWallet;
        minInvestmentUSD = 10000; // 100 USD in cents
        ethPriceUSD = _ethPriceUSD; // e.g., 200000 for 2000 USD/ETH
        MATL = 100; // default worst-case; owner should set realistic via oracle
        R1 = 0;     // default
    }

    receive() external payable {
        invest(0); // default to no lock period
    }

    /**
     * @dev Invest with flexible duration
     * @param duration Lock period in seconds (0 for no lock)
     */
    function invest(uint256 duration) public payable {
        require(msg.value > 0, "Send ETH to invest");
        
        // Check minimum investment (100 USD equivalent)
        uint256 usdValue = (msg.value * ethPriceUSD) / 1 ether;
        require(usdValue >= minInvestmentUSD, "Minimum investment is 100 USD");
        
        bonds[msg.sender].amount += msg.value;
        bonds[msg.sender].startTime = block.timestamp;
        bonds[msg.sender].duration = duration;
        
        emit InvestmentMade(msg.sender, msg.value, duration);
    }

    /// Update ETH price in USD (in production use oracle)
    function updateEthPrice(uint256 _ethPriceUSD) external onlyOwner {
        ethPriceUSD = _ethPriceUSD;
        emit PriceUpdated(_ethPriceUSD);
    }

    /// Update minimum investment amount
    function updateMinInvestment(uint256 _minInvestmentUSD) external onlyOwner {
        minInvestmentUSD = _minInvestmentUSD;
        emit MinInvestmentUpdated(_minInvestmentUSD);
    }

    /// owner can update invariants (in production use oracle/signed attestation)
    function setInvariants(uint256 _MATL, uint256 _R1) external onlyOwner {
        MATL = _MATL;
        R1 = _R1;
        emit InvariantsUpdated(MATL, R1);
    }

    /**
     * @dev Redeem bond with 5% transaction fee
     * Red Code compliance checked before redemption
     */
    function redeem(address investor) external onlyOwner {
        Bond memory bond = bonds[investor];
        require(bond.amount > 0, "No investment");
        
        // Check if duration has elapsed
        if (bond.duration > 0) {
            require(block.timestamp >= bond.startTime + bond.duration, "Lock period not elapsed");
        }

        uint256 amount = bond.amount;
        bonds[investor].amount = 0;

        if (MATL <= 10 && R1 >= 45) {
            // Red Code invariants met -> apply 5% fee and return funds
            uint256 fee = (amount * REDEMPTION_FEE_PERCENT) / FEE_DENOMINATOR;
            uint256 netAmount = amount - fee;
            
            // Fee goes to foundation
            payable(foundationWallet).transfer(fee);
            // Net amount to investor
            payable(investor).transfer(netAmount);
            
            emit Redeemed(investor, netAmount, fee);
        } else {
            // Red Code invariants violated -> redirect all funds to recirculation wallet
            payable(foundationWallet).transfer(amount);
            emit Redeemed(investor, 0, amount);
        }
    }

    /// fallback admin functionality to withdraw accidentally-sent funds (onlyOwner)
    function emergencyWithdraw(address to, uint256 amount) external onlyOwner {
        payable(to).transfer(amount);
    }
}