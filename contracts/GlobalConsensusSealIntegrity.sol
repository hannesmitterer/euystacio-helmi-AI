// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

/**
 * @title GlobalConsensusSealIntegrity
 * @notice Implements G-CSI for cryptographic validation of council actions
 * @dev Validates signatures from council members before critical governance operations
 */
contract GlobalConsensusSealIntegrity is Ownable {
    using ECDSA for bytes32;

    // Council structure
    struct CouncilMember {
        address memberAddress;
        string name;
        bool active;
        uint256 addedAt;
    }

    mapping(address => CouncilMember) public councilMembers;
    address[] public councilAddresses;
    uint256 public activeCouncilCount;

    // Seal structure for validated actions
    struct ConsensusSeal {
        bytes32 actionHash;
        address[] signers;
        mapping(address => bool) hasSigned;
        uint256 signatureCount;
        uint256 createdAt;
        bool executed;
        string metadata;
    }

    mapping(bytes32 => ConsensusSeal) public seals;
    bytes32[] public sealHistory;

    // Quorum requirements
    uint256 public quorumPercentage; // Out of 100
    uint256 public minimumSignatures;

    event CouncilMemberAdded(address indexed member, string name);
    event CouncilMemberRemoved(address indexed member);
    event CouncilMemberDeactivated(address indexed member);
    event SealCreated(bytes32 indexed sealId, bytes32 indexed actionHash, string metadata);
    event SealSigned(bytes32 indexed sealId, address indexed signer);
    event SealExecuted(bytes32 indexed sealId);
    event QuorumUpdated(uint256 percentage, uint256 minimumSignatures);

    modifier onlyActiveCouncil() {
        require(councilMembers[msg.sender].active, "G-CSI: Not an active council member");
        _;
    }

    constructor() {
        quorumPercentage = 51; // 51% default
        minimumSignatures = 1;
        
        // Add deployer as initial council member
        _addCouncilMember(msg.sender, "Deployer");
    }

    /**
     * @notice Add a new council member
     * @param member Address of the council member
     * @param name Human-readable name
     */
    function addCouncilMember(address member, string calldata name) external onlyOwner {
        _addCouncilMember(member, name);
    }

    /**
     * @notice Internal function to add council member
     */
    function _addCouncilMember(address member, string memory name) internal {
        require(member != address(0), "G-CSI: Invalid address");
        require(!councilMembers[member].active, "G-CSI: Already active member");
        
        councilMembers[member] = CouncilMember({
            memberAddress: member,
            name: name,
            active: true,
            addedAt: block.timestamp
        });
        
        councilAddresses.push(member);
        activeCouncilCount++;
        
        emit CouncilMemberAdded(member, name);
    }

    /**
     * @notice Deactivate a council member
     * @param member Address to deactivate
     */
    function deactivateCouncilMember(address member) external onlyOwner {
        require(councilMembers[member].active, "G-CSI: Not an active member");
        require(activeCouncilCount > minimumSignatures, "G-CSI: Cannot deactivate, would break quorum");
        
        councilMembers[member].active = false;
        activeCouncilCount--;
        
        emit CouncilMemberDeactivated(member);
    }

    /**
     * @notice Update quorum requirements
     * @param percentage Percentage of council required (out of 100)
     * @param minSignatures Minimum number of signatures regardless of percentage
     */
    function setQuorumRequirements(uint256 percentage, uint256 minSignatures) external onlyOwner {
        require(percentage > 0 && percentage <= 100, "G-CSI: Invalid percentage");
        require(minSignatures > 0, "G-CSI: Minimum must be at least 1");
        require(minSignatures <= activeCouncilCount, "G-CSI: Min signatures exceeds council size");
        
        quorumPercentage = percentage;
        minimumSignatures = minSignatures;
        
        emit QuorumUpdated(percentage, minSignatures);
    }

    /**
     * @notice Create a new seal for an action requiring consensus
     * @param actionHash Hash of the action to be validated
     * @param metadata Human-readable description
     * @return sealId Unique identifier for this seal
     */
    function createSeal(bytes32 actionHash, string calldata metadata) external onlyActiveCouncil returns (bytes32) {
        require(actionHash != bytes32(0), "G-CSI: Invalid action hash");
        
        bytes32 sealId = keccak256(abi.encodePacked(actionHash, block.timestamp, msg.sender));
        
        ConsensusSeal storage newSeal = seals[sealId];
        newSeal.actionHash = actionHash;
        newSeal.createdAt = block.timestamp;
        newSeal.executed = false;
        newSeal.metadata = metadata;
        
        sealHistory.push(sealId);
        
        emit SealCreated(sealId, actionHash, metadata);
        
        // Creator automatically signs
        _signSeal(sealId, msg.sender);
        
        return sealId;
    }

    /**
     * @notice Sign an existing seal
     * @param sealId The seal to sign
     */
    function signSeal(bytes32 sealId) external onlyActiveCouncil {
        _signSeal(sealId, msg.sender);
    }

    /**
     * @notice Internal function to sign a seal
     */
    function _signSeal(bytes32 sealId, address signer) internal {
        ConsensusSeal storage seal = seals[sealId];
        require(seal.actionHash != bytes32(0), "G-CSI: Seal does not exist");
        require(!seal.executed, "G-CSI: Seal already executed");
        require(!seal.hasSigned[signer], "G-CSI: Already signed");
        
        seal.hasSigned[signer] = true;
        seal.signers.push(signer);
        seal.signatureCount++;
        
        emit SealSigned(sealId, signer);
    }

    /**
     * @notice Mark a seal as executed after quorum is reached
     * @param sealId The seal to execute
     */
    function executeSeal(bytes32 sealId) external onlyActiveCouncil {
        ConsensusSeal storage seal = seals[sealId];
        require(seal.actionHash != bytes32(0), "G-CSI: Seal does not exist");
        require(!seal.executed, "G-CSI: Already executed");
        require(hasQuorum(sealId), "G-CSI: Quorum not reached");
        
        seal.executed = true;
        
        emit SealExecuted(sealId);
    }

    /**
     * @notice Check if a seal has reached quorum
     * @param sealId The seal to check
     * @return reached True if quorum is reached
     * @dev Quorum calculation: percentage requirement is rounded down (e.g., 51% of 3 members = 1.53 = 1)
     *      The final requirement is the maximum of percentage-based and minimum signature requirements
     */
    function hasQuorum(bytes32 sealId) public view returns (bool) {
        ConsensusSeal storage seal = seals[sealId];
        
        if (seal.actionHash == bytes32(0)) {
            return false;
        }
        
        // Must meet both percentage and minimum requirements
        uint256 requiredByPercentage = (activeCouncilCount * quorumPercentage) / 100;
        uint256 required = requiredByPercentage > minimumSignatures ? requiredByPercentage : minimumSignatures;
        
        return seal.signatureCount >= required;
    }

    /**
     * @notice Verify if a seal is valid and executed
     * @param sealId The seal to verify
     * @return valid True if seal is valid and executed
     */
    function verifySeal(bytes32 sealId) external view returns (bool) {
        ConsensusSeal storage seal = seals[sealId];
        return seal.actionHash != bytes32(0) && seal.executed && hasQuorum(sealId);
    }

    /**
     * @notice Get the number of signatures on a seal
     * @param sealId The seal to query
     * @return count Number of signatures
     */
    function getSignatureCount(bytes32 sealId) external view returns (uint256) {
        return seals[sealId].signatureCount;
    }

    /**
     * @notice Get signers of a seal
     * @param sealId The seal to query
     * @return signers Array of addresses that signed
     */
    function getSigners(bytes32 sealId) external view returns (address[] memory) {
        return seals[sealId].signers;
    }

    /**
     * @notice Check if an address has signed a seal
     * @param sealId The seal to check
     * @param signer The address to check
     * @return signed True if address has signed
     */
    function hasSigned(bytes32 sealId, address signer) external view returns (bool) {
        return seals[sealId].hasSigned[signer];
    }

    /**
     * @notice Get total number of seals
     * @return count Number of seals in history
     */
    function getSealCount() external view returns (uint256) {
        return sealHistory.length;
    }

    /**
     * @notice Get seal ID by index
     * @param index Index in seal history
     * @return sealId The seal identifier
     */
    function getSealIdByIndex(uint256 index) external view returns (bytes32) {
        require(index < sealHistory.length, "G-CSI: Index out of bounds");
        return sealHistory[index];
    }

    /**
     * @notice Calculate current quorum requirement
     * @return required Number of signatures required for quorum
     */
    function getCurrentQuorumRequirement() external view returns (uint256) {
        uint256 requiredByPercentage = (activeCouncilCount * quorumPercentage) / 100;
        return requiredByPercentage > minimumSignatures ? requiredByPercentage : minimumSignatures;
    }
}
