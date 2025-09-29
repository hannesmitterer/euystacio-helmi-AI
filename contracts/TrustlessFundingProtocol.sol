// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

contract TrustlessFundingProtocol is Ownable {
    address public foundationWallet;
    mapping(uint256 => bool) public trancheReleased;

    constructor(address _foundationWallet) {
        foundationWallet = _foundationWallet;
    }

    function releaseTranche(uint256 trancheId, bytes32 proofHash) external onlyOwner {
        require(!trancheReleased[trancheId], "Already released");
        require(proofHash != 0, "Invalid proof");
        trancheReleased[trancheId] = true;
    }
}