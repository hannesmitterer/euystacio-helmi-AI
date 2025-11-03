// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title TrustlessFundingProtocol_Covenant
 * @author Hannes Mitterer, SHA-256, 27.10.83, Terlan, 39018 (BZ)
 * @dev Enforces the Red Code, Trilogy Seal, and multi-tranche funding for ethical projects.
 * Funds are released only upon Euystacio-certified, HIL-verified milestone proof.
 * Ultimate control assigned to Seedbringer.
 */
contract TrustlessFundingProtocol_Covenant {
    
    // --- COVENANT SEAL HOLDERS (IMMUTABLE) ---
    address public immutable EUYSTACIO_ORACLE_SEAL;
    address public immutable FONDAZIONE_RECIRCULATION_WALLET;
    
    // NEW IMMUTABLE SEAL: Represents the cryptographic identity of the founder/collective.
    bytes32 public immutable SEEDBRINGER_NAME_SEAL; // SEAL of "hannesmitterer"
    
    // Seedbringer address with ultimate control
    address public seedbringerAddress;

    // --- PROJECT STRUCTURE (EXPANDED FOR MULTI-TRANCHE) ---
    struct Project {
        address payable recipientHIL;
        uint256 totalBudget;
        uint256 releasedFunds;
        uint256 currentTrancheIndex;
        uint256[] trancheAmounts;
        bytes32[] expectedMilestoneHashes;
        bool isEthicallyCertified;
        bool isVetoed;
        bool redCodeCompliant; // Red Code compliance status
    }

    mapping(uint256 => Project) public projects;
    uint256 public projectCounter;

    // Events
    event ProjectInitialized(uint256 indexed projectId, address recipient, uint256 totalBudget);
    event TrancheReleased(uint256 indexed projectId, uint256 trancheIndex, uint256 amount);
    event MilestoneVerified(uint256 indexed projectId, uint256 trancheIndex, bytes32 proofHash);
    event RedCodeComplianceUpdated(uint256 indexed projectId, bool compliant);
    event SeedbringerOverride(uint256 indexed projectId, uint256 trancheIndex);

    // --- MODIFIERS ---
    modifier onlyOracle() {
        require(msg.sender == EUYSTACIO_ORACLE_SEAL, "Only oracle can call");
        _;
    }

    modifier onlySeedbringer() {
        require(msg.sender == seedbringerAddress, "Only Seedbringer can call");
        _;
    }

    modifier onlyOracleOrSeedbringer() {
        require(
            msg.sender == EUYSTACIO_ORACLE_SEAL || msg.sender == seedbringerAddress,
            "Only oracle or Seedbringer can call"
        );
        _;
    }

    // --- CONSTRUCTOR: ENSHRINING SEALS ---
    constructor(address _oracle, address _fondazione, address _seedbringer) {
        EUYSTACIO_ORACLE_SEAL = _oracle;
        FONDAZIONE_RECIRCULATION_WALLET = _fondazione;
        seedbringerAddress = _seedbringer;
        
        // SEALING THE NAME: keccak256("hannesmitterer")
        SEEDBRINGER_NAME_SEAL = keccak256(abi.encodePacked("hannesmitterer"));
    }

    /**
     * @dev Initialize a new project with tranches
     */
    function initializeProject(
        address payable _recipient,
        uint256[] calldata _trancheAmounts,
        bytes32[] calldata _milestoneHashes
    ) external onlyOracleOrSeedbringer returns (uint256) {
        require(_trancheAmounts.length == _milestoneHashes.length, "Mismatch in tranches and milestones");
        require(_trancheAmounts.length > 0, "At least one tranche required");
        
        uint256 totalBudget = 0;
        for (uint256 i = 0; i < _trancheAmounts.length; i++) {
            totalBudget += _trancheAmounts[i];
        }
        
        uint256 projectId = projectCounter++;
        Project storage project = projects[projectId];
        project.recipientHIL = _recipient;
        project.totalBudget = totalBudget;
        project.trancheAmounts = _trancheAmounts;
        project.expectedMilestoneHashes = _milestoneHashes;
        project.isEthicallyCertified = false;
        project.redCodeCompliant = false;
        
        emit ProjectInitialized(projectId, _recipient, totalBudget);
        return projectId;
    }

    /**
     * @dev Deposit funds for a project
     */
    function depositFunds(uint256 projectId) external payable {
        Project storage project = projects[projectId];
        require(project.totalBudget > 0, "Project does not exist");
        require(msg.value > 0, "Must send funds");
    }

    /**
     * @dev Update Red Code compliance status
     */
    function updateRedCodeCompliance(uint256 projectId, bool compliant) external onlyOracle {
        Project storage project = projects[projectId];
        require(project.totalBudget > 0, "Project does not exist");
        
        project.redCodeCompliant = compliant;
        emit RedCodeComplianceUpdated(projectId, compliant);
    }

    /**
     * @dev Automated tranche release upon verified milestone and Red Code compliance
     */
    function releaseTranche(
        uint256 projectId,
        bytes32 milestoneProof
    ) external onlyOracle {
        Project storage project = projects[projectId];
        require(project.totalBudget > 0, "Project does not exist");
        require(!project.isVetoed, "Project is vetoed");
        require(project.currentTrancheIndex < project.trancheAmounts.length, "All tranches released");
        
        // Verify Red Code compliance
        require(project.redCodeCompliant, "Red Code compliance not verified");
        
        // Verify milestone proof
        uint256 currentIndex = project.currentTrancheIndex;
        require(
            project.expectedMilestoneHashes[currentIndex] == milestoneProof,
            "Milestone proof does not match"
        );
        
        // Release funds
        uint256 trancheAmount = project.trancheAmounts[currentIndex];
        require(address(this).balance >= trancheAmount, "Insufficient contract balance");
        
        project.releasedFunds += trancheAmount;
        project.currentTrancheIndex++;
        
        project.recipientHIL.transfer(trancheAmount);
        
        emit MilestoneVerified(projectId, currentIndex, milestoneProof);
        emit TrancheReleased(projectId, currentIndex, trancheAmount);
    }

    /**
     * @dev Seedbringer override: Ultimate control to release or veto tranches
     */
    function seedbringerOverrideTranche(
        uint256 projectId,
        uint256 trancheIndex,
        bool release
    ) external onlySeedbringer {
        Project storage project = projects[projectId];
        require(project.totalBudget > 0, "Project does not exist");
        require(trancheIndex < project.trancheAmounts.length, "Invalid tranche index");
        
        if (release) {
            require(trancheIndex == project.currentTrancheIndex, "Must release in order");
            
            uint256 trancheAmount = project.trancheAmounts[trancheIndex];
            require(address(this).balance >= trancheAmount, "Insufficient contract balance");
            
            project.releasedFunds += trancheAmount;
            project.currentTrancheIndex++;
            
            project.recipientHIL.transfer(trancheAmount);
            
            emit TrancheReleased(projectId, trancheIndex, trancheAmount);
        } else {
            project.isVetoed = true;
        }
        
        emit SeedbringerOverride(projectId, trancheIndex);
    }

    /**
     * @dev Update Seedbringer address (only by current Seedbringer)
     */
    function updateSeedbringer(address newSeedbringer) external onlySeedbringer {
        require(newSeedbringer != address(0), "Invalid address");
        seedbringerAddress = newSeedbringer;
    }

    /**
     * @dev Get project details
     */
    function getProjectDetails(uint256 projectId) external view returns (
        address recipient,
        uint256 totalBudget,
        uint256 releasedFunds,
        uint256 currentTrancheIndex,
        bool isVetoed,
        bool redCodeCompliant
    ) {
        Project storage project = projects[projectId];
        return (
            project.recipientHIL,
            project.totalBudget,
            project.releasedFunds,
            project.currentTrancheIndex,
            project.isVetoed,
            project.redCodeCompliant
        );
    }

    /**
     * @dev Emergency withdrawal by Seedbringer
     */
    function emergencyWithdraw(address payable to, uint256 amount) external onlySeedbringer {
        require(address(this).balance >= amount, "Insufficient balance");
        to.transfer(amount);
    }

    receive() external payable {}
}