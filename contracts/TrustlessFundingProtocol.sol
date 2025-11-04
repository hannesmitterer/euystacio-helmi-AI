// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract TrustlessFundingProtocol is Ownable, ReentrancyGuard {
    // Seedbringer authority - hannesmitterer
    address public seedbringer;
    address public foundationWallet;
    
    struct Tranche {
        uint256 amount;
        bool released;
        bool redCodeCertified;
        bytes32 milestoneProofHash;
        address recipient;
        uint256 releaseTime;
        bool vetoedBySeedbringer;
    }
    
    mapping(uint256 => Tranche) public tranches;
    uint256 public trancheCount;
    
    event TrancheCreated(uint256 indexed trancheId, address indexed recipient, uint256 amount);
    event TrancheReleased(uint256 indexed trancheId, bytes32 proofHash, uint256 timestamp);
    event TrancheVetoed(uint256 indexed trancheId, address indexed seedbringer);
    event RedCodeCertified(uint256 indexed trancheId, bool certified);
    event SeedbringerUpdated(address indexed newSeedbringer);
    event MilestoneProofSubmitted(uint256 indexed trancheId, bytes32 proofHash);

    modifier onlySeedbringer() {
        require(msg.sender == seedbringer, "Only Seedbringer");
        _;
    }

    constructor(address _foundationWallet, address _seedbringer) {
        foundationWallet = _foundationWallet;
        seedbringer = _seedbringer;
    }

    receive() external payable {}

    /// Create a new tranche
    function createTranche(address recipient, uint256 amount) external onlyOwner {
        uint256 trancheId = trancheCount++;
        tranches[trancheId] = Tranche({
            amount: amount,
            released: false,
            redCodeCertified: false,
            milestoneProofHash: bytes32(0),
            recipient: recipient,
            releaseTime: 0,
            vetoedBySeedbringer: false
        });
        emit TrancheCreated(trancheId, recipient, amount);
    }

    /// Seedbringer certifies Red Code compliance for a tranche
    function certifyRedCode(uint256 trancheId, bool certified) external onlySeedbringer {
        require(trancheId < trancheCount, "Invalid tranche");
        tranches[trancheId].redCodeCertified = certified;
        emit RedCodeCertified(trancheId, certified);
    }

    /// Submit milestone proof for automated verification (restricted to owner or recipient)
    function submitMilestoneProof(uint256 trancheId, bytes32 proofHash) external {
        require(trancheId < trancheCount, "Invalid tranche");
        Tranche storage tranche = tranches[trancheId];
        
        // Only owner or recipient can submit proof
        require(msg.sender == owner() || msg.sender == tranche.recipient, "Not authorized");
        require(!tranche.released, "Already released");
        require(!tranche.vetoedBySeedbringer, "Vetoed by Seedbringer");
        require(proofHash != bytes32(0), "Invalid proof");
        
        tranche.milestoneProofHash = proofHash;
        emit MilestoneProofSubmitted(trancheId, proofHash);
        
        // Automated release if Red Code certified and proof submitted
        if (tranche.redCodeCertified) {
            _releaseTranche(trancheId);
        }
    }

    /// Internal function to release tranche
    function _releaseTranche(uint256 trancheId) internal nonReentrant {
        Tranche storage tranche = tranches[trancheId];
        require(!tranche.released, "Already released");
        require(tranche.redCodeCertified, "Red Code certification required");
        require(tranche.milestoneProofHash != bytes32(0), "Milestone proof required");
        require(!tranche.vetoedBySeedbringer, "Vetoed by Seedbringer");
        require(address(this).balance >= tranche.amount, "Insufficient balance");
        
        tranche.released = true;
        tranche.releaseTime = block.timestamp;
        
        (bool success, ) = payable(tranche.recipient).call{value: tranche.amount}("");
        require(success, "Transfer failed");
        
        emit TrancheReleased(trancheId, tranche.milestoneProofHash, block.timestamp);
    }

    /// Seedbringer can manually release a tranche (override)
    function seedbringerRelease(uint256 trancheId) external onlySeedbringer nonReentrant {
        require(trancheId < trancheCount, "Invalid tranche");
        Tranche storage tranche = tranches[trancheId];
        require(!tranche.released, "Already released");
        require(!tranche.vetoedBySeedbringer, "Cannot release vetoed tranche");
        
        // Seedbringer can release even without Red Code or proof
        tranche.released = true;
        tranche.releaseTime = block.timestamp;
        
        if (address(this).balance >= tranche.amount) {
            (bool success, ) = payable(tranche.recipient).call{value: tranche.amount}("");
            require(success, "Transfer failed");
        }
        emit TrancheReleased(trancheId, tranche.milestoneProofHash, block.timestamp);
    }

    /// Seedbringer veto power
    function vetoTranche(uint256 trancheId) external onlySeedbringer {
        require(trancheId < trancheCount, "Invalid tranche");
        require(!tranches[trancheId].released, "Already released");
        
        tranches[trancheId].vetoedBySeedbringer = true;
        emit TrancheVetoed(trancheId, msg.sender);
    }

    /// Seedbringer can update the Seedbringer address
    function updateSeedbringer(address newSeedbringer) external onlySeedbringer {
        seedbringer = newSeedbringer;
        emit SeedbringerUpdated(newSeedbringer);
    }

    /// Owner can fund the contract
    function fundContract() external payable onlyOwner {}

    /// Emergency withdrawal (only owner)
    function emergencyWithdraw(address to, uint256 amount) external onlyOwner nonReentrant {
        (bool success, ) = payable(to).call{value: amount}("");
        require(success, "Emergency withdrawal failed");
    }
}