// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title RedCodeVeto
 * @notice Implements the Red Code Veto H-Var mechanism for ethical governance enforcement
 * @dev Provides veto capability across all governance contracts to prevent unapproved actions
 */
contract RedCodeVeto is Ownable {
    // H-Var states
    enum VetoState {
        ACTIVE,      // Normal operations allowed
        SUSPENDED,   // All operations suspended pending review
        EMERGENCY    // Emergency state - only critical functions allowed
    }

    VetoState public currentState;
    
    // Veto reasons and metadata
    struct VetoRecord {
        VetoState state;
        string reason;
        uint256 timestamp;
        address initiator;
        bool active;
    }

    mapping(bytes32 => VetoRecord) public vetoRecords;
    bytes32[] public vetoHistory;
    
    // Council members who can initiate vetos
    mapping(address => bool) public councilMembers;
    uint256 public councilMemberCount;
    
    // Required signatures for veto actions
    uint256 public requiredSignatures;
    
    event StateChanged(VetoState indexed previousState, VetoState indexed newState, string reason);
    event VetoInitiated(bytes32 indexed vetoId, VetoState state, address indexed initiator, string reason);
    event VetoResolved(bytes32 indexed vetoId, address indexed resolver);
    event CouncilMemberAdded(address indexed member);
    event CouncilMemberRemoved(address indexed member);
    event RequiredSignaturesUpdated(uint256 oldValue, uint256 newValue);

    modifier onlyCouncil() {
        require(councilMembers[msg.sender], "RedCodeVeto: Not a council member");
        _;
    }

    modifier notSuspended() {
        require(currentState != VetoState.SUSPENDED, "RedCodeVeto: Operations suspended");
        _;
    }

    modifier notEmergency() {
        require(currentState != VetoState.EMERGENCY, "RedCodeVeto: Emergency state active");
        _;
    }

    constructor() {
        currentState = VetoState.ACTIVE;
        requiredSignatures = 1;
        
        // Add deployer as initial council member
        councilMembers[msg.sender] = true;
        councilMemberCount = 1;
        
        emit CouncilMemberAdded(msg.sender);
    }

    /**
     * @notice Add a council member who can initiate vetos
     * @param member Address to add as council member
     */
    function addCouncilMember(address member) external onlyOwner {
        require(!councilMembers[member], "RedCodeVeto: Already a member");
        require(member != address(0), "RedCodeVeto: Invalid address");
        
        councilMembers[member] = true;
        councilMemberCount++;
        
        emit CouncilMemberAdded(member);
    }

    /**
     * @notice Remove a council member
     * @param member Address to remove from council
     */
    function removeCouncilMember(address member) external onlyOwner {
        require(councilMembers[member], "RedCodeVeto: Not a member");
        require(councilMemberCount > requiredSignatures, "RedCodeVeto: Cannot remove, would break quorum");
        
        councilMembers[member] = false;
        councilMemberCount--;
        
        emit CouncilMemberRemoved(member);
    }

    /**
     * @notice Update required signatures for veto actions
     * @param signatures New required signature count
     */
    function setRequiredSignatures(uint256 signatures) external onlyOwner {
        require(signatures > 0, "RedCodeVeto: Must require at least 1 signature");
        require(signatures <= councilMemberCount, "RedCodeVeto: Cannot require more signatures than council members");
        
        uint256 oldValue = requiredSignatures;
        requiredSignatures = signatures;
        
        emit RequiredSignaturesUpdated(oldValue, signatures);
    }

    /**
     * @notice Initiate a veto with a specific state
     * @param state The veto state to apply
     * @param reason Human-readable reason for the veto
     * @return vetoId The unique identifier for this veto
     */
    function initiateVeto(VetoState state, string calldata reason) external onlyCouncil returns (bytes32) {
        require(state != VetoState.ACTIVE, "RedCodeVeto: Use resolveVeto to return to ACTIVE");
        require(bytes(reason).length > 0, "RedCodeVeto: Reason required");
        
        bytes32 vetoId = keccak256(abi.encodePacked(block.timestamp, msg.sender, reason));
        
        vetoRecords[vetoId] = VetoRecord({
            state: state,
            reason: reason,
            timestamp: block.timestamp,
            initiator: msg.sender,
            active: true
        });
        
        vetoHistory.push(vetoId);
        
        VetoState previousState = currentState;
        currentState = state;
        
        emit VetoInitiated(vetoId, state, msg.sender, reason);
        emit StateChanged(previousState, state, reason);
        
        return vetoId;
    }

    /**
     * @notice Resolve a veto and return to ACTIVE state
     * @param vetoId The veto identifier to resolve
     */
    function resolveVeto(bytes32 vetoId) external onlyCouncil {
        require(vetoRecords[vetoId].active, "RedCodeVeto: Veto not active or doesn't exist");
        
        vetoRecords[vetoId].active = false;
        
        VetoState previousState = currentState;
        currentState = VetoState.ACTIVE;
        
        emit VetoResolved(vetoId, msg.sender);
        emit StateChanged(previousState, VetoState.ACTIVE, "Veto resolved");
    }

    /**
     * @notice Emergency function to force return to ACTIVE state (owner only)
     * @param reason Reason for emergency override
     */
    function emergencyOverride(string calldata reason) external onlyOwner {
        VetoState previousState = currentState;
        currentState = VetoState.ACTIVE;
        
        emit StateChanged(previousState, VetoState.ACTIVE, reason);
    }

    /**
     * @notice Check if operations are allowed in current state
     * @return allowed True if operations are allowed
     */
    function operationsAllowed() external view returns (bool) {
        return currentState == VetoState.ACTIVE;
    }

    /**
     * @notice Check if a specific state allows operations
     * @return allowed True if state allows operations
     */
    function isActiveState() external view returns (bool) {
        return currentState == VetoState.ACTIVE;
    }

    /**
     * @notice Get total number of vetos in history
     * @return count Number of vetos
     */
    function getVetoCount() external view returns (uint256) {
        return vetoHistory.length;
    }

    /**
     * @notice Get veto ID by index
     * @param index Index in veto history
     * @return vetoId The veto identifier
     */
    function getVetoIdByIndex(uint256 index) external view returns (bytes32) {
        require(index < vetoHistory.length, "RedCodeVeto: Index out of bounds");
        return vetoHistory[index];
    }
}
