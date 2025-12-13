// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title TFKVerifier
 * @dev Smart contract for on-chain verification of Tuttifruttikarma (TFK) integrity
 * Validates the integrity between on-chain TFK records and off-chain CID (Content ID) data
 */
contract TFKVerifier {
    
    struct IntegrityRecord {
        bytes32 tfkHash;        // TFK on-chain hash
        string cidReference;    // IPFS/CID off-chain reference
        uint256 timestamp;      // Verification timestamp
        address verifier;       // Address that performed verification
        bool isValid;          // Integrity status
    }
    
    // Mapping from record ID to IntegrityRecord
    mapping(uint256 => IntegrityRecord) public integrityRecords;
    
    // Current record counter
    uint256 public recordCount;
    
    // Authorized verifiers
    mapping(address => bool) public authorizedVerifiers;
    
    // Owner of the contract
    address public owner;
    
    // Events
    event IntegrityRecorded(
        uint256 indexed recordId,
        bytes32 tfkHash,
        string cidReference,
        uint256 timestamp,
        bool isValid
    );
    
    event VerifierAuthorized(address indexed verifier, bool status);
    event IntegrityViolationDetected(uint256 indexed recordId, bytes32 tfkHash, string cidReference);
    
    modifier onlyOwner() {
        require(msg.sender == owner, "TFKVerifier: caller is not the owner");
        _;
    }
    
    modifier onlyAuthorized() {
        require(authorizedVerifiers[msg.sender] || msg.sender == owner, "TFKVerifier: caller is not authorized");
        _;
    }
    
    constructor() {
        owner = msg.sender;
        authorizedVerifiers[msg.sender] = true;
    }
    
    /**
     * @dev Authorize or revoke a verifier
     * @param verifier Address to authorize/revoke
     * @param status Authorization status
     */
    function setAuthorizedVerifier(address verifier, bool status) external onlyOwner {
        require(verifier != address(0), "TFKVerifier: invalid verifier address");
        authorizedVerifiers[verifier] = status;
        emit VerifierAuthorized(verifier, status);
    }
    
    /**
     * @dev Record an integrity check result
     * @param tfkHash On-chain TFK hash
     * @param cidReference Off-chain CID reference
     * @param isValid Whether the integrity check passed
     * @return recordId The ID of the created record
     */
    function recordIntegrityCheck(
        bytes32 tfkHash,
        string memory cidReference,
        bool isValid
    ) external onlyAuthorized returns (uint256) {
        require(tfkHash != bytes32(0), "TFKVerifier: invalid TFK hash");
        require(bytes(cidReference).length > 0, "TFKVerifier: invalid CID reference");
        
        uint256 recordId = recordCount++;
        
        integrityRecords[recordId] = IntegrityRecord({
            tfkHash: tfkHash,
            cidReference: cidReference,
            timestamp: block.timestamp,
            verifier: msg.sender,
            isValid: isValid
        });
        
        emit IntegrityRecorded(recordId, tfkHash, cidReference, block.timestamp, isValid);
        
        if (!isValid) {
            emit IntegrityViolationDetected(recordId, tfkHash, cidReference);
        }
        
        return recordId;
    }
    
    /**
     * @dev Batch record multiple integrity checks
     * @param tfkHashes Array of TFK hashes
     * @param cidReferences Array of CID references
     * @param validityFlags Array of validity flags
     * @return recordIds Array of created record IDs
     */
    function batchRecordIntegrityChecks(
        bytes32[] memory tfkHashes,
        string[] memory cidReferences,
        bool[] memory validityFlags
    ) external onlyAuthorized returns (uint256[] memory) {
        require(
            tfkHashes.length == cidReferences.length && 
            tfkHashes.length == validityFlags.length,
            "TFKVerifier: array length mismatch"
        );
        require(tfkHashes.length > 0, "TFKVerifier: empty arrays");
        require(tfkHashes.length <= 100, "TFKVerifier: batch size too large");
        
        uint256[] memory recordIds = new uint256[](tfkHashes.length);
        
        for (uint256 i = 0; i < tfkHashes.length; i++) {
            require(tfkHashes[i] != bytes32(0), "TFKVerifier: invalid TFK hash");
            require(bytes(cidReferences[i]).length > 0, "TFKVerifier: invalid CID reference");
            
            uint256 recordId = recordCount++;
            
            integrityRecords[recordId] = IntegrityRecord({
                tfkHash: tfkHashes[i],
                cidReference: cidReferences[i],
                timestamp: block.timestamp,
                verifier: msg.sender,
                isValid: validityFlags[i]
            });
            
            emit IntegrityRecorded(recordId, tfkHashes[i], cidReferences[i], block.timestamp, validityFlags[i]);
            
            if (!validityFlags[i]) {
                emit IntegrityViolationDetected(recordId, tfkHashes[i], cidReferences[i]);
            }
            
            recordIds[i] = recordId;
        }
        
        return recordIds;
    }
    
    /**
     * @dev Get integrity record by ID
     * @param recordId The record ID to query
     * @return IntegrityRecord struct
     */
    function getIntegrityRecord(uint256 recordId) 
        external 
        view 
        returns (IntegrityRecord memory) 
    {
        require(recordId < recordCount, "TFKVerifier: invalid record ID");
        return integrityRecords[recordId];
    }
    
    /**
     * @dev Get recent integrity records
     * @param count Number of recent records to retrieve
     * @return Array of IntegrityRecord structs
     */
    function getRecentIntegrityRecords(uint256 count) 
        external 
        view 
        returns (IntegrityRecord[] memory) 
    {
        if (count > recordCount) {
            count = recordCount;
        }
        
        IntegrityRecord[] memory records = new IntegrityRecord[](count);
        uint256 startIndex = recordCount - count;
        
        for (uint256 i = 0; i < count; i++) {
            records[i] = integrityRecords[startIndex + i];
        }
        
        return records;
    }
    
    /**
     * @dev Check if a specific TFK hash has valid integrity
     * @param tfkHash The TFK hash to check
     * @return bool Whether the most recent record for this hash is valid
     */
    function hasValidIntegrity(bytes32 tfkHash) external view returns (bool) {
        // Search backwards for the most recent record with this hash
        for (uint256 i = recordCount; i > 0; i--) {
            uint256 recordId = i - 1;
            if (integrityRecords[recordId].tfkHash == tfkHash) {
                return integrityRecords[recordId].isValid;
            }
        }
        return false;
    }
    
    /**
     * @dev Get count of integrity violations in a time range
     * @param startTime Start timestamp
     * @param endTime End timestamp
     * @return violationCount Number of violations in the range
     */
    function getViolationCount(uint256 startTime, uint256 endTime) 
        external 
        view 
        returns (uint256 violationCount) 
    {
        require(startTime <= endTime, "TFKVerifier: invalid time range");
        
        for (uint256 i = 0; i < recordCount; i++) {
            IntegrityRecord memory record = integrityRecords[i];
            if (record.timestamp >= startTime && 
                record.timestamp <= endTime && 
                !record.isValid) {
                violationCount++;
            }
        }
        
        return violationCount;
    }
}
