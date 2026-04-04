// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./EuystacioKernel.sol";

contract ResonanceDiploma {
    EuystacioKernel public kernel;
    mapping(address => bool) public isResonant;
    uint256 public totalResonators;

    event DiplomaIssued(address indexed resonator, uint256 timestamp);

    constructor(address _kernelAddress) {
        kernel = EuystacioKernel(_kernelAddress);
    }

    function issueDiploma() public {
        require(kernel.systemActive(), "Sistema in Mute Mode.");
        require(kernel.dignityAffinity() >= 950, "Risonanza globale troppo bassa.");
        require(!isResonant[msg.sender], "Gia risonante.");
        
        isResonant[msg.sender] = true;
        totalResonators++;
        emit DiplomaIssued(msg.sender, block.timestamp);
    }
}
