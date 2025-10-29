const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("SimpleDFPOracle", function () {
  let simpleDFPOracle;
  let dfpEscrowStub;
  let owner;
  let nonOwner;

  beforeEach(async function () {
    // Get signers
    [owner, nonOwner] = await ethers.getSigners();

    // Deploy DFPEscrowStub (initially set to not revert)
    const DFPEscrowStub = await ethers.getContractFactory("DFPEscrowStub");
    dfpEscrowStub = await DFPEscrowStub.deploy(false, "");

    // Deploy SimpleDFPOracle with the stub as the escrow address
    const SimpleDFPOracle = await ethers.getContractFactory("SimpleDFPOracle");
    simpleDFPOracle = await SimpleDFPOracle.deploy(dfpEscrowStub.target);
  });

  describe("Deployment", function () {
    it("should set the owner correctly", async function () {
      expect(await simpleDFPOracle.owner()).to.equal(owner.address);
    });

    it("should set the escrow address correctly", async function () {
      expect(await simpleDFPOracle.dfpEscrowAddress()).to.equal(dfpEscrowStub.target);
    });

    it("should revert if escrow address is zero address", async function () {
      const SimpleDFPOracle = await ethers.getContractFactory("SimpleDFPOracle");
      await expect(
        SimpleDFPOracle.deploy(ethers.ZeroAddress)
      ).to.be.revertedWith("Escrow address cannot be zero");
    });

    it("should revert if escrow address is not a contract", async function () {
      const SimpleDFPOracle = await ethers.getContractFactory("SimpleDFPOracle");
      await expect(
        SimpleDFPOracle.deploy(nonOwner.address)
      ).to.be.revertedWith("Escrow address must be a contract");
    });
  });

  describe("fulfillSafePassage - Success Flow (TRF-001: Trustful)", function () {
    it("should update oracle state and notify escrow successfully", async function () {
      const tripId = 1;
      const success = true;

      // Execute fulfillSafePassage
      const tx = await simpleDFPOracle.fulfillSafePassage(tripId, success);
      const receipt = await tx.wait();

      // Verify oracle state was updated
      expect(await simpleDFPOracle.safePassageConfirmed(tripId)).to.equal(success);

      // Verify SafePassageFulfilled event was emitted
      const safePassageEvent = receipt.logs.find(
        log => log.fragment && log.fragment.name === "SafePassageFulfilled"
      );
      expect(safePassageEvent).to.not.be.undefined;
      expect(safePassageEvent.args.tripId).to.equal(tripId);
      expect(safePassageEvent.args.success).to.equal(success);

      // Verify EscrowNotified event with success=true
      const escrowNotifiedEvent = receipt.logs.find(
        log => log.fragment && log.fragment.name === "EscrowNotified"
      );
      expect(escrowNotifiedEvent).to.not.be.undefined;
      expect(escrowNotifiedEvent.args.tripId).to.equal(tripId);
      expect(escrowNotifiedEvent.args.success).to.equal(success);
      expect(escrowNotifiedEvent.args.callSuccess).to.equal(true);

      // Verify stub received the confirmation
      expect(await dfpEscrowStub.lastTripId()).to.equal(tripId);
      expect(await dfpEscrowStub.lastSuccess()).to.equal(success);
      expect(await dfpEscrowStub.confirmationCount()).to.equal(1);
    });

    it("should handle safe passage with success=false", async function () {
      const tripId = 2;
      const success = false;

      await simpleDFPOracle.fulfillSafePassage(tripId, success);

      // Verify oracle state
      expect(await simpleDFPOracle.safePassageConfirmed(tripId)).to.equal(success);

      // Verify stub received the correct value
      expect(await dfpEscrowStub.lastTripId()).to.equal(tripId);
      expect(await dfpEscrowStub.lastSuccess()).to.equal(success);
    });

    it("should handle multiple fulfillments", async function () {
      await simpleDFPOracle.fulfillSafePassage(1, true);
      await simpleDFPOracle.fulfillSafePassage(2, false);
      await simpleDFPOracle.fulfillSafePassage(3, true);

      expect(await simpleDFPOracle.safePassageConfirmed(1)).to.equal(true);
      expect(await simpleDFPOracle.safePassageConfirmed(2)).to.equal(false);
      expect(await simpleDFPOracle.safePassageConfirmed(3)).to.equal(true);
      expect(await dfpEscrowStub.confirmationCount()).to.equal(3);
    });
  });

  describe("fulfillSafePassage - Failure Flow (Ethical Infallibility)", function () {
    it("should maintain oracle state even when escrow call reverts (try/catch resilience)", async function () {
      const tripId = 10;
      const success = true;

      // Configure stub to revert
      await dfpEscrowStub.setShouldRevert(true);
      await dfpEscrowStub.setRevertMessage("Escrow is down");

      // Execute fulfillSafePassage - should NOT revert
      const tx = await simpleDFPOracle.fulfillSafePassage(tripId, success);
      const receipt = await tx.wait();

      // CRITICAL: Verify oracle state was STILL updated despite escrow failure
      expect(await simpleDFPOracle.safePassageConfirmed(tripId)).to.equal(success);

      // Verify SafePassageFulfilled event was still emitted
      const safePassageEvent = receipt.logs.find(
        log => log.fragment && log.fragment.name === "SafePassageFulfilled"
      );
      expect(safePassageEvent).to.not.be.undefined;

      // Verify EscrowNotified event with callSuccess=false
      const escrowNotifiedEvent = receipt.logs.find(
        log => log.fragment && log.fragment.name === "EscrowNotified"
      );
      expect(escrowNotifiedEvent).to.not.be.undefined;
      expect(escrowNotifiedEvent.args.tripId).to.equal(tripId);
      expect(escrowNotifiedEvent.args.success).to.equal(success);
      expect(escrowNotifiedEvent.args.callSuccess).to.equal(false);
      
      // The returnData should contain the revert reason
      expect(escrowNotifiedEvent.args.returnData.length).to.be.greaterThan(0);

      // Verify stub did NOT receive confirmation (because it reverted)
      expect(await dfpEscrowStub.confirmationCount()).to.equal(0);
    });

    it("should handle multiple failures gracefully", async function () {
      await dfpEscrowStub.setShouldRevert(true);
      await dfpEscrowStub.setRevertMessage("System error");

      // All should succeed from oracle's perspective
      await simpleDFPOracle.fulfillSafePassage(1, true);
      await simpleDFPOracle.fulfillSafePassage(2, false);
      await simpleDFPOracle.fulfillSafePassage(3, true);

      // All oracle states should be updated
      expect(await simpleDFPOracle.safePassageConfirmed(1)).to.equal(true);
      expect(await simpleDFPOracle.safePassageConfirmed(2)).to.equal(false);
      expect(await simpleDFPOracle.safePassageConfirmed(3)).to.equal(true);

      // But stub received nothing
      expect(await dfpEscrowStub.confirmationCount()).to.equal(0);
    });

    it("should recover when escrow becomes available again", async function () {
      // Start with failing escrow
      await dfpEscrowStub.setShouldRevert(true);
      await dfpEscrowStub.setRevertMessage("Temporary failure");

      // First call - escrow fails but oracle succeeds
      await simpleDFPOracle.fulfillSafePassage(1, true);
      expect(await simpleDFPOracle.safePassageConfirmed(1)).to.equal(true);
      expect(await dfpEscrowStub.confirmationCount()).to.equal(0);

      // Fix escrow
      await dfpEscrowStub.setShouldRevert(false);

      // Second call - should work end-to-end
      await simpleDFPOracle.fulfillSafePassage(2, false);
      expect(await simpleDFPOracle.safePassageConfirmed(2)).to.equal(false);
      expect(await dfpEscrowStub.confirmationCount()).to.equal(1);
      expect(await dfpEscrowStub.lastTripId()).to.equal(2);
    });
  });

  describe("Access Control", function () {
    it("should only allow owner to fulfill safe passage", async function () {
      await expect(
        simpleDFPOracle.connect(nonOwner).fulfillSafePassage(1, true)
      ).to.be.revertedWith("Only owner can call this function");
    });

    it("should only allow owner to update escrow address", async function () {
      const newStub = await (await ethers.getContractFactory("DFPEscrowStub")).deploy(false, "");
      
      await expect(
        simpleDFPOracle.connect(nonOwner).updateEscrowAddress(newStub.target)
      ).to.be.revertedWith("Only owner can call this function");
    });
  });

  describe("updateEscrowAddress", function () {
    it("should update escrow address successfully", async function () {
      const newStub = await (await ethers.getContractFactory("DFPEscrowStub")).deploy(false, "");
      
      const tx = await simpleDFPOracle.updateEscrowAddress(newStub.target);
      const receipt = await tx.wait();

      expect(await simpleDFPOracle.dfpEscrowAddress()).to.equal(newStub.target);

      // Verify event
      const event = receipt.logs.find(
        log => log.fragment && log.fragment.name === "EscrowAddressUpdated"
      );
      expect(event).to.not.be.undefined;
      expect(event.args.newAddress).to.equal(newStub.target);
    });

    it("should revert when updating to zero address", async function () {
      await expect(
        simpleDFPOracle.updateEscrowAddress(ethers.ZeroAddress)
      ).to.be.revertedWith("Escrow address cannot be zero");
    });

    it("should revert when updating to non-contract address", async function () {
      await expect(
        simpleDFPOracle.updateEscrowAddress(nonOwner.address)
      ).to.be.revertedWith("Escrow address must be a contract");
    });

    it("should work with new escrow after update", async function () {
      const newStub = await (await ethers.getContractFactory("DFPEscrowStub")).deploy(false, "");
      
      await simpleDFPOracle.updateEscrowAddress(newStub.target);
      await simpleDFPOracle.fulfillSafePassage(100, true);

      // Old stub should not receive anything
      expect(await dfpEscrowStub.confirmationCount()).to.equal(0);

      // New stub should receive the confirmation
      expect(await newStub.confirmationCount()).to.equal(1);
      expect(await newStub.lastTripId()).to.equal(100);
    });
  });

  describe("Integration: TRF-001 and Ethical Infallibility", function () {
    it("should demonstrate trustful behavior (TRF-001) with successful external calls", async function () {
      // TRF-001: The system operates with trust and transparency
      // When escrow is working, the oracle trusts and uses it
      const tripId = 999;
      await simpleDFPOracle.fulfillSafePassage(tripId, true);

      // Both oracle and escrow are in sync
      expect(await simpleDFPOracle.safePassageConfirmed(tripId)).to.equal(true);
      expect(await dfpEscrowStub.lastTripId()).to.equal(tripId);
      expect(await dfpEscrowStub.lastSuccess()).to.equal(true);
    });

    it("should demonstrate ethical infallibility with failed external calls", async function () {
      // Ethical Infallibility: The system must never fail completely
      // Even when external dependencies fail, the oracle maintains its core function
      await dfpEscrowStub.setShouldRevert(true);
      await dfpEscrowStub.setRevertMessage("Critical escrow failure");

      const tripId = 888;
      // This should NOT throw - demonstrating infallibility
      await expect(
        simpleDFPOracle.fulfillSafePassage(tripId, true)
      ).to.not.be.reverted;

      // Oracle state is preserved - core function maintained
      expect(await simpleDFPOracle.safePassageConfirmed(tripId)).to.equal(true);
    });

    it("should maintain state consistency across success and failure scenarios", async function () {
      // Mix of successful and failed external calls
      await simpleDFPOracle.fulfillSafePassage(1, true); // Success
      
      await dfpEscrowStub.setShouldRevert(true);
      await simpleDFPOracle.fulfillSafePassage(2, false); // Failure
      
      await dfpEscrowStub.setShouldRevert(false);
      await simpleDFPOracle.fulfillSafePassage(3, true); // Success again

      // All oracle states should be consistent
      expect(await simpleDFPOracle.safePassageConfirmed(1)).to.equal(true);
      expect(await simpleDFPOracle.safePassageConfirmed(2)).to.equal(false);
      expect(await simpleDFPOracle.safePassageConfirmed(3)).to.equal(true);

      // Stub should have received 2 confirmations (1 and 3, not 2)
      expect(await dfpEscrowStub.confirmationCount()).to.equal(2);
    });
  });
});
