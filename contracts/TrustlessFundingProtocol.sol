// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title TrustlessFundingProtocol
 * @dev Simple version of trustless funding with tranche releases
 * For more advanced features, see TrustlessFundingProtocol_Covenant
 */
contract TrustlessFundingProtocol is Ownable {
    address public foundationWallet;
    mapping(uint256 => bool) public trancheReleased;
    mapping(uint256 => bool) public redCodeCompliant;
    
    event TrancheReleased(uint256 indexed trancheId, bytes32 proofHash, uint256 timestamp);
    event RedCodeComplianceUpdated(uint256 indexed trancheId, bool compliant);

    constructor(address _foundationWallet) Ownable(msg.sender) {
        foundationWallet = _foundationWallet;
    }

    /**
     * @dev Update Red Code compliance for a tranche
     */
    function updateRedCodeCompliance(uint256 trancheId, bool compliant) external onlyOwner {
        redCodeCompliant[trancheId] = compliant;
        emit RedCodeComplianceUpdated(trancheId, compliant);
    }

    /**
     * @dev Release tranche when proofHash submitted and Red Code is compliant
     * Proof stored off-chain
     */
    function releaseTranche(uint256 trancheId, bytes32 proofHash) external onlyOwner {
        require(!trancheReleased[trancheId], "Already released");
        require(proofHash != bytes32(0), "Invalid proof");
        require(redCodeCompliant[trancheId], "Red Code compliance not verified");
        
        trancheReleased[trancheId] = true;
        emit TrancheReleased(trancheId, proofHash, block.timestamp);
    }
}