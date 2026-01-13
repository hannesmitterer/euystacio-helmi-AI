// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title EuystacioSTAnchor
 * @notice Governance smart contract with Red Code Veto H-Var capabilities
 * @dev Implements immutable ethical principles and deployment sealing
 */
contract EuystacioSTAnchor is Ownable {
    
    // ==================== State Variables ====================
    
    /// @notice Immutable Red Code Veto authority (Human Variable)
    address public immutable redCodeVetoAuthority;
    
    /// @notice Deployment sealed status - once true, cannot be changed
    bool public deploymentSealed;
    
    /// @notice Governance state locked status
    bool public governanceStateLocked;
    
    /// @notice IPFS CID for Red Code ethical framework
    string public redCodeIPFSCID;
    
    /// @notice IPFS CID for G-CSI anchoring graph
    string public gcsiAnchoringGraphCID;
    
    /// @notice Locked deployment keys registry
    mapping(bytes32 => DeploymentKey) public deploymentKeys;
    
    /// @notice Locked runtime parameters registry
    mapping(bytes32 => RuntimeParameter) public runtimeParameters;
    
    /// @notice IPFS-backed governance documents
    mapping(bytes32 => GovernanceDocument) public governanceDocuments;
    
    /// @notice Authorized governance contracts that can invoke Red Code Veto
    mapping(address => bool) public authorizedGovernanceContracts;
    
    // ==================== Structs ====================
    
    struct DeploymentKey {
        string name;
        bytes32 keyHash;
        bool locked;
        uint256 lockedAt;
        string ipfsCID;
    }
    
    struct RuntimeParameter {
        string name;
        bytes32 valueHash;
        bool locked;
        uint256 lockedAt;
        string description;
    }
    
    struct GovernanceDocument {
        string name;
        string ipfsCID;
        bytes32 contentHash;
        uint256 timestamp;
        bool validated;
    }
    
    // ==================== Events ====================
    
    event DeploymentSealed(uint256 timestamp, address sealedBy);
    event GovernanceStateLocked(uint256 timestamp, address lockedBy);
    event RedCodeVetoInvoked(address invoker, string reason, uint256 timestamp);
    event DeploymentKeyRegistered(bytes32 indexed keyId, string name, string ipfsCID);
    event DeploymentKeyLocked(bytes32 indexed keyId, uint256 timestamp);
    event RuntimeParameterSet(bytes32 indexed paramId, string name, bytes32 valueHash);
    event RuntimeParameterLocked(bytes32 indexed paramId, uint256 timestamp);
    event GovernanceDocumentAnchored(bytes32 indexed docId, string ipfsCID, bytes32 contentHash);
    event GCSIAnchoringGraphUpdated(string ipfsCID, uint256 timestamp);
    event RedCodeIPFSUpdated(string ipfsCID, uint256 timestamp);
    event GovernanceContractAuthorized(address indexed govContract, bool authorized);
    
    // ==================== Modifiers ====================
    
    modifier onlyRedCodeVetoAuthority() {
        require(msg.sender == redCodeVetoAuthority, "Only Red Code Veto Authority");
        _;
    }
    
    modifier whenNotSealed() {
        require(!deploymentSealed, "Deployment is sealed");
        _;
    }
    
    modifier whenNotGovernanceLocked() {
        require(!governanceStateLocked, "Governance state is locked");
        _;
    }
    
    // ==================== Constructor ====================
    
    constructor(address _redCodeVetoAuthority) {
        require(_redCodeVetoAuthority != address(0), "Invalid veto authority");
        redCodeVetoAuthority = _redCodeVetoAuthority;
    }
    
    // ==================== Red Code Veto Functions ====================
    
    /**
     * @notice Invoke Red Code Veto - ultimate ethical override (H-Var)
     * @dev Can be called by Red Code Veto Authority or authorized governance contracts
     * @param reason The ethical reason for invoking the veto
     */
    function invokeRedCodeVeto(string calldata reason) external {
        require(
            msg.sender == redCodeVetoAuthority || authorizedGovernanceContracts[msg.sender],
            "Only Red Code Veto Authority or authorized governance"
        );
        emit RedCodeVetoInvoked(msg.sender, reason, block.timestamp);
        // Additional veto logic can be implemented here based on specific requirements
    }
    
    /**
     * @notice Set Red Code IPFS CID for ethical framework reference
     * @param ipfsCID The IPFS CID containing the Red Code ethical framework
     */
    function setRedCodeIPFS(string calldata ipfsCID) external onlyRedCodeVetoAuthority whenNotSealed {
        require(bytes(ipfsCID).length > 0, "Invalid IPFS CID");
        redCodeIPFSCID = ipfsCID;
        emit RedCodeIPFSUpdated(ipfsCID, block.timestamp);
    }
    
    /**
     * @notice Authorize or deauthorize a governance contract to invoke Red Code Veto
     * @param govContract Address of the governance contract
     * @param authorized Whether to authorize or deauthorize
     */
    function setAuthorizedGovernanceContract(address govContract, bool authorized) external onlyOwner {
        require(govContract != address(0), "Invalid governance contract");
        authorizedGovernanceContracts[govContract] = authorized;
        emit GovernanceContractAuthorized(govContract, authorized);
    }
    
    // ==================== Deployment Sealing Functions ====================
    
    /**
     * @notice Seal the deployment - irreversible action
     * @dev Once sealed, no further configuration changes are allowed
     */
    function sealDeployment() external onlyOwner whenNotSealed {
        deploymentSealed = true;
        emit DeploymentSealed(block.timestamp, msg.sender);
    }
    
    /**
     * @notice Lock governance state - irreversible action
     * @dev Once locked, governance parameters become immutable
     */
    function lockGovernanceState() external onlyOwner whenNotGovernanceLocked {
        governanceStateLocked = true;
        emit GovernanceStateLocked(block.timestamp, msg.sender);
    }
    
    // ==================== Deployment Key Management ====================
    
    /**
     * @notice Register a deployment key with IPFS backing
     * @param keyId Unique identifier for the key
     * @param name Human-readable name of the key
     * @param keyHash Hash of the key for verification
     * @param ipfsCID IPFS CID containing key documentation
     */
    function registerDeploymentKey(
        bytes32 keyId,
        string calldata name,
        bytes32 keyHash,
        string calldata ipfsCID
    ) external onlyOwner whenNotSealed {
        require(deploymentKeys[keyId].lockedAt == 0, "Key already exists");
        require(bytes(name).length > 0, "Invalid name");
        require(keyHash != bytes32(0), "Invalid key hash");
        
        deploymentKeys[keyId] = DeploymentKey({
            name: name,
            keyHash: keyHash,
            locked: false,
            lockedAt: 0,
            ipfsCID: ipfsCID
        });
        
        emit DeploymentKeyRegistered(keyId, name, ipfsCID);
    }
    
    /**
     * @notice Lock a deployment key - irreversible action
     * @param keyId The key identifier to lock
     */
    function lockDeploymentKey(bytes32 keyId) external onlyOwner {
        require(deploymentKeys[keyId].lockedAt != 0 || bytes(deploymentKeys[keyId].name).length > 0, "Key does not exist");
        require(!deploymentKeys[keyId].locked, "Key already locked");
        
        deploymentKeys[keyId].locked = true;
        deploymentKeys[keyId].lockedAt = block.timestamp;
        
        emit DeploymentKeyLocked(keyId, block.timestamp);
    }
    
    // ==================== Runtime Parameter Management ====================
    
    /**
     * @notice Set a runtime parameter
     * @param paramId Unique identifier for the parameter
     * @param name Human-readable name of the parameter
     * @param valueHash Hash of the parameter value
     * @param description Description of the parameter
     */
    function setRuntimeParameter(
        bytes32 paramId,
        string calldata name,
        bytes32 valueHash,
        string calldata description
    ) external onlyOwner whenNotGovernanceLocked {
        require(!runtimeParameters[paramId].locked, "Parameter is locked");
        require(bytes(name).length > 0, "Invalid name");
        require(valueHash != bytes32(0), "Invalid value hash");
        
        runtimeParameters[paramId] = RuntimeParameter({
            name: name,
            valueHash: valueHash,
            locked: false,
            lockedAt: 0,
            description: description
        });
        
        emit RuntimeParameterSet(paramId, name, valueHash);
    }
    
    /**
     * @notice Lock a runtime parameter - irreversible action
     * @param paramId The parameter identifier to lock
     */
    function lockRuntimeParameter(bytes32 paramId) external onlyOwner {
        require(runtimeParameters[paramId].lockedAt != 0 || bytes(runtimeParameters[paramId].name).length > 0, "Parameter does not exist");
        require(!runtimeParameters[paramId].locked, "Parameter already locked");
        
        runtimeParameters[paramId].locked = true;
        runtimeParameters[paramId].lockedAt = block.timestamp;
        
        emit RuntimeParameterLocked(paramId, block.timestamp);
    }
    
    // ==================== G-CSI IPFS Anchoring Functions ====================
    
    /**
     * @notice Anchor a governance document with IPFS backing and cryptographic validation
     * @param docId Unique identifier for the document
     * @param name Human-readable name of the document
     * @param ipfsCID IPFS CID of the document
     * @param contentHash Cryptographic hash of the document content for validation
     */
    function anchorGovernanceDocument(
        bytes32 docId,
        string calldata name,
        string calldata ipfsCID,
        bytes32 contentHash
    ) external onlyOwner whenNotSealed {
        require(bytes(ipfsCID).length > 0, "Invalid IPFS CID");
        require(contentHash != bytes32(0), "Invalid content hash");
        require(bytes(name).length > 0, "Invalid name");
        
        governanceDocuments[docId] = GovernanceDocument({
            name: name,
            ipfsCID: ipfsCID,
            contentHash: contentHash,
            timestamp: block.timestamp,
            validated: false
        });
        
        emit GovernanceDocumentAnchored(docId, ipfsCID, contentHash);
    }
    
    /**
     * @notice Validate a governance document's cryptographic hash
     * @param docId The document identifier to validate
     */
    function validateGovernanceDocument(bytes32 docId) external onlyOwner {
        require(governanceDocuments[docId].timestamp != 0, "Document does not exist");
        require(!governanceDocuments[docId].validated, "Document already validated");
        
        governanceDocuments[docId].validated = true;
    }
    
    /**
     * @notice Update G-CSI anchoring graph IPFS CID
     * @param ipfsCID The IPFS CID containing the complete G-CSI anchoring graph
     */
    function updateGCSIAnchoringGraph(string calldata ipfsCID) external onlyOwner whenNotSealed {
        require(bytes(ipfsCID).length > 0, "Invalid IPFS CID");
        gcsiAnchoringGraphCID = ipfsCID;
        emit GCSIAnchoringGraphUpdated(ipfsCID, block.timestamp);
    }
    
    // ==================== View Functions ====================
    
    /**
     * @notice Check if a deployment key is locked
     */
    function isDeploymentKeyLocked(bytes32 keyId) external view returns (bool) {
        return deploymentKeys[keyId].locked;
    }
    
    /**
     * @notice Check if a runtime parameter is locked
     */
    function isRuntimeParameterLocked(bytes32 paramId) external view returns (bool) {
        return runtimeParameters[paramId].locked;
    }
    
    /**
     * @notice Get deployment key details
     */
    function getDeploymentKey(bytes32 keyId) external view returns (
        string memory name,
        bytes32 keyHash,
        bool locked,
        uint256 lockedAt,
        string memory ipfsCID
    ) {
        DeploymentKey memory key = deploymentKeys[keyId];
        return (key.name, key.keyHash, key.locked, key.lockedAt, key.ipfsCID);
    }
    
    /**
     * @notice Get runtime parameter details
     */
    function getRuntimeParameter(bytes32 paramId) external view returns (
        string memory name,
        bytes32 valueHash,
        bool locked,
        uint256 lockedAt,
        string memory description
    ) {
        RuntimeParameter memory param = runtimeParameters[paramId];
        return (param.name, param.valueHash, param.locked, param.lockedAt, param.description);
    }
    
    /**
     * @notice Get governance document details
     */
    function getGovernanceDocument(bytes32 docId) external view returns (
        string memory name,
        string memory ipfsCID,
        bytes32 contentHash,
        uint256 timestamp,
        bool validated
    ) {
        GovernanceDocument memory doc = governanceDocuments[docId];
        return (doc.name, doc.ipfsCID, doc.contentHash, doc.timestamp, doc.validated);
    }
}
