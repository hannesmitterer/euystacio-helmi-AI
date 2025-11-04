// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

contract KarmaBond is Ownable {
    // Seedbringer authority - keccak256("hannesmitterer")
    bytes32 public constant SEEDBRINGER_HASH = 0x7b11220dc61c8a1f0f489ffae1410aba2b6aded2c713617a0361e1e60766cbed;
    address public seedbringer;
    address public foundationWallet;
    
    // Minimum investment: $100 equivalent in wei (approximated as 0.03 ETH at ~$3300/ETH)
    uint256 public constant MIN_INVESTMENT = 0.03 ether;
    
    // 5% redemption fee (in basis points: 500 = 5%)
    uint256 public constant REDEMPTION_FEE = 500;
    uint256 public constant FEE_DENOMINATOR = 10000;
    
    // simple invariants. In production, use an oracle or signed attestation.
    uint256 public MATL; // MATL in percent, e.g. 10 means 10%
    uint256 public R1;   // R1 scaled by 10 (e.g. 45 -> 4.5%)

    struct Investment {
        uint256 amount;
        uint256 startTime;
        uint256 duration; // in seconds
        bool redCodeCompliant;
    }
    
    mapping(address => Investment) public investments;
    
    event InvestmentMade(address indexed investor, uint256 amount, uint256 duration);
    event Redeemed(address indexed investor, uint256 amount, uint256 fee);
    event InvariantsUpdated(uint256 matl, uint256 r1);
    event RedCodeStatusUpdated(address indexed investor, bool status);
    event SeedbringerUpdated(address indexed newSeedbringer);

    modifier onlySeedbringer() {
        require(msg.sender == seedbringer, "Only Seedbringer");
        _;
    }

    constructor(address _foundationWallet, address _seedbringer) {
        foundationWallet = _foundationWallet;
        seedbringer = _seedbringer;
        MATL = 100; // default worst-case; owner should set realistic via oracle
        R1 = 0;     // default
    }

    receive() external payable {
        invest(365 days); // default duration: 1 year
    }

    function invest(uint256 duration) public payable {
        require(msg.value >= MIN_INVESTMENT, "Investment below minimum");
        require(duration > 0, "Duration must be positive");
        
        Investment storage inv = investments[msg.sender];
        inv.amount += msg.value;
        inv.startTime = block.timestamp;
        inv.duration = duration;
        // Red Code compliance starts as false, must be certified
        
        emit InvestmentMade(msg.sender, msg.value, duration);
    }

    /// Seedbringer can certify Red Code compliance
    function certifyRedCode(address investor, bool status) external onlySeedbringer {
        investments[investor].redCodeCompliant = status;
        emit RedCodeStatusUpdated(investor, status);
    }

    /// owner can update invariants (in production use oracle/signed attestation)
    function setInvariants(uint256 _MATL, uint256 _R1) external onlyOwner {
        MATL = _MATL;
        R1 = _R1;
        emit InvariantsUpdated(MATL, R1);
    }

    /// redeem: only owner (DAO multisig) triggers actual payouts after checks
    function redeem(address investor) external onlyOwner {
        Investment storage inv = investments[investor];
        require(inv.amount > 0, "No investment");
        require(inv.redCodeCompliant, "Red Code certification required");
        require(block.timestamp >= inv.startTime + inv.duration, "Investment period not complete");

        uint256 amount = inv.amount;
        inv.amount = 0;

        if (MATL <= 10 && R1 >= 45) {
            // invariants met -> apply 5% fee and return funds
            uint256 fee = (amount * REDEMPTION_FEE) / FEE_DENOMINATOR;
            uint256 netAmount = amount - fee;
            
            // Send fee to foundation
            payable(foundationWallet).transfer(fee);
            // Send net amount to investor
            payable(investor).transfer(netAmount);
            
            emit Redeemed(investor, netAmount, fee);
        } else {
            // invariants violated -> redirect to recirculation wallet
            payable(foundationWallet).transfer(amount);
            emit Redeemed(investor, 0, amount);
        }
    }

    /// Seedbringer can update the Seedbringer address
    function updateSeedbringer(address newSeedbringer) external onlySeedbringer {
        seedbringer = newSeedbringer;
        emit SeedbringerUpdated(newSeedbringer);
    }

    /// fallback admin functionality to withdraw accidentally-sent funds (onlyOwner)
    function emergencyWithdraw(address to, uint256 amount) external onlyOwner {
        payable(to).transfer(amount);
    }
}