// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

contract TrustlessFundingProtocol is Ownable {
    address public foundationWallet;
    mapping(uint256 => bool) public trancheReleased;
    event TrancheReleased(uint256 indexed trancheId, bytes32 proofHash, uint256 timestamp);

    constructor(address _foundationWallet) {
        foundationWallet = _foundationWallet;
    }

    /// release tranche when proofHash submitted (proof stored off-chain)
    function releaseTranche(uint256 trancheId, bytes32 proofHash) external onlyOwner {
        require(!trancheReleased[trancheId], "Already released");
        require(proofHash != bytes32(0), "Invalid proof");
        trancheReleased[trancheId] = true;
        emit TrancheReleased(trancheId, proofHash, block.timestamp);
    }
}