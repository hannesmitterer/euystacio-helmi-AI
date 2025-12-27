// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Base64.sol";

contract EuystacioManifest is ERC721 {
    uint256 public constant TOKEN_ID = 1;

    string[] public fileCIDs;
    bytes32[] public fileHashes;

    event EuystacioAnchored(
        uint256 indexed tokenId,
        string[] fileCIDs,
        bytes32[] fileHashes
    );

    constructor(string[] memory _fileCIDs) ERC721("EuystacioManifest", "EUM") {
        fileCIDs = _fileCIDs;
        fileHashes = new bytes32[](_fileCIDs.length);

        for (uint i = 0; i < _fileCIDs.length; i++) {
            fileHashes[i] = keccak256(bytes(_fileCIDs[i]));
        }

        _mint(msg.sender, TOKEN_ID);
        emit EuystacioAnchored(TOKEN_ID, fileCIDs, fileHashes);
    }

    function tokenURI(uint256) public view override returns (string memory) {
        bytes memory json = abi.encodePacked(
            '{"name":"Euystacio Manifest","description":"Publicly anchored manifesto with multiple cryptographic signatures","files":['
        );

        for (uint i = 0; i < fileCIDs.length; i++) {
            json = abi.encodePacked(
                json,
                '{"cid":"', fileCIDs[i], '","hash":"0x', _toHex(fileHashes[i]), '"}',
                i < fileCIDs.length - 1 ? ',' : ''
            );
        }

        json = abi.encodePacked(json, "]}");

        return string(
            abi.encodePacked("data:application/json;base64,", Base64.encode(json))
        );
    }

    function _toHex(bytes32 data) internal pure returns (string memory) {
        bytes memory alphabet = "0123456789abcdef";
        bytes memory str = new bytes(64);
        for (uint i = 0; i < 32; i++) {
            str[i*2] = alphabet[uint8(data[i] >> 4)];
            str[i*2+1] = alphabet[uint8(data[i] & 0x0f)];
        }
        return string(str);
    }
}
