// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title Interface for the DFPEscrow Contract
 * @notice Defines the external function signature for notifying the escrow.
 */
interface IDFPEscrow {
    function confirmSafePassage(uint256 tripId, bool success) external;
}

/**
 * @title Simple DFP Oracle with Escrow Notification
 * @notice Oracle stores "safe passage" results and notifies a DFPEscrow contract.
 */
contract SimpleDFPOracle {
    // --- State Variables ---

    address public owner;
    address public dfpEscrowAddress;
    
    // Mapping to store the result of the safe passage check for each tripId
    mapping(uint256 => bool) public safePassageConfirmed;

    // --- Events ---

    event EscrowAddressUpdated(address indexed oldAddress, address indexed newAddress);
    event SafePassageFulfilled(uint256 indexed tripId, bool success);
    event EscrowNotified(uint256 indexed tripId, bool success, bool indexed callSuccess, bytes returnData);

    // --- Modifiers ---

    /**
     * @notice Restricts access to the contract owner.
     * @dev Note: In production, consider replacing this with a dedicated 'oracle' role
     * (e.g., using OpenZeppelin AccessControl) for better separation of duties.
     */
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    // --- Constructor ---

    constructor(address _initialEscrowAddress) {
        owner = msg.sender;
        // The initial address set here must be an escrow contract
        _setEscrowAddress(_initialEscrowAddress);
    }

    // --- External Call Safety Check ---
    
    /**
     * @notice Performs a minimal check to see if an address is a contract.
     * @dev Checks if the address has non-zero code size.
     * @param account The address to check.
     * @return bool True if the address is a contract.
     */
    function isContract(address account) internal view returns (bool) {
        uint256 size;
        assembly {
            size := extcodesize(account)
        }
        return size > 0;
    }

    // --- Core Oracle Logic ---

    /**
     * @notice Stores the safe passage result and attempts to notify the Escrow contract.
     * @dev This is typically called by a trusted off-chain oracle node (the owner).
     * State is updated *before* the external call for good practice.
     * @param tripId The unique identifier for the trip.
     * @param success The result of the safe passage check.
     */
    function fulfillSafePassage(uint256 tripId, bool success) external onlyOwner {
        // 1. Update Oracle State
        safePassageConfirmed[tripId] = success;
        emit SafePassageFulfilled(tripId, success);

        // 2. Attempt Escrow Notification (Safer External Call)
        // try/catch ensures the oracle's state update is not reverted by a failed escrow call.
        try IDFPEscrow(dfpEscrowAddress).confirmSafePassage(tripId, success) {
            // Success branch
            emit EscrowNotified(tripId, success, true, new bytes(0));
        } catch (bytes memory reason) {
            // Failure branch: call failed or reverted
            emit EscrowNotified(tripId, success, false, reason);
        }
    }

    // --- Administration Functions ---

    /**
     * @notice Updates the address of the DFPEscrow contract.
     * @dev Requires the new address to be a contract, not an EOA.
     * @param newEscrowAddress The address of the new DFPEscrow contract.
     */
    function updateEscrowAddress(address newEscrowAddress) external onlyOwner {
        _setEscrowAddress(newEscrowAddress);
    }

    /**
     * @dev Internal function to update the escrow address with checks.
     */
    function _setEscrowAddress(address newEscrowAddress) internal {
        require(newEscrowAddress != address(0), "Escrow address cannot be zero");
        require(isContract(newEscrowAddress), "Escrow address must be a contract");
        
        emit EscrowAddressUpdated(dfpEscrowAddress, newEscrowAddress);
        dfpEscrowAddress = newEscrowAddress;
    }
}