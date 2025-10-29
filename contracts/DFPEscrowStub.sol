// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title DFPEscrowStub
 * @notice Stub contract for testing SimpleDFPOracle's external call resilience.
 * This contract implements the IDFPEscrow interface and can be configured to
 * succeed or revert, allowing us to test both success and failure flows.
 */
contract DFPEscrowStub {
    // State variables for testing
    bool public shouldRevert;
    string public revertMessage;
    
    // Storage for received confirmations
    uint256 public lastTripId;
    bool public lastSuccess;
    uint256 public confirmationCount;
    
    // Events
    event ConfirmationReceived(uint256 indexed tripId, bool success);
    
    /**
     * @notice Constructor to initialize the stub
     * @param _shouldRevert Whether the stub should revert on confirmSafePassage calls
     * @param _revertMessage The message to use when reverting
     */
    constructor(bool _shouldRevert, string memory _revertMessage) {
        shouldRevert = _shouldRevert;
        revertMessage = _revertMessage;
    }
    
    /**
     * @notice Implementation of the IDFPEscrow interface
     * @dev This function will revert if shouldRevert is true, otherwise it stores the data
     * @param tripId The trip identifier
     * @param success The safe passage result
     */
    function confirmSafePassage(uint256 tripId, bool success) external {
        if (shouldRevert) {
            revert(revertMessage);
        }
        
        lastTripId = tripId;
        lastSuccess = success;
        confirmationCount++;
        
        emit ConfirmationReceived(tripId, success);
    }
    
    /**
     * @notice Allows updating the revert behavior for testing
     * @param _shouldRevert New revert behavior
     */
    function setShouldRevert(bool _shouldRevert) external {
        shouldRevert = _shouldRevert;
    }
    
    /**
     * @notice Allows updating the revert message for testing
     * @param _revertMessage New revert message
     */
    function setRevertMessage(string memory _revertMessage) external {
        revertMessage = _revertMessage;
    }
    
    /**
     * @notice Resets the confirmation tracking
     */
    function reset() external {
        lastTripId = 0;
        lastSuccess = false;
        confirmationCount = 0;
    }
}
