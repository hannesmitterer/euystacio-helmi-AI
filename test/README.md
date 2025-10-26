# SimpleDFPOracle Unit Tests

This directory contains comprehensive unit tests for the SimpleDFPOracle.sol contract.

## Overview

The tests validate the Oracle's external call resilience mechanism using the DFPEscrowStub.sol boilerplate contract. They demonstrate both success and failure flows of the Oracle's external calls, ensuring alignment with the Trustful (TRF-001) and Ethical Infallibility constants within the smart contract layer.

## Test Coverage

### 1. Deployment Tests
- Validates correct owner and escrow address initialization
- Ensures proper validation of escrow address (non-zero, contract)

### 2. Success Flow Tests (TRF-001: Trustful)
- Tests successful oracle state updates with escrow notification
- Validates event emissions (SafePassageFulfilled, EscrowNotified)
- Ensures proper handling of multiple safe passage confirmations
- Confirms bidirectional data flow between Oracle and Escrow

### 3. Failure Flow Tests (Ethical Infallibility)
- **Key Feature**: Demonstrates try/catch resilience mechanism
- Validates that Oracle state is preserved even when Escrow calls fail
- Tests multiple consecutive failures
- Confirms system recovery when Escrow becomes available again
- Ensures no state reversion on external call failures

### 4. Access Control Tests
- Restricts fulfillSafePassage to owner only
- Restricts escrow address updates to owner only

### 5. Integration Tests
- Validates TRF-001 (Trustful) behavior with working external dependencies
- Demonstrates Ethical Infallibility with failing external dependencies
- Tests state consistency across mixed success/failure scenarios

## Running the Tests

### Prerequisites
```bash
npm install
```

### Run All SimpleDFPOracle Tests
```bash
npx hardhat test test/simpleDFPOracle.test.js --no-compile
```

### Run Specific Test Suites
```bash
# Run only deployment tests
npx hardhat test test/simpleDFPOracle.test.js --grep "Deployment" --no-compile

# Run only success flow tests
npx hardhat test test/simpleDFPOracle.test.js --grep "Success Flow" --no-compile

# Run only failure flow tests
npx hardhat test test/simpleDFPOracle.test.js --grep "Failure Flow" --no-compile
```

### Generate Gas Report
```bash
REPORT_GAS=true npx hardhat test test/simpleDFPOracle.test.js --no-compile
```

## Test Architecture

### DFPEscrowStub.sol
The stub contract provides a configurable testing interface:
- **Success Mode**: Acts as a normal escrow, storing confirmations
- **Failure Mode**: Reverts with configurable error messages
- **Tracking**: Maintains counters and last received values for verification

### Key Test Scenarios

#### 1. Trustful Behavior (TRF-001)
When external dependencies are functioning correctly, the Oracle trusts and uses them transparently:
```javascript
await simpleDFPOracle.fulfillSafePassage(tripId, true);
// Both Oracle state AND Escrow state are updated
```

#### 2. Ethical Infallibility
When external dependencies fail, the Oracle maintains its core functionality:
```javascript
await dfpEscrowStub.setShouldRevert(true);
await simpleDFPOracle.fulfillSafePassage(tripId, true);
// Oracle state is STILL updated (no revert)
// System remains operational despite external failure
```

## Test Results

All 19 tests pass successfully:
- ✅ 4 Deployment tests
- ✅ 3 Success Flow tests  
- ✅ 3 Failure Flow tests
- ✅ 2 Access Control tests
- ✅ 4 Escrow Address Update tests
- ✅ 3 Integration tests

## Notes

The `--no-compile` flag is used because some other contracts in the repository have compilation issues unrelated to SimpleDFPOracle. The SimpleDFPOracle and DFPEscrowStub contracts compile successfully and their artifacts are cached for testing.

## Smart Contract Constants

### TRF-001: Trustful
The system operates with trust and transparency. When external dependencies are functioning, the Oracle trusts and integrates with them seamlessly.

### Ethical Infallibility
The system must never fail completely. Even when external dependencies fail, the Oracle maintains its core state management function through the try/catch resilience mechanism.
