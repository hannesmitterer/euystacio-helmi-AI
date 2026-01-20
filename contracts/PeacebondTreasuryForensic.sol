// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title PeacebondTreasuryForensic
 * @dev EU 2026 Compliance - Peacebond Treasury with Forensic Switch
 * 
 * Protocollo: EUYSTACIO / NSR
 * Implementazione: Gestione del Peacebond Treasury
 * 
 * Features:
 * - Detects centralized blocks/freeze attempts
 * - Automatic resource redirection in secure mode
 * - Forensic switch for emergency situations
 * - Multi-signature governance
 */

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract PeacebondTreasuryForensic is Ownable, ReentrancyGuard {
    
    // ============ State Variables ============
    
    /// @notice Resonance Credits token
    IERC20 public resonanceCredits;
    
    /// @notice Emergency backup addresses for secure redirection
    address[] public backupAddresses;
    
    /// @notice Forensic switch state
    bool public forensicSwitchActivated;
    
    /// @notice Block detection threshold (number of failed transactions)
    uint256 public blockDetectionThreshold;
    
    /// @notice Counter for failed transactions (potential blocks)
    uint256 public failedTransactionCount;
    
    /// @notice Minimum number of backup addresses required
    uint256 public constant MIN_BACKUP_ADDRESSES = 3;
    
    /// @notice Cooldown period for forensic switch (in seconds)
    uint256 public constant FORENSIC_COOLDOWN = 1 hours;
    
    /// @notice Last forensic switch activation time
    uint256 public lastForensicActivation;
    
    /// @notice Authorized guardians for forensic switch
    mapping(address => bool) public authorizedGuardians;
    
    /// @notice Number of authorized guardians
    uint256 public guardianCount;
    
    /// @notice Minimum number of guardian approvals needed
    uint256 public requiredGuardianApprovals;
    
    /// @notice Guardian approvals for forensic switch
    mapping(address => bool) public guardianApprovals;
    
    /// @notice Current number of guardian approvals
    uint256 public currentApprovals;
    
    // ============ Events ============
    
    event ForensicSwitchActivated(address indexed activator, uint256 timestamp);
    event ForensicSwitchDeactivated(address indexed deactivator, uint256 timestamp);
    event BackupAddressAdded(address indexed backupAddress);
    event BackupAddressRemoved(address indexed backupAddress);
    event CentralizedBlockDetected(uint256 failedCount, uint256 timestamp);
    event ResourceRedirected(address indexed from, address indexed to, uint256 amount);
    event GuardianAdded(address indexed guardian);
    event GuardianRemoved(address indexed guardian);
    event GuardianApprovalGranted(address indexed guardian);
    event GuardianApprovalRevoked(address indexed guardian);
    event EmergencyWithdrawal(address indexed to, uint256 amount);
    
    // ============ Modifiers ============
    
    modifier onlyGuardian() {
        require(authorizedGuardians[msg.sender], "Not an authorized guardian");
        _;
    }
    
    modifier whenNotForensic() {
        require(!forensicSwitchActivated, "Forensic switch is activated");
        _;
    }
    
    modifier whenForensic() {
        require(forensicSwitchActivated, "Forensic switch not activated");
        _;
    }
    
    // ============ Constructor ============
    
    constructor(
        address _resonanceCredits,
        uint256 _blockDetectionThreshold,
        uint256 _requiredGuardianApprovals
    ) {
        require(_resonanceCredits != address(0), "Invalid token address");
        require(_blockDetectionThreshold > 0, "Invalid threshold");
        require(_requiredGuardianApprovals > 0, "Invalid approvals required");
        
        resonanceCredits = IERC20(_resonanceCredits);
        blockDetectionThreshold = _blockDetectionThreshold;
        requiredGuardianApprovals = _requiredGuardianApprovals;
        forensicSwitchActivated = false;
        failedTransactionCount = 0;
        guardianCount = 0;
        currentApprovals = 0;
        
        // Add deployer as first guardian
        authorizedGuardians[msg.sender] = true;
        guardianCount = 1;
    }
    
    // ============ Guardian Management ============
    
    /**
     * @notice Add a new authorized guardian
     * @param _guardian Address of the guardian to add
     */
    function addGuardian(address _guardian) external onlyOwner {
        require(_guardian != address(0), "Invalid guardian address");
        require(!authorizedGuardians[_guardian], "Guardian already authorized");
        
        authorizedGuardians[_guardian] = true;
        guardianCount++;
        
        emit GuardianAdded(_guardian);
    }
    
    /**
     * @notice Remove an authorized guardian
     * @param _guardian Address of the guardian to remove
     */
    function removeGuardian(address _guardian) external onlyOwner {
        require(authorizedGuardians[_guardian], "Guardian not authorized");
        require(guardianCount > requiredGuardianApprovals, "Cannot remove guardian");
        
        authorizedGuardians[_guardian] = false;
        guardianCount--;
        
        // Revoke any existing approval
        if (guardianApprovals[_guardian]) {
            guardianApprovals[_guardian] = false;
            currentApprovals--;
        }
        
        emit GuardianRemoved(_guardian);
    }
    
    /**
     * @notice Guardian grants approval for forensic switch
     */
    function grantForensicApproval() external onlyGuardian {
        require(!guardianApprovals[msg.sender], "Already approved");
        
        guardianApprovals[msg.sender] = true;
        currentApprovals++;
        
        emit GuardianApprovalGranted(msg.sender);
        
        // Auto-activate if threshold reached
        if (currentApprovals >= requiredGuardianApprovals && !forensicSwitchActivated) {
            _activateForensicSwitch();
        }
    }
    
    /**
     * @notice Guardian revokes approval for forensic switch
     */
    function revokeForensicApproval() external onlyGuardian {
        require(guardianApprovals[msg.sender], "Not approved");
        
        guardianApprovals[msg.sender] = false;
        currentApprovals--;
        
        emit GuardianApprovalRevoked(msg.sender);
    }
    
    // ============ Backup Address Management ============
    
    /**
     * @notice Add a backup address for secure redirection
     * @param _backupAddress Address to add as backup
     */
    function addBackupAddress(address _backupAddress) external onlyOwner {
        require(_backupAddress != address(0), "Invalid backup address");
        
        // Check if already exists
        for (uint256 i = 0; i < backupAddresses.length; i++) {
            require(backupAddresses[i] != _backupAddress, "Backup already exists");
        }
        
        backupAddresses.push(_backupAddress);
        emit BackupAddressAdded(_backupAddress);
    }
    
    /**
     * @notice Remove a backup address
     * @param _backupAddress Address to remove
     */
    function removeBackupAddress(address _backupAddress) external onlyOwner {
        require(backupAddresses.length > MIN_BACKUP_ADDRESSES, "Cannot remove backup");
        
        for (uint256 i = 0; i < backupAddresses.length; i++) {
            if (backupAddresses[i] == _backupAddress) {
                backupAddresses[i] = backupAddresses[backupAddresses.length - 1];
                backupAddresses.pop();
                emit BackupAddressRemoved(_backupAddress);
                return;
            }
        }
        
        revert("Backup address not found");
    }
    
    // ============ Block Detection ============
    
    /**
     * @notice Report a failed transaction (potential centralized block)
     * @dev Can only be called by guardians
     */
    function reportFailedTransaction() external onlyGuardian {
        failedTransactionCount++;
        
        emit CentralizedBlockDetected(failedTransactionCount, block.timestamp);
        
        // Auto-activate forensic switch if threshold exceeded
        if (failedTransactionCount >= blockDetectionThreshold && !forensicSwitchActivated) {
            grantForensicApproval();
        }
    }
    
    /**
     * @notice Reset failed transaction counter
     * @dev Can only be called by owner when situation normalized
     */
    function resetFailedTransactionCount() external onlyOwner {
        failedTransactionCount = 0;
    }
    
    // ============ Forensic Switch ============
    
    /**
     * @notice Internal function to activate forensic switch
     */
    function _activateForensicSwitch() internal {
        require(!forensicSwitchActivated, "Already activated");
        require(
            block.timestamp >= lastForensicActivation + FORENSIC_COOLDOWN,
            "Cooldown period not elapsed"
        );
        
        forensicSwitchActivated = true;
        lastForensicActivation = block.timestamp;
        
        emit ForensicSwitchActivated(msg.sender, block.timestamp);
    }
    
    /**
     * @notice Manually activate forensic switch (requires owner + approvals)
     */
    function activateForensicSwitch() external onlyOwner {
        require(currentApprovals >= requiredGuardianApprovals, "Insufficient approvals");
        _activateForensicSwitch();
    }
    
    /**
     * @notice Deactivate forensic switch
     * @dev Requires owner and resets all approvals
     */
    function deactivateForensicSwitch() external onlyOwner whenForensic {
        forensicSwitchActivated = false;
        
        // Reset all approvals
        currentApprovals = 0;
        for (uint256 i = 0; i < guardianCount; i++) {
            // Note: In production, you'd iterate through guardian addresses
            // This is a simplified version
        }
        
        emit ForensicSwitchDeactivated(msg.sender, block.timestamp);
    }
    
    // ============ Resource Redirection ============
    
    /**
     * @notice Redirect resources to secure backup addresses
     * @dev Activated when forensic switch is on
     */
    function redirectResources() external whenForensic nonReentrant {
        require(backupAddresses.length >= MIN_BACKUP_ADDRESSES, "Insufficient backup addresses");
        
        uint256 balance = resonanceCredits.balanceOf(address(this));
        require(balance > 0, "No resources to redirect");
        
        // Distribute evenly across backup addresses
        uint256 amountPerBackup = balance / backupAddresses.length;
        
        for (uint256 i = 0; i < backupAddresses.length; i++) {
            require(
                resonanceCredits.transfer(backupAddresses[i], amountPerBackup),
                "Transfer failed"
            );
            
            emit ResourceRedirected(address(this), backupAddresses[i], amountPerBackup);
        }
        
        // Transfer any remainder to first backup
        uint256 remainder = resonanceCredits.balanceOf(address(this));
        if (remainder > 0) {
            require(
                resonanceCredits.transfer(backupAddresses[0], remainder),
                "Remainder transfer failed"
            );
        }
    }
    
    /**
     * @notice Emergency withdrawal when forensic switch active
     * @param _to Address to withdraw to (must be backup address)
     * @param _amount Amount to withdraw
     */
    function emergencyWithdraw(address _to, uint256 _amount) 
        external 
        onlyGuardian 
        whenForensic 
        nonReentrant 
    {
        // Verify _to is a backup address
        bool isBackup = false;
        for (uint256 i = 0; i < backupAddresses.length; i++) {
            if (backupAddresses[i] == _to) {
                isBackup = true;
                break;
            }
        }
        require(isBackup, "Not a backup address");
        
        require(
            resonanceCredits.transfer(_to, _amount),
            "Emergency withdrawal failed"
        );
        
        emit EmergencyWithdrawal(_to, _amount);
    }
    
    // ============ View Functions ============
    
    /**
     * @notice Get current treasury balance
     */
    function getTreasuryBalance() external view returns (uint256) {
        return resonanceCredits.balanceOf(address(this));
    }
    
    /**
     * @notice Get all backup addresses
     */
    function getBackupAddresses() external view returns (address[] memory) {
        return backupAddresses;
    }
    
    /**
     * @notice Check if forensic switch can be activated
     */
    function canActivateForensicSwitch() external view returns (bool) {
        return currentApprovals >= requiredGuardianApprovals &&
               !forensicSwitchActivated &&
               block.timestamp >= lastForensicActivation + FORENSIC_COOLDOWN;
    }
    
    /**
     * @notice Get treasury status
     */
    function getStatus() external view returns (
        bool forensicActive,
        uint256 balance,
        uint256 backupCount,
        uint256 failedTxCount,
        uint256 approvalCount,
        bool canActivate
    ) {
        return (
            forensicSwitchActivated,
            resonanceCredits.balanceOf(address(this)),
            backupAddresses.length,
            failedTransactionCount,
            currentApprovals,
            currentApprovals >= requiredGuardianApprovals &&
                !forensicSwitchActivated &&
                block.timestamp >= lastForensicActivation + FORENSIC_COOLDOWN
        );
    }
    
    // ============ Configuration ============
    
    /**
     * @notice Update block detection threshold
     */
    function setBlockDetectionThreshold(uint256 _newThreshold) external onlyOwner {
        require(_newThreshold > 0, "Invalid threshold");
        blockDetectionThreshold = _newThreshold;
    }
    
    /**
     * @notice Update required guardian approvals
     */
    function setRequiredGuardianApprovals(uint256 _newRequired) external onlyOwner {
        require(_newRequired > 0, "Invalid requirement");
        require(_newRequired <= guardianCount, "More than available guardians");
        requiredGuardianApprovals = _newRequired;
    }
}
