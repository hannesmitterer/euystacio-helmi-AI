// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/// @title EuystacioSTAnchor v1.0
/// @notice Minimaler, auditierbarer Anchor-Contract zur Versiegelung von Core-Metriken.
/// @dev Dieses Template ist auf Einfachheit, Auditierbarkeit und Witness-Integration ausgelegt.

contract EuystacioSTAnchor {
    address public admin;
    bytes32 public rootCommit; // ROOT-ETERNAL-C48B2A7 -> keccak256("ROOT-ETERNAL-C48B2A7")
    uint256 public anchorCount;

    struct Anchor {
        bytes32 metricsHash;    // keccak256(JSON metrics)
        string metadataURI;     // optional: IPFS/ystFS pointer
        uint256 timestamp;
        address submitter;
        bytes witnessSig;       // ECDSA signature by Witness engine / signer
        bool verified;
    }

    mapping(uint256 => Anchor) public anchors;

    // Council quorum requirement (basic form)
    mapping(address => bool) public council;
    uint8 public councilQuorum; // minimal number of council confirmations needed

    event Anchored(uint256 indexed id, bytes32 metricsHash, address indexed submitter);
    event Verified(uint256 indexed id, address indexed verifier);
    event QuorumReached(uint256 indexed id, uint8 confirmations);

    modifier onlyAdmin() {
        require(msg.sender == admin, "not admin");
        _;
    }

    constructor(bytes32 _rootCommit, address[] memory _council, uint8 _quorum) {
        require(_quorum > 0, "quorum must be positive");
        require(_council.length >= _quorum, "council size must meet quorum");
        admin = msg.sender;
        rootCommit = _rootCommit;
        councilQuorum = _quorum;
        for (uint i = 0; i < _council.length; i++) {
            require(_council[i] != address(0), "invalid council address");
            council[_council[i]] = true;
        }
    }

    /// @notice Submit an anchor with precomputed metricsHash and optional metadata pointer
    function submitAnchor(bytes32 metricsHash, string calldata metadataURI, bytes calldata witnessSig) external returns (uint256) {
        anchorCount += 1;
        anchors[anchorCount] = Anchor({
            metricsHash: metricsHash,
            metadataURI: metadataURI,
            timestamp: block.timestamp,
            submitter: msg.sender,
            witnessSig: witnessSig,
            verified: false
        });
        emit Anchored(anchorCount, metricsHash, msg.sender);
        return anchorCount;
    }

    /// @notice Council verification step - each council member calls to mark verified.
    mapping(uint256 => mapping(address => bool)) public confirmations;
    mapping(uint256 => uint8) public confirmationCount;

    function confirmAnchor(uint256 id) external {
        require(council[msg.sender], "not council");
        require(anchors[id].submitter != address(0), "no anchor");
        require(!confirmations[id][msg.sender], "already confirmed");
        require(!anchors[id].verified, "already verified");
        confirmations[id][msg.sender] = true;
        confirmationCount[id] += 1;
        if (confirmationCount[id] >= councilQuorum) {
            anchors[id].verified = true;
            emit Verified(id, msg.sender);
            emit QuorumReached(id, confirmationCount[id]);
        }
    }

    /// @notice Get anchor data (view)
    function getAnchor(uint256 id) external view returns (Anchor memory) {
        return anchors[id];
    }

    /// @notice Administrative function to update council (only admin)
    function setCouncilMember(address member, bool allowed) external onlyAdmin {
        council[member] = allowed;
    }

    /// @notice Emergency function to set root commit (only admin) — logged for audit
    function setRootCommit(bytes32 newRoot) external onlyAdmin {
        rootCommit = newRoot;
    }
}
