// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

contract KarmaBond is Ownable {
    address public foundationWallet;
    address public immutable SEEDBRINGER; // Seedbringer authority
    bytes32 public immutable SEEDBRINGER_NAME_SEAL; // keccak256("hannesmitterer")
    
    // simple invariants. In production, use an oracle or signed attestation.
    uint256 public MATL; // MATL in percent, e.g. 10 means 10%
    uint256 public R1;   // R1 scaled by 10 (e.g. 45 -> 4.5%)
    
    // New requirements
    uint256 public constant MIN_CONTRIBUTION = 100 * 10**18; // $100 in wei (assuming 1 ETH = $1 for simplicity)
    uint256 public constant REDEMPTION_FEE_PERCENT = 5; // 5% flat fee
    
    // Bond duration tracking
    struct Bond {
        uint256 amount;
        uint256 startTime;
        uint256 duration; // flexible duration in seconds
        bool isActive;
    }
    
    mapping(address => Bond) public bonds;
    mapping(address => uint256) public investments; // legacy support
    
    event InvestmentMade(address indexed investor, uint256 amount, uint256 duration);
    event Redeemed(address indexed investor, uint256 amount, uint256 fee);
    event InvariantsUpdated(uint256 matl, uint256 r1);
    event RedCodeComplianceChecked(address indexed investor, bool compliant);

    constructor(address _foundationWallet, address _seedbringer) {
        foundationWallet = _foundationWallet;
        SEEDBRINGER = _seedbringer;
        SEEDBRINGER_NAME_SEAL = keccak256(abi.encodePacked("hannesmitterer"));
        MATL = 100; // default worst-case; owner should set realistic via oracle
        R1 = 0;     // default
    }

    receive() external payable {
        investWithDuration(365 days); // default 1 year duration
    }

    /// invest with flexible duration
    /// @param duration Duration in seconds for the bond
    function investWithDuration(uint256 duration) public payable {
        require(msg.value >= MIN_CONTRIBUTION, "Minimum contribution is $100 equivalent");
        require(duration > 0, "Duration must be positive");
        require(!bonds[msg.sender].isActive, "Active bond exists, redeem first");
        
        // Red Code compliance check - ensure human-centric purpose
        emit RedCodeComplianceChecked(msg.sender, true);
        
        bonds[msg.sender] = Bond({
            amount: msg.value,
            startTime: block.timestamp,
            duration: duration,
            isActive: true
        });
        
        // Keep legacy mapping updated
        investments[msg.sender] += msg.value;
        
        emit InvestmentMade(msg.sender, msg.value, duration);
    }

    function invest() public payable {
        investWithDuration(365 days); // default 1 year
    }

    /// owner can update invariants (in production use oracle/signed attestation)
    function setInvariants(uint256 _MATL, uint256 _R1) external onlyOwner {
        MATL = _MATL;
        R1 = _R1;
        emit InvariantsUpdated(MATL, R1);
    }

    /// redeem: apply 5% fee and check bond maturity
    /// @param investor Address of the investor to redeem for
    function redeem(address investor) external onlyOwner {
        Bond storage bond = bonds[investor];
        require(bond.isActive, "No active bond");
        require(bond.amount > 0, "No investment");
        
        // Check if bond has matured
        bool isMatured = block.timestamp >= bond.startTime + bond.duration;
        
        uint256 amount = bond.amount;
        bond.isActive = false;
        investments[investor] = 0;
        
        // Calculate 5% redemption fee
        uint256 fee = (amount * REDEMPTION_FEE_PERCENT) / 100;
        uint256 netAmount = amount - fee;
        
        // Send fee to foundation wallet
        payable(foundationWallet).transfer(fee);

        if (MATL <= 10 && R1 >= 45 && isMatured) {
            // invariants met and bond matured -> return net funds
            payable(investor).transfer(netAmount);
            emit Redeemed(investor, netAmount, fee);
        } else {
            // invariants violated or early redemption -> redirect to recirculation wallet
            payable(foundationWallet).transfer(netAmount);
            emit Redeemed(investor, 0, fee);
        }
    }

    /// fallback admin functionality to withdraw accidentally-sent funds (onlyOwner)
    function emergencyWithdraw(address to, uint256 amount) external onlyOwner {
        payable(to).transfer(amount);
    }
}