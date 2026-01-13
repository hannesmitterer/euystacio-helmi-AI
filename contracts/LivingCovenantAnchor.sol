// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title LivingCovenantAnchor
 * @notice Implements the push-and-seal process to link governance milestones to the Living Covenant
 * @dev Creates immutable anchors for critical governance actions
 */
contract LivingCovenantAnchor is Ownable {
    // Milestone structure
    struct Milestone {
        bytes32 milestoneHash;
        string description;
        bytes32 covenantReference;
        bytes32 actionHash;
        address initiator;
        uint256 timestamp;
        bool isSealed;
        bytes32[] linkedAnchors;
    }

    // Immutable anchor structure
    struct ImmutableAnchor {
        bytes32 anchorHash;
        bytes32 milestoneId;
        string anchorType; // e.g., "governance", "covenant", "consensus"
        bytes32 contentHash;
        uint256 blockNumber;
        uint256 timestamp;
        bool permanent;
    }

    mapping(bytes32 => Milestone) public milestones;
    mapping(bytes32 => ImmutableAnchor) public anchors;
    mapping(address => bool) public authorizedSealers;
    
    bytes32[] public milestoneHistory;
    bytes32[] public anchorHistory;

    // Living Covenant metadata
    string public covenantURI;
    bytes32 public covenantRootHash;
    uint256 public lastCovenantUpdate;

    event MilestoneCreated(bytes32 indexed milestoneId, string description, address indexed initiator);
    event MilestoneSealed(bytes32 indexed milestoneId, bytes32 indexed anchorHash);
    event AnchorCreated(bytes32 indexed anchorHash, bytes32 indexed milestoneId, string anchorType);
    event CovenantUpdated(bytes32 indexed oldRoot, bytes32 indexed newRoot, string uri);
    event AnchorLinked(bytes32 indexed milestoneId, bytes32 indexed anchorHash);
    event AuthorizedSealerAdded(address indexed sealer);
    event AuthorizedSealerRemoved(address indexed sealer);

    modifier onlyAuthorizedSealer() {
        require(authorizedSealers[msg.sender] || msg.sender == owner(), "LCA: Not authorized");
        _;
    }

    constructor(string memory _covenantURI, bytes32 _covenantRootHash) {
        covenantURI = _covenantURI;
        covenantRootHash = _covenantRootHash;
        lastCovenantUpdate = block.timestamp;
        authorizedSealers[msg.sender] = true;
    }

    /**
     * @notice Authorize an address to seal milestones
     * @param sealer Address to authorize
     */
    function addAuthorizedSealer(address sealer) external onlyOwner {
        require(!authorizedSealers[sealer], "LCA: Already authorized");
        authorizedSealers[sealer] = true;
        emit AuthorizedSealerAdded(sealer);
    }

    /**
     * @notice Remove authorization from an address
     * @param sealer Address to deauthorize
     */
    function removeAuthorizedSealer(address sealer) external onlyOwner {
        require(authorizedSealers[sealer], "LCA: Not authorized");
        authorizedSealers[sealer] = false;
        emit AuthorizedSealerRemoved(sealer);
    }

    /**
     * @notice Create a new governance milestone
     * @param description Human-readable description of the milestone
     * @param actionHash Hash of the governance action
     * @param covenantReference Reference to relevant covenant section
     * @return milestoneId Unique identifier for the milestone
     */
    function createMilestone(
        string calldata description,
        bytes32 actionHash,
        bytes32 covenantReference
    ) external returns (bytes32) {
        require(bytes(description).length > 0, "LCA: Description required");
        require(actionHash != bytes32(0), "LCA: Invalid action hash");
        
        bytes32 milestoneId = keccak256(abi.encodePacked(
            description,
            actionHash,
            block.timestamp,
            msg.sender
        ));

        milestones[milestoneId] = Milestone({
            milestoneHash: milestoneId,
            description: description,
            covenantReference: covenantReference,
            actionHash: actionHash,
            initiator: msg.sender,
            timestamp: block.timestamp,
            isSealed: false,
            linkedAnchors: new bytes32[](0)
        });

        milestoneHistory.push(milestoneId);

        emit MilestoneCreated(milestoneId, description, msg.sender);

        return milestoneId;
    }

    /**
     * @notice Create an immutable anchor for a milestone
     * @param milestoneId The milestone to anchor
     * @param anchorType Type of anchor (e.g., "governance", "covenant")
     * @param contentHash Hash of the content being anchored
     * @return anchorHash Unique identifier for the anchor
     */
    function createAnchor(
        bytes32 milestoneId,
        string calldata anchorType,
        bytes32 contentHash
    ) external returns (bytes32) {
        require(milestones[milestoneId].milestoneHash != bytes32(0), "LCA: Milestone does not exist");
        require(contentHash != bytes32(0), "LCA: Invalid content hash");
        require(bytes(anchorType).length > 0, "LCA: Anchor type required");

        bytes32 anchorHash = keccak256(abi.encodePacked(
            milestoneId,
            anchorType,
            contentHash,
            block.number,
            block.timestamp
        ));

        anchors[anchorHash] = ImmutableAnchor({
            anchorHash: anchorHash,
            milestoneId: milestoneId,
            anchorType: anchorType,
            contentHash: contentHash,
            blockNumber: block.number,
            timestamp: block.timestamp,
            permanent: true
        });

        anchorHistory.push(anchorHash);

        emit AnchorCreated(anchorHash, milestoneId, anchorType);

        return anchorHash;
    }

    /**
     * @notice Link an anchor to a milestone
     * @param milestoneId The milestone to link to
     * @param anchorHash The anchor to link
     */
    function linkAnchor(bytes32 milestoneId, bytes32 anchorHash) external {
        require(milestones[milestoneId].milestoneHash != bytes32(0), "LCA: Milestone does not exist");
        require(anchors[anchorHash].anchorHash != bytes32(0), "LCA: Anchor does not exist");
        require(!milestones[milestoneId].isSealed, "LCA: Milestone already sealed");

        milestones[milestoneId].linkedAnchors.push(anchorHash);

        emit AnchorLinked(milestoneId, anchorHash);
    }

    /**
     * @notice Seal a milestone making it immutable
     * @param milestoneId The milestone to seal
     * @param finalAnchorHash Optional final anchor to create and link
     */
    function sealMilestone(bytes32 milestoneId, bytes32 finalAnchorHash) external onlyAuthorizedSealer {
        Milestone storage milestone = milestones[milestoneId];
        require(milestone.milestoneHash != bytes32(0), "LCA: Milestone does not exist");
        require(!milestone.isSealed, "LCA: Already sealed");

        milestone.isSealed = true;

        emit MilestoneSealed(milestoneId, finalAnchorHash);
    }

    /**
     * @notice Update the Living Covenant reference
     * @param newURI New URI for the covenant
     * @param newRootHash New root hash of the covenant
     */
    function updateCovenant(string calldata newURI, bytes32 newRootHash) external onlyOwner {
        require(bytes(newURI).length > 0, "LCA: URI required");
        require(newRootHash != bytes32(0), "LCA: Invalid root hash");

        bytes32 oldRoot = covenantRootHash;
        
        covenantURI = newURI;
        covenantRootHash = newRootHash;
        lastCovenantUpdate = block.timestamp;

        emit CovenantUpdated(oldRoot, newRootHash, newURI);
    }

    /**
     * @notice Verify if a milestone is sealed
     * @param milestoneId The milestone to check
     * @return sealed True if milestone is sealed
     */
    function isMilestoneSealed(bytes32 milestoneId) external view returns (bool) {
        return milestones[milestoneId].isSealed;
    }

    /**
     * @notice Get linked anchors for a milestone
     * @param milestoneId The milestone to query
     * @return anchors Array of anchor hashes
     */
    function getLinkedAnchors(bytes32 milestoneId) external view returns (bytes32[] memory) {
        return milestones[milestoneId].linkedAnchors;
    }

    /**
     * @notice Verify an anchor exists and is permanent
     * @param anchorHash The anchor to verify
     * @return valid True if anchor exists and is permanent
     */
    function verifyAnchor(bytes32 anchorHash) external view returns (bool) {
        ImmutableAnchor storage anchor = anchors[anchorHash];
        return anchor.anchorHash != bytes32(0) && anchor.permanent;
    }

    /**
     * @notice Get milestone count
     * @return count Number of milestones
     */
    function getMilestoneCount() external view returns (uint256) {
        return milestoneHistory.length;
    }

    /**
     * @notice Get anchor count
     * @return count Number of anchors
     */
    function getAnchorCount() external view returns (uint256) {
        return anchorHistory.length;
    }

    /**
     * @notice Get milestone ID by index
     * @param index Index in milestone history
     * @return milestoneId The milestone identifier
     */
    function getMilestoneIdByIndex(uint256 index) external view returns (bytes32) {
        require(index < milestoneHistory.length, "LCA: Index out of bounds");
        return milestoneHistory[index];
    }

    /**
     * @notice Get anchor hash by index
     * @param index Index in anchor history
     * @return anchorHash The anchor identifier
     */
    function getAnchorHashByIndex(uint256 index) external view returns (bytes32) {
        require(index < anchorHistory.length, "LCA: Index out of bounds");
        return anchorHistory[index];
    }

    /**
     * @notice Get current covenant information
     * @return uri The covenant URI
     * @return rootHash The covenant root hash
     * @return lastUpdate Timestamp of last update
     */
    function getCovenantInfo() external view returns (string memory uri, bytes32 rootHash, uint256 lastUpdate) {
        return (covenantURI, covenantRootHash, lastCovenantUpdate);
    }
}
