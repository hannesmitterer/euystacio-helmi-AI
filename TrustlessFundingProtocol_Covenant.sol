// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title TrustlessFundingProtocol_Covenant
 * @dev Enforces the Red Code, Trilogy Seal, and multi-tranche funding for ethical projects.
 * Funds are released only upon Euystacio-certified, HIL-verified milestone proof.
 */
contract TrustlessFundingProtocol_Covenant {
    
    // --- COVENANT SEAL HOLDERS (IMMUTABLE) ---
    // These addresses enforce the Trilogy Seal and Red Code Veto
    address public immutable EUYSTACIO_ORACLE_SEAL;
    address public immutable FONDAZIONE_RECIRCULATION_WALLET;

    // --- PROJECT STRUCTURE (EXPANDED FOR MULTI-TRANCHE) ---
    struct Project {
        address payable recipientHIL;
        uint256 totalBudget;
        uint256 releasedFunds;
        uint256 currentTrancheIndex;
        uint256[] trancheAmounts;
        bytes32[] expectedMilestoneHashes;
        bool isEthicallyCertified;
    }

    mapping(uint256 => Project) public projects;
    uint256 public projectCounter;

    // --- CONSTRUCTOR: ENSHRINING SEALS ---
    constructor(address _oracle, address _fondazione) {
        EUYSTACIO_ORACLE_SEAL = _oracle;
        FONDAZIONE_RECIRCULATION_WALLET = _fondazione;
    }

    // --- 1. INITIALIZATION (RESTRICTED BY ORACLE SEAL) ---
    function initializeProject(
        address payable _recipientHIL,
        uint256[] calldata _trancheAmounts,
        bytes32[] calldata _expectedHashes,
        bool _isEthicallyCertified
    ) public returns (uint256 projectId) {
        require(msg.sender == EUYSTACIO_ORACLE_SEAL, "RedCode Violation: Initialization restricted to Oracle.");
        require(_isEthicallyCertified, "RedCode Veto: Project lacks Ethical Certification.");
        require(_trancheAmounts.length == _expectedHashes.length, "Tranche and Hash arrays must match.");
        
        projectCounter++;
        projectId = projectCounter;
        
        uint256 totalBudget = 0;
        for (uint i = 0; i < _trancheAmounts.length; i++) {
            totalBudget += _trancheAmounts[i];
        }

        projects[projectId] = Project({
            recipientHIL: _recipientHIL,
            totalBudget: totalBudget,
            releasedFunds: 0,
            currentTrancheIndex: 0,
            trancheAmounts: _trancheAmounts,
            expectedMilestoneHashes: _expectedHashes,
            isEthicallyCertified: true
        });
    }

    // --- 2. DEPOSIT FUNDS (LINKED TO PROJECT) ---
    function depositFunds(uint256 _projectId) public payable {
        Project storage p = projects[_projectId];
        require(p.totalBudget > 0, "Project not initialized or invalid.");
    }

    // --- 3. SUBMIT PROOF (RESTRICTED BY HIL RECIPIENT) ---
    function submitMilestoneProof(uint256 _projectId, bytes32 _submittedProof) public {
        Project storage p = projects[_projectId];
        require(msg.sender == p.recipientHIL, "TrilogySeal Violation: Unauthorized submission.");
        uint256 currentIdx = p.currentTrancheIndex;
        require(currentIdx < p.expectedMilestoneHashes.length, "All tranches have already been released.");
        require(_submittedProof == p.expectedMilestoneHashes[currentIdx], "TrilogySeal Broken: Submitted proof does not match certified hash.");
        releaseCurrentTranche(_projectId);
        p.currentTrancheIndex++;
    }

    // --- 4. RELEASE FUNDS (INTERNAL & MANDATED) ---
    function releaseCurrentTranche(uint256 _projectId) internal {
        Project storage p = projects[_projectId];
        uint256 trancheAmount = p.trancheAmounts[p.currentTrancheIndex];
        require(address(this).balance >= trancheAmount, "Insufficient deposited funds for tranche release.");
        p.releasedFunds += trancheAmount;
        (bool success, ) = p.recipientHIL.call{value: trancheAmount}("");
        require(success, "Fund release failed.");
    }

    // --- 5. FALLBACK FUNCTION (RESTRICTED) ---
    receive() external payable {
        revert("RedCode Alert: Use depositFunds(projectId) for project-specific funding.");
    }
}