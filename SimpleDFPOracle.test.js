const { expect } = require('chai');
const { ethers } = require('hardhat');

describe('SimpleDFPOracle', function () {
    let SimpleDFPOracle;
    let DFPEscrowStub;
    let oracle;
    let escrowStub;
    let owner;
    let addr1;
    const TRIP_ID_SUCCESS = 101;
    const TRIP_ID_FAILURE = 102;
    const TRIP_ID_REVERT = 103;

    beforeEach(async function () {
        [owner, addr1] = await ethers.getSigners();

        // Deploy the DFPEscrowStub first
        DFPEscrowStub = await ethers.getContractFactory('DFPEscrowStub');
        escrowStub = await DFPEscrowStub.deploy();
        await escrowStub.waitForDeployment();

        // Deploy the Oracle, passing the stub address
        SimpleDFPOracle = await ethers.getContractFactory('SimpleDFPOracle');
        oracle = await SimpleDFPOracle.deploy(await escrowStub.getAddress());
        await oracle.waitForDeployment();
    });

    // ----------------------------------------------------------------
    // Core Logic Tests: fulfillSafePassage
    // ----------------------------------------------------------------

    describe('fulfillSafePassage', function () {
        it('Should revert if called by non-owner', async function () {
            await expect(
                oracle.connect(addr1).fulfillSafePassage(TRIP_ID_SUCCESS, true)
            ).to.be.revertedWith('Only owner can call this function');
        });

        it('Should correctly update oracle state and emit SafePassageFulfilled', async function () {
            await expect(oracle.fulfillSafePassage(TRIP_ID_SUCCESS, true))
                .to.emit(oracle, 'SafePassageFulfilled')
                .withArgs(TRIP_ID_SUCCESS, true);

            expect(await oracle.safePassageConfirmed(TRIP_ID_SUCCESS)).to.equal(true);
        });

        it('Should successfully notify escrow and emit EscrowNotified(callSuccess=true)', async function () {
            // Check that the escrow receives the confirmation
            await expect(oracle.fulfillSafePassage(TRIP_ID_FAILURE, false))
                .to.emit(escrowStub, 'PassageConfirmationReceived')
                .withArgs(TRIP_ID_FAILURE, false)
                // Check that the oracle correctly reports successful external call
                .to.emit(oracle, 'EscrowNotified')
                .withArgs(TRIP_ID_FAILURE, false, true, '0x'); 

            expect(await escrowStub.tripConfirmed(TRIP_ID_FAILURE)).to.equal(false);
        });
    });

    // ----------------------------------------------------------------
    // Resilience Test: try/catch handling
    // ----------------------------------------------------------------

    describe('External Call Resilience', function () {
        it('Should update oracle state even if escrow call reverts (try/catch)', async function () {
            // 1. Owner forces the stub to revert on the next call
            await escrowStub.toggleRevert(true);

            // 2. Call the oracle function: this should fail internally on the escrow call,
            // but the oracle state update must persist.
            await expect(oracle.fulfillSafePassage(TRIP_ID_REVERT, true))
                .to.not.be.reverted; // Crucial: the oracle transaction must succeed

            // 3. Verify Oracle State (State must be updated)
            expect(await oracle.safePassageConfirmed(TRIP_ID_REVERT)).to.equal(true);

            // 4. Verify EscrowNotified event (Should report failure with reason)
            // The reason will contain the ABI-encoded revert message.
            const tx = await oracle.fulfillSafePassage.staticCall(TRIP_ID_REVERT, true); // Get event data from the call
            
            await expect(oracle.fulfillSafePassage(TRIP_ID_REVERT, true))
                .to.emit(oracle, 'EscrowNotified')
                .withArgs(
                    TRIP_ID_REVERT, 
                    true, 
                    false, // Crucial: callSuccess must be false
                    ethers.utils.hexlify(ethers.utils.toUtf8Bytes('Escrow forced to revert for testing.'))
                ); 
        });
    });
    
    // ----------------------------------------------------------------
    // Administration Tests: updateEscrowAddress
    // ----------------------------------------------------------------

    describe('Administration', function () {
        let newEscrowStub;

        beforeEach(async function() {
            // Deploy a second stub to represent a new escrow contract
            newEscrowStub = await DFPEscrowStub.deploy();
            await newEscrowStub.waitForDeployment();
        });

        it('Should revert if new address is EOA (not a contract)', async function () {
            await expect(
                oracle.updateEscrowAddress(addr1.address)
            ).to.be.revertedWith('Escrow address must be a contract');
        });

        it('Should revert if called by non-owner', async function () {
            await expect(
                oracle.connect(addr1).updateEscrowAddress(await newEscrowStub.getAddress())
            ).to.be.revertedWith('Only owner can call this function');
        });

        it('Should successfully update the address and emit EscrowAddressUpdated', async function () {
            const oldAddress = await oracle.dfpEscrowAddress();
            const newAddress = await newEscrowStub.getAddress();

            await expect(oracle.updateEscrowAddress(newAddress))
                .to.emit(oracle, 'EscrowAddressUpdated')
                .withArgs(oldAddress, newAddress);

            expect(await oracle.dfpEscrowAddress()).to.equal(newAddress);
        });
    });
});
