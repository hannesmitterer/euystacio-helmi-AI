// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/**
 * @title Sustainment
 * @notice Manages the Seedbringer sustainment fund with a configurable minimum threshold
 * @dev Enforces the $10,000 Minimum Sustenance Rule for governance operations
 */
contract Sustainment is Ownable, ReentrancyGuard {
    using SafeERC20 for IERC20;

    /// @notice The stablecoin token used for sustainment (e.g., USDC)
    IERC20 public immutable stableToken;
    
    /// @notice Decimals of the stable token (e.g., 6 for USDC)
    uint8 public immutable stableDecimals;
    
    /// @notice Minimum sustainment reserve required (in stable token base units)
    uint256 public minSustainment;
    
    /// @notice Current sustainment reserve balance (in stable token base units)
    uint256 public sustainmentReserve;
    
    /// @notice Authorized contracts that can deposit to sustainment
    mapping(address => bool) public authorizedDepositors;

    /// @notice Emitted when funds are deposited to sustainment
    event SustainmentDeposited(address indexed from, uint256 amount);
    
    /// @notice Emitted when the minimum sustainment threshold is updated
    event MinSustainmentUpdated(uint256 previous, uint256 current);
    
    /// @notice Emitted when funds are withdrawn from sustainment
    event SustainmentWithdrawn(address indexed to, uint256 amount);
    
    /// @notice Emitted when sustainment reserve is near threshold (within 5%)
    event SustainmentAlertNearThreshold(uint256 currentReserve, uint256 minSustainment);
    
    /// @notice Emitted when an authorized depositor is added or removed
    event AuthorizedDepositorUpdated(address indexed depositor, bool authorized);

    /**
     * @notice Constructor to initialize the Sustainment contract
     * @param _stableToken Address of the stablecoin token (e.g., USDC)
     * @param _stableDecimals Decimals of the stable token
     * @param _minSustainment Initial minimum sustainment in USD (will be scaled by decimals)
     */
    constructor(
        address _stableToken,
        uint8 _stableDecimals,
        uint256 _minSustainment
    ) {
        require(_stableToken != address(0), "Invalid stable token");
        stableToken = IERC20(_stableToken);
        stableDecimals = _stableDecimals;
        // Scale minimum by decimals (e.g., 10000 USD * 10^6 for USDC)
        minSustainment = _minSustainment * (10 ** _stableDecimals);
        emit MinSustainmentUpdated(0, minSustainment);
    }

    /**
     * @notice Deposit funds to the sustainment reserve
     * @param amount Amount of stable tokens to deposit
     */
    function depositToSustainment(uint256 amount) external nonReentrant {
        require(authorizedDepositors[msg.sender] || msg.sender == owner(), "Not authorized");
        require(amount > 0, "Amount must be positive");
        
        stableToken.safeTransferFrom(msg.sender, address(this), amount);
        sustainmentReserve += amount;
        
        emit SustainmentDeposited(msg.sender, amount);
        _checkThresholdAlert();
    }

    /**
     * @notice Receive sustainment share from bond minting (called by KarmaBond)
     * @param amount Amount of stable tokens allocated from bond
     */
    function receiveShareFromBond(uint256 amount) external nonReentrant {
        require(authorizedDepositors[msg.sender], "Not authorized bond contract");
        require(amount > 0, "Amount must be positive");
        
        // Note: Caller (KarmaBond) should have already transferred tokens
        // This function just records the allocation
        sustainmentReserve += amount;
        
        emit SustainmentDeposited(msg.sender, amount);
        _checkThresholdAlert();
    }

    /**
     * @notice Set the minimum sustainment threshold
     * @param newMinUSD New minimum in USD (will be scaled by decimals)
     */
    function setMinSustainment(uint256 newMinUSD) external onlyOwner {
        uint256 previous = minSustainment;
        minSustainment = newMinUSD * (10 ** stableDecimals);
        emit MinSustainmentUpdated(previous, minSustainment);
        _checkThresholdAlert();
    }

    /**
     * @notice Withdraw from sustainment reserve (for Seedbringer payouts)
     * @param to Recipient address
     * @param amount Amount to withdraw
     */
    function withdrawSustainment(address to, uint256 amount) external onlyOwner nonReentrant {
        require(to != address(0), "Invalid recipient");
        require(amount > 0, "Amount must be positive");
        require(sustainmentReserve >= amount, "Insufficient reserve");
        
        sustainmentReserve -= amount;
        stableToken.safeTransfer(to, amount);
        
        emit SustainmentWithdrawn(to, amount);
        _checkThresholdAlert();
    }

    /**
     * @notice Add or remove an authorized depositor (e.g., KarmaBond contract)
     * @param depositor Address to authorize/unauthorize
     * @param authorized True to authorize, false to remove
     */
    function setAuthorizedDepositor(address depositor, bool authorized) external onlyOwner {
        require(depositor != address(0), "Invalid depositor");
        authorizedDepositors[depositor] = authorized;
        emit AuthorizedDepositorUpdated(depositor, authorized);
    }

    /**
     * @notice Get current sustainment reserve balance
     * @return Current reserve in stable token base units
     */
    function getSustainmentReserve() external view returns (uint256) {
        return sustainmentReserve;
    }

    /**
     * @notice Check if sustainment reserve is above minimum threshold
     * @return True if reserve >= minSustainment, false otherwise
     */
    function isAboveMinimum() external view returns (bool) {
        return sustainmentReserve >= minSustainment;
    }

    /**
     * @notice Check if reserve would be above minimum after a withdrawal
     * @param withdrawalAmount Amount to potentially withdraw
     * @return True if reserve would remain >= minSustainment after withdrawal
     */
    function wouldRemainAboveMinimum(uint256 withdrawalAmount) external view returns (bool) {
        if (sustainmentReserve < withdrawalAmount) {
            return false;
        }
        return (sustainmentReserve - withdrawalAmount) >= minSustainment;
    }

    /**
     * @dev Check if reserve is within 5% of minimum and emit alert
     */
    function _checkThresholdAlert() private {
        if (sustainmentReserve > 0 && sustainmentReserve < minSustainment) {
            emit SustainmentAlertNearThreshold(sustainmentReserve, minSustainment);
        } else if (sustainmentReserve >= minSustainment) {
            // Check if within 5% above minimum
            uint256 threshold = minSustainment + (minSustainment * 5 / 100);
            if (sustainmentReserve <= threshold) {
                emit SustainmentAlertNearThreshold(sustainmentReserve, minSustainment);
            }
        }
    }
}
