// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./EuystacioKernel.sol";

contract EuystacioPeaceBond {
    EuystacioKernel public kernel;
    
    struct Bond {
        uint256 value;
        uint256 startTime;
        uint256 maturityTime;
        bool liquidated;
    }

    mapping(address => Bond) public bonds;
    uint256 public totalPeaceCapital;

    event BondIssued(address indexed holder, uint256 amount);
    event BondImpactVerified(address indexed holder, uint256 currentDignity);

    constructor(address _kernelAddress) {
        kernel = EuystacioKernel(_kernelAddress);
    }

    /**
     * @dev Emette un PeaceBond. L'azione è possibile solo se il sistema è in risonanza.
     */
    function issueBond(uint256 _amount, uint256 _durationDays) public {
        require(kernel.systemActive(), "Emissione bloccata: Sistema in Mute Mode.");
        require(kernel.dignityAffinity() >= 950, "Dignita insufficiente per emettere Titoli di Pace.");

        bonds[msg.sender] = Bond({
            value: _amount,
            startTime: block.timestamp,
            maturityTime: block.timestamp + (_durationDays * 1 days),
            liquidated: false
        });

        totalPeaceCapital += _amount;
        emit BondIssued(msg.sender, _amount);
    }

    /**
     * @dev Verifica l'impatto. Se la dignita scende, il bond entra in 'Ethical Freeze'.
     */
    function verifyImpact() public view returns (bool) {
        return kernel.dignityAffinity() >= 940;
    }
}
