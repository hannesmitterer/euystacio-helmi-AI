// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

contract TrustlessFundingProtocol is Ownable {
    address public foundationWallet;
    address public immutable SEEDBRINGER; // Seedbringer authority for veto/release
    bytes32 public immutable SEEDBRINGER_NAME_SEAL; // keccak256("hannesmitterer")
    
    struct Tranche {
        uint256 amount;
        bytes32 milestoneHash;
        bool released;
        bool ethicallyCompliant;
        bool vetoed;
    }
    
    mapping(uint256 => Tranche) public tranches;
    mapping(uint256 => bool) public trancheReleased; // legacy support
    uint256 public trancheCounter;
    
    event TrancheCreated(uint256 indexed trancheId, uint256 amount, bytes32 milestoneHash);
    event TrancheReleased(uint256 indexed trancheId, bytes32 proofHash, uint256 timestamp);
    event TrancheVetoed(uint256 indexed trancheId, address vetoedBy);
    event EthicalComplianceVerified(uint256 indexed trancheId, bool compliant);

    constructor(address _foundationWallet, address _seedbringer) {
        foundationWallet = _foundationWallet;
        SEEDBRINGER = _seedbringer;
        SEEDBRINGER_NAME_SEAL = keccak256(abi.encodePacked("hannesmitterer"));
    }
    
    /// Create a new tranche with milestone requirements
    /// @param amount Amount of funds for this tranche
    /// @param milestoneHash Expected milestone hash for verification
    function createTranche(uint256 amount, bytes32 milestoneHash) external onlyOwner {
        require(amount > 0, "Amount must be positive");
        require(milestoneHash != bytes32(0), "Invalid milestone hash");
        
        uint256 trancheId = trancheCounter++;
        tranches[trancheId] = Tranche({
            amount: amount,
            milestoneHash: milestoneHash,
            released: false,
            ethicallyCompliant: false,
            vetoed: false
        });
        
        emit TrancheCreated(trancheId, amount, milestoneHash);
    }
    
    /// Verify ethical compliance for a tranche (only Seedbringer)
    /// @param trancheId The tranche to verify
    /// @param compliant Whether the tranche meets ethical standards
    function verifyEthicalCompliance(uint256 trancheId, bool compliant) external {
        require(msg.sender == SEEDBRINGER || msg.sender == owner(), "Only Seedbringer or owner");
        require(!tranches[trancheId].released, "Already released");
        require(!tranches[trancheId].vetoed, "Tranche vetoed");
        
        tranches[trancheId].ethicallyCompliant = compliant;
        emit EthicalComplianceVerified(trancheId, compliant);
    }
    
    /// Seedbringer veto power for any tranche
    /// @param trancheId The tranche to veto
    function vetoTranche(uint256 trancheId) external {
        require(msg.sender == SEEDBRINGER, "Only Seedbringer can veto");
        require(!tranches[trancheId].released, "Already released");
        
        tranches[trancheId].vetoed = true;
        emit TrancheVetoed(trancheId, msg.sender);
    }

    /// release tranche when proofHash submitted and ethical compliance verified
    /// Final authority to Seedbringer for approval
    function releaseTranche(uint256 trancheId, bytes32 proofHash) external {
        require(msg.sender == SEEDBRINGER || msg.sender == owner(), "Only Seedbringer or owner");
        
        Tranche storage tranche = tranches[trancheId];
        require(!tranche.released, "Already released");
        require(!tranche.vetoed, "Tranche vetoed");
        require(tranche.ethicallyCompliant, "Ethical compliance not verified");
        require(proofHash != bytes32(0), "Invalid proof");
        require(proofHash == tranche.milestoneHash, "Proof does not match milestone");
        
        tranche.released = true;
        trancheReleased[trancheId] = true; // legacy support
        
        emit TrancheReleased(trancheId, proofHash, block.timestamp);
    }
}