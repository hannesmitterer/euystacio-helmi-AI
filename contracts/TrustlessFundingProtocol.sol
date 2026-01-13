// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

interface ISustainment {
    function isAboveMinimum() external view returns (bool);
    function getSustainmentReserve() external view returns (uint256);
    function minSustainment() external view returns (uint256);
}

interface IRedCodeVeto {
    function operationsAllowed() external view returns (bool);
    function isActiveState() external view returns (bool);
}

interface IGlobalConsensusSealIntegrity {
    function verifySeal(bytes32 sealId) external view returns (bool);
    function hasQuorum(bytes32 sealId) external view returns (bool);
}

interface ILivingCovenantAnchor {
    function createMilestone(string calldata description, bytes32 actionHash, bytes32 covenantReference) external returns (bytes32);
    function createAnchor(bytes32 milestoneId, string calldata anchorType, bytes32 contentHash) external returns (bytes32);
    function sealMilestone(bytes32 milestoneId, bytes32 finalAnchorHash) external;
    function isMilestoneSealed(bytes32 milestoneId) external view returns (bool);
}

/**
 * @title TrustlessFundingProtocol
 * @notice Governance contract for trustless funding with sustainment enforcement
 * @dev Enforces minimum sustainment threshold before releasing tranches
 */
contract TrustlessFundingProtocol is Ownable {
    address public foundationWallet;
    ISustainment public sustainmentContract;
    IRedCodeVeto public redCodeVeto;
    IGlobalConsensusSealIntegrity public gCSI;
    ILivingCovenantAnchor public livingCovenantAnchor;
    
    mapping(uint256 => bool) public trancheReleased;
    mapping(uint256 => bytes32) public trancheMilestones;
    mapping(uint256 => bytes32) public trancheSeals;
    
    /// @notice Whether governance checks are enforced (can be disabled by owner in emergency)
    bool public governanceEnforced;
    
    event TrancheReleased(uint256 indexed trancheId, bytes32 proofHash, uint256 timestamp);
    event SustainmentContractUpdated(address indexed previous, address indexed current);
    event GovernanceEnforcementToggled(bool enforced);
    event TrancheRejectedInsufficientSustainment(uint256 indexed trancheId, uint256 currentReserve, uint256 minRequired);
    event RedCodeVetoUpdated(address indexed previous, address indexed current);
    event GCSIUpdated(address indexed previous, address indexed current);
    event LivingCovenantAnchorUpdated(address indexed previous, address indexed current);
    event TrancheVetoed(uint256 indexed trancheId, string reason);
    event TrancheSealRequired(uint256 indexed trancheId, bytes32 sealId);
    event MilestoneCreatedForTranche(uint256 indexed trancheId, bytes32 milestoneId);

    constructor(address _foundationWallet) {
        foundationWallet = _foundationWallet;
        governanceEnforced = true; // Default to enforced
    }

    /**
     * @notice Set the sustainment contract address
     * @param _sustainmentContract Address of Sustainment contract
     */
    function setSustainmentContract(address _sustainmentContract) external onlyOwner {
        address previous = address(sustainmentContract);
        sustainmentContract = ISustainment(_sustainmentContract);
        emit SustainmentContractUpdated(previous, _sustainmentContract);
    }

    /**
     * @notice Set the Red Code Veto contract address
     * @param _redCodeVeto Address of Red Code Veto contract
     */
    function setRedCodeVeto(address _redCodeVeto) external onlyOwner {
        address previous = address(redCodeVeto);
        redCodeVeto = IRedCodeVeto(_redCodeVeto);
        emit RedCodeVetoUpdated(previous, _redCodeVeto);
    }

    /**
     * @notice Set the G-CSI contract address
     * @param _gCSI Address of Global Consensus Seal Integrity contract
     */
    function setGCSI(address _gCSI) external onlyOwner {
        address previous = address(gCSI);
        gCSI = IGlobalConsensusSealIntegrity(_gCSI);
        emit GCSIUpdated(previous, _gCSI);
    }

    /**
     * @notice Set the Living Covenant Anchor contract address
     * @param _anchor Address of Living Covenant Anchor contract
     */
    function setLivingCovenantAnchor(address _anchor) external onlyOwner {
        address previous = address(livingCovenantAnchor);
        livingCovenantAnchor = ILivingCovenantAnchor(_anchor);
        emit LivingCovenantAnchorUpdated(previous, _anchor);
    }

    /**
     * @notice Toggle governance enforcement (emergency override)
     * @param enforced True to enforce, false to disable
     */
    function setGovernanceEnforcement(bool enforced) external onlyOwner {
        governanceEnforced = enforced;
        emit GovernanceEnforcementToggled(enforced);
    }

    /**
     * @notice Release tranche when proofHash submitted and all requirements met
     * @param trancheId ID of the tranche to release
     * @param proofHash Hash of proof (stored off-chain)
     * @param sealId G-CSI seal ID for this tranche (optional, bytes32(0) if not required)
     */
    function releaseTranche(uint256 trancheId, bytes32 proofHash, bytes32 sealId) external onlyOwner {
        require(!trancheReleased[trancheId], "Already released");
        require(proofHash != bytes32(0), "Invalid proof");
        
        // Red Code Veto H-Var check
        if (governanceEnforced && address(redCodeVeto) != address(0)) {
            require(redCodeVeto.operationsAllowed(), "Red Code Veto: Operations not allowed");
        }
        
        // G-CSI validation check
        if (governanceEnforced && address(gCSI) != address(0) && sealId != bytes32(0)) {
            require(gCSI.verifySeal(sealId), "G-CSI: Seal not verified or executed");
            trancheSeals[trancheId] = sealId;
        }
        
        // Check sustainment requirements if enforcement is enabled
        if (governanceEnforced && address(sustainmentContract) != address(0)) {
            bool aboveMin = sustainmentContract.isAboveMinimum();
            if (!aboveMin) {
                uint256 currentReserve = sustainmentContract.getSustainmentReserve();
                uint256 minRequired = sustainmentContract.minSustainment();
                emit TrancheRejectedInsufficientSustainment(trancheId, currentReserve, minRequired);
                revert("Sustainment below minimum");
            }
        }
        
        // Create and seal milestone in Living Covenant Anchor
        if (address(livingCovenantAnchor) != address(0)) {
            bytes32 milestoneId = livingCovenantAnchor.createMilestone(
                string(abi.encodePacked("Tranche ", _uint2str(trancheId), " release")),
                proofHash,
                keccak256(abi.encodePacked("TRANCHE_RELEASE"))
            );
            trancheMilestones[trancheId] = milestoneId;
            
            bytes32 anchorHash = livingCovenantAnchor.createAnchor(
                milestoneId,
                "governance",
                proofHash
            );
            
            livingCovenantAnchor.sealMilestone(milestoneId, anchorHash);
            emit MilestoneCreatedForTranche(trancheId, milestoneId);
        }
        
        trancheReleased[trancheId] = true;
        emit TrancheReleased(trancheId, proofHash, block.timestamp);
    }

    /**
     * @notice Check if a tranche can be released (view function for frontend)
     * @param trancheId ID of the tranche
     * @return canRelease True if tranche can be released
     * @return reason Reason if cannot release
     */
    function canReleaseTranche(uint256 trancheId) external view returns (bool canRelease, string memory reason) {
        if (trancheReleased[trancheId]) {
            return (false, "Already released");
        }
        
        // Check Red Code Veto
        if (governanceEnforced && address(redCodeVeto) != address(0)) {
            if (!redCodeVeto.operationsAllowed()) {
                return (false, "Red Code Veto active");
            }
        }
        
        // Check sustainment
        if (governanceEnforced && address(sustainmentContract) != address(0)) {
            if (!sustainmentContract.isAboveMinimum()) {
                return (false, "Sustainment below minimum");
            }
        }
        
        return (true, "");
    }

    /**
     * @notice Get milestone ID for a tranche
     * @param trancheId The tranche ID
     * @return milestoneId The associated milestone ID
     */
    function getTrancheMilestone(uint256 trancheId) external view returns (bytes32) {
        return trancheMilestones[trancheId];
    }

    /**
     * @notice Get seal ID for a tranche
     * @param trancheId The tranche ID
     * @return sealId The associated seal ID
     */
    function getTrancheSeal(uint256 trancheId) external view returns (bytes32) {
        return trancheSeals[trancheId];
    }

    /**
     * @notice Internal helper to convert uint to string
     */
    function _uint2str(uint256 _i) internal pure returns (string memory) {
        if (_i == 0) {
            return "0";
        }
        uint256 j = _i;
        uint256 len;
        while (j != 0) {
            len++;
            j /= 10;
        }
        bytes memory bstr = new bytes(len);
        uint256 k = len;
        while (_i != 0) {
            k = k-1;
            uint8 temp = (48 + uint8(_i - _i / 10 * 10));
            bytes1 b1 = bytes1(temp);
            bstr[k] = b1;
            _i /= 10;
        }
        return string(bstr);
    }
}
