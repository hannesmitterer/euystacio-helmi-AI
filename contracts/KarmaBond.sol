// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

interface ISustainment {
    function receiveShareFromBond(uint256 amount) external;
    function isAboveMinimum() external view returns (bool);
    function getSustainmentReserve() external view returns (uint256);
    function minSustainment() external view returns (uint256);
}

/**
 * @title KarmaBond
 * @notice Manages bond minting and redemption with integrated sustainment allocation
 * @dev Allocates a configurable percentage of bond mints to the Sustainment contract
 */
contract KarmaBond is Ownable, ReentrancyGuard {
    using SafeERC20 for IERC20;

    /// @notice The stablecoin used for bonds (e.g., USDC)
    IERC20 public immutable stableToken;
    
    /// @notice Sustainment contract address
    ISustainment public sustainmentContract;
    
    /// @notice Foundation wallet for recirculation
    address public foundationWallet;
    
    /// @notice Percentage of bond mints allocated to sustainment (in basis points, 200 = 2%)
    uint256 public sustainmentPercent;
    
    /// @notice Reserve backing outstanding bonds (excludes sustainment allocation)
    uint256 public stableReserve;
    
    /// @notice Total bonds issued (in stable token units)
    uint256 public totalBondsIssued;
    
    /// @notice Bond balances per address
    mapping(address => uint256) public bondBalances;
    
    // Legacy invariants for redemption logic
    uint256 public MATL; // MATL in percent, e.g. 10 means 10%
    uint256 public R1;   // R1 scaled by 10 (e.g. 45 -> 4.5%)

    /// @notice Emitted when a bond is minted
    event BondMinted(address indexed investor, uint256 stableAmount, uint256 bondAmount);
    
    /// @notice Emitted when sustainment allocation is made
    event SustainmentAllocated(address indexed from, uint256 stableAmount, uint256 sustainmentShare);
    
    /// @notice Emitted when a bond is redeemed
    event BondRedeemed(address indexed investor, uint256 bondAmount, uint256 stableAmount);
    
    /// @notice Emitted when invariants are updated
    event InvariantsUpdated(uint256 matl, uint256 r1);
    
    /// @notice Emitted when sustainment percent is updated
    event SustainmentPercentUpdated(uint256 previous, uint256 current);
    
    /// @notice Emitted when sustainment contract is updated
    event SustainmentContractUpdated(address indexed previous, address indexed current);

    /**
     * @notice Constructor
     * @param _stableToken Address of stablecoin (e.g., USDC)
     * @param _sustainmentContract Address of Sustainment contract
     * @param _foundationWallet Address of foundation wallet
     * @param _sustainmentPercent Basis points for sustainment allocation (default 200 = 2%)
     */
    constructor(
        address _stableToken,
        address _sustainmentContract,
        address _foundationWallet,
        uint256 _sustainmentPercent
    ) {
        require(_stableToken != address(0), "Invalid stable token");
        require(_foundationWallet != address(0), "Invalid foundation wallet");
        
        stableToken = IERC20(_stableToken);
        sustainmentContract = ISustainment(_sustainmentContract);
        foundationWallet = _foundationWallet;
        sustainmentPercent = _sustainmentPercent;
        
        MATL = 100; // default worst-case; owner should set realistic via oracle
        R1 = 0;     // default
    }

    /**
     * @notice Mint bonds by depositing stablecoins
     * @param stableAmount Amount of stablecoins to deposit
     */
    function mintBond(uint256 stableAmount) external nonReentrant {
        require(stableAmount > 0, "Amount must be positive");
        
        // Calculate sustainment share
        uint256 sustainmentShare = (stableAmount * sustainmentPercent) / 10000;
        uint256 bondReserveAmount = stableAmount - sustainmentShare;
        
        // Transfer stable tokens from user
        stableToken.safeTransferFrom(msg.sender, address(this), stableAmount);
        
        // Handle sustainment allocation
        if (sustainmentShare > 0 && address(sustainmentContract) != address(0)) {
            // Transfer to sustainment contract
            stableToken.safeTransfer(address(sustainmentContract), sustainmentShare);
            sustainmentContract.receiveShareFromBond(sustainmentShare);
            emit SustainmentAllocated(msg.sender, stableAmount, sustainmentShare);
        }
        
        // Update reserves and mint bonds (1:1 ratio for simplicity)
        stableReserve += bondReserveAmount;
        bondBalances[msg.sender] += stableAmount; // Bond balance includes full amount
        totalBondsIssued += stableAmount;
        
        emit BondMinted(msg.sender, stableAmount, stableAmount);
    }

    /**
     * @notice Redeem bonds for stablecoins (owner controlled, checks invariants)
     * @param investor Address of bond holder
     * @param bondAmount Amount of bonds to redeem
     */
    function redeemBond(address investor, uint256 bondAmount) external onlyOwner nonReentrant {
        require(bondAmount > 0, "Amount must be positive");
        require(bondBalances[investor] >= bondAmount, "Insufficient bond balance");
        
        // Calculate redemption amount (applying sustainment deduction from original mint)
        uint256 sustainmentDeduction = (bondAmount * sustainmentPercent) / 10000;
        uint256 redemptionAmount = bondAmount - sustainmentDeduction;
        
        require(stableReserve >= redemptionAmount, "Insufficient reserve");
        
        bondBalances[investor] -= bondAmount;
        totalBondsIssued -= bondAmount;
        stableReserve -= redemptionAmount;

        if (MATL <= 10 && R1 >= 45) {
            // Invariants met -> return funds to investor
            stableToken.safeTransfer(investor, redemptionAmount);
            emit BondRedeemed(investor, bondAmount, redemptionAmount);
        } else {
            // Invariants violated -> redirect to recirculation wallet
            stableToken.safeTransfer(foundationWallet, redemptionAmount);
            emit BondRedeemed(investor, bondAmount, 0);
        }
    }

    /**
     * @notice Withdraw excess stable reserves (cannot touch sustainment or bonded reserves)
     * @param to Recipient address
     * @param amount Amount to withdraw
     */
    function withdrawExcessStable(address to, uint256 amount) external onlyOwner nonReentrant {
        require(to != address(0), "Invalid recipient");
        uint256 contractBalance = stableToken.balanceOf(address(this));
        uint256 excess = contractBalance > stableReserve ? contractBalance - stableReserve : 0;
        require(amount <= excess, "Amount exceeds excess reserves");
        
        stableToken.safeTransfer(to, amount);
    }

    /**
     * @notice Set invariants for redemption logic
     * @param _MATL MATL percentage
     * @param _R1 R1 scaled value
     */
    function setInvariants(uint256 _MATL, uint256 _R1) external onlyOwner {
        MATL = _MATL;
        R1 = _R1;
        emit InvariantsUpdated(MATL, R1);
    }

    /**
     * @notice Set sustainment allocation percentage
     * @param newPercent New percentage in basis points (e.g., 200 = 2%)
     */
    function setSustainmentPercent(uint256 newPercent) external onlyOwner {
        require(newPercent <= 10000, "Percent exceeds 100%");
        uint256 previous = sustainmentPercent;
        sustainmentPercent = newPercent;
        emit SustainmentPercentUpdated(previous, newPercent);
    }

    /**
     * @notice Set sustainment contract address
     * @param newContract New sustainment contract address
     */
    function setSustainmentContract(address newContract) external onlyOwner {
        address previous = address(sustainmentContract);
        sustainmentContract = ISustainment(newContract);
        emit SustainmentContractUpdated(previous, newContract);
    }

    /**
     * @notice Get bond balance for an address
     * @param account Address to query
     * @return Bond balance
     */
    function getBondBalance(address account) external view returns (uint256) {
        return bondBalances[account];
    }
}
