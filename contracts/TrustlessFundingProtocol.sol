// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

interface ISustainment {
    function isAboveMinimum() external view returns (bool);
    function getSustainmentReserve() external view returns (uint256);
    function minSustainment() external view returns (uint256);
}

/**
 * @title TrustlessFundingProtocol
 * @notice Governance contract for trustless funding with sustainment enforcement
 * @dev Enforces minimum sustainment threshold before releasing tranches
 * 
 * ETHICAL FRAMEWORK - Cosimbiosi Basis Fundamentum in Eternuum:
 * - Transparency: All funding decisions are recorded on-chain with proofHash
 * - Collaborative Governance: Decisions respect collective sustainability requirements
 * - Individual Autonomy: Owner can override governance in emergencies (setGovernanceEnforcement)
 * - Zero-Obligation Override: Emergency bypass mechanism honors NRE-002 principle
 * - Sustainable Harmony: Enforces minimum reserves for ecosystem continuity
 * - Accessible Verification: Public view functions (canReleaseTranche) enable transparency
 * 
 * USER CONTROL MECHANISMS:
 * - governanceEnforced flag allows emergency bypass of automated checks
 * - Public view functions provide transparency before actions
 * - Event logging ensures full audit trail
 */
contract TrustlessFundingProtocol is Ownable {
    address public foundationWallet;
    ISustainment public sustainmentContract;
    
    mapping(uint256 => bool) public trancheReleased;
    
    /// @notice Whether governance checks are enforced (can be disabled by owner in emergency)
    bool public governanceEnforced;
    
    event TrancheReleased(uint256 indexed trancheId, bytes32 proofHash, uint256 timestamp);
    event SustainmentContractUpdated(address indexed previous, address indexed current);
    event GovernanceEnforcementToggled(bool enforced);
    event TrancheRejectedInsufficientSustainment(uint256 indexed trancheId, uint256 currentReserve, uint256 minRequired);

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
     * @notice Toggle governance enforcement (emergency override)
     * @param enforced True to enforce, false to disable
     */
    function setGovernanceEnforcement(bool enforced) external onlyOwner {
        governanceEnforced = enforced;
        emit GovernanceEnforcementToggled(enforced);
    }

    /**
     * @notice Release tranche when proofHash submitted and sustainment requirements met
     * @param trancheId ID of the tranche to release
     * @param proofHash Hash of proof (stored off-chain)
     */
    function releaseTranche(uint256 trancheId, bytes32 proofHash) external onlyOwner {
        require(!trancheReleased[trancheId], "Already released");
        require(proofHash != bytes32(0), "Invalid proof");
        
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
        
        if (governanceEnforced && address(sustainmentContract) != address(0)) {
            if (!sustainmentContract.isAboveMinimum()) {
                return (false, "Sustainment below minimum");
            }
        }
        
        return (true, "");
    }
}
