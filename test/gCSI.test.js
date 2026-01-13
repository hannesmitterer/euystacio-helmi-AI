const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("GlobalConsensusSealIntegrity", function () {
  let gCSI;
  let owner;
  let council1;
  let council2;
  let council3;
  let nonMember;

  beforeEach(async function () {
    [owner, council1, council2, council3, nonMember] = await ethers.getSigners();

    const GCSI = await ethers.getContractFactory("GlobalConsensusSealIntegrity");
    gCSI = await GCSI.deploy();
    await gCSI.waitForDeployment();
  });

  describe("Council Management", function () {
    it("Should add deployer as initial council member", async function () {
      const member = await gCSI.councilMembers(owner.address);
      expect(member.active).to.be.true;
      expect(await gCSI.activeCouncilCount()).to.equal(1);
    });

    it("Should allow owner to add council members", async function () {
      await expect(gCSI.addCouncilMember(council1.address, "Council Member 1"))
        .to.emit(gCSI, "CouncilMemberAdded")
        .withArgs(council1.address, "Council Member 1");

      const member = await gCSI.councilMembers(council1.address);
      expect(member.active).to.be.true;
      expect(member.name).to.equal("Council Member 1");
    });

    it("Should prevent adding duplicate active members", async function () {
      await gCSI.addCouncilMember(council1.address, "Council 1");
      
      await expect(
        gCSI.addCouncilMember(council1.address, "Duplicate")
      ).to.be.revertedWith("G-CSI: Already active member");
    });

    it("Should allow owner to deactivate council members", async function () {
      await gCSI.addCouncilMember(council1.address, "Council 1");
      await gCSI.addCouncilMember(council2.address, "Council 2");

      await expect(gCSI.deactivateCouncilMember(council1.address))
        .to.emit(gCSI, "CouncilMemberDeactivated")
        .withArgs(council1.address);

      const member = await gCSI.councilMembers(council1.address);
      expect(member.active).to.be.false;
      expect(await gCSI.activeCouncilCount()).to.equal(2);
    });

    it("Should prevent deactivation if it would break quorum", async function () {
      // Only owner is active, minimum signatures is 1
      await expect(
        gCSI.deactivateCouncilMember(owner.address)
      ).to.be.revertedWith("G-CSI: Cannot deactivate, would break quorum");
    });
  });

  describe("Quorum Requirements", function () {
    beforeEach(async function () {
      await gCSI.addCouncilMember(council1.address, "Council 1");
      await gCSI.addCouncilMember(council2.address, "Council 2");
      // Total: 3 active council members
    });

    it("Should allow owner to update quorum requirements", async function () {
      await expect(gCSI.setQuorumRequirements(66, 2))
        .to.emit(gCSI, "QuorumUpdated")
        .withArgs(66, 2);

      expect(await gCSI.quorumPercentage()).to.equal(66);
      expect(await gCSI.minimumSignatures()).to.equal(2);
    });

    it("Should prevent invalid percentage", async function () {
      await expect(
        gCSI.setQuorumRequirements(0, 1)
      ).to.be.revertedWith("G-CSI: Invalid percentage");

      await expect(
        gCSI.setQuorumRequirements(101, 1)
      ).to.be.revertedWith("G-CSI: Invalid percentage");
    });

    it("Should prevent minimum signatures exceeding council size", async function () {
      await expect(
        gCSI.setQuorumRequirements(50, 10)
      ).to.be.revertedWith("G-CSI: Min signatures exceeds council size");
    });

    it("Should calculate current quorum requirement correctly", async function () {
      // 3 members, 51% = 1.53 rounded = 2, min = 1, so requirement = 2
      let requirement = await gCSI.getCurrentQuorumRequirement();
      expect(requirement).to.equal(1); // 51% of 3 = 1.53, min is 1

      await gCSI.setQuorumRequirements(67, 2);
      requirement = await gCSI.getCurrentQuorumRequirement();
      expect(requirement).to.equal(2); // 67% of 3 = 2.01, min is 2
    });
  });

  describe("Seal Creation and Signing", function () {
    let actionHash;

    beforeEach(async function () {
      await gCSI.addCouncilMember(council1.address, "Council 1");
      await gCSI.addCouncilMember(council2.address, "Council 2");
      actionHash = ethers.keccak256(ethers.toUtf8Bytes("test action"));
    });

    it("Should allow council member to create seal", async function () {
      const metadata = "Test governance action";
      
      const tx = await gCSI.connect(owner).createSeal(actionHash, metadata);
      const receipt = await tx.wait();

      const sealId = await gCSI.getSealIdByIndex(0);
      const seal = await gCSI.seals(sealId);
      
      expect(seal.actionHash).to.equal(actionHash);
      expect(seal.metadata).to.equal(metadata);
      expect(seal.signatureCount).to.equal(1); // Creator auto-signs
    });

    it("Should prevent non-council members from creating seal", async function () {
      await expect(
        gCSI.connect(nonMember).createSeal(actionHash, "metadata")
      ).to.be.revertedWith("G-CSI: Not an active council member");
    });

    it("Should auto-sign seal for creator", async function () {
      await gCSI.connect(owner).createSeal(actionHash, "metadata");
      const sealId = await gCSI.getSealIdByIndex(0);
      
      expect(await gCSI.hasSigned(sealId, owner.address)).to.be.true;
      expect(await gCSI.getSignatureCount(sealId)).to.equal(1);
    });

    it("Should allow other council members to sign", async function () {
      await gCSI.connect(owner).createSeal(actionHash, "metadata");
      const sealId = await gCSI.getSealIdByIndex(0);

      await expect(gCSI.connect(council1).signSeal(sealId))
        .to.emit(gCSI, "SealSigned")
        .withArgs(sealId, council1.address);

      expect(await gCSI.hasSigned(sealId, council1.address)).to.be.true;
      expect(await gCSI.getSignatureCount(sealId)).to.equal(2);
    });

    it("Should prevent signing twice", async function () {
      await gCSI.connect(owner).createSeal(actionHash, "metadata");
      const sealId = await gCSI.getSealIdByIndex(0);

      await expect(
        gCSI.connect(owner).signSeal(sealId)
      ).to.be.revertedWith("G-CSI: Already signed");
    });

    it("Should prevent non-council members from signing", async function () {
      await gCSI.connect(owner).createSeal(actionHash, "metadata");
      const sealId = await gCSI.getSealIdByIndex(0);

      await expect(
        gCSI.connect(nonMember).signSeal(sealId)
      ).to.be.revertedWith("G-CSI: Not an active council member");
    });
  });

  describe("Quorum and Execution", function () {
    let actionHash;

    beforeEach(async function () {
      await gCSI.addCouncilMember(council1.address, "Council 1");
      await gCSI.addCouncilMember(council2.address, "Council 2");
      await gCSI.setQuorumRequirements(51, 2); // Need 2 signatures
      actionHash = ethers.keccak256(ethers.toUtf8Bytes("test action"));
    });

    it("Should detect when quorum is not reached", async function () {
      await gCSI.connect(owner).createSeal(actionHash, "metadata");
      const sealId = await gCSI.getSealIdByIndex(0);

      // Only 1 signature (creator)
      expect(await gCSI.hasQuorum(sealId)).to.be.false;
    });

    it("Should detect when quorum is reached", async function () {
      await gCSI.connect(owner).createSeal(actionHash, "metadata");
      const sealId = await gCSI.getSealIdByIndex(0);

      await gCSI.connect(council1).signSeal(sealId);
      
      // Now 2 signatures
      expect(await gCSI.hasQuorum(sealId)).to.be.true;
    });

    it("Should allow execution when quorum reached", async function () {
      await gCSI.connect(owner).createSeal(actionHash, "metadata");
      const sealId = await gCSI.getSealIdByIndex(0);

      await gCSI.connect(council1).signSeal(sealId);

      await expect(gCSI.connect(council2).executeSeal(sealId))
        .to.emit(gCSI, "SealExecuted")
        .withArgs(sealId);

      const seal = await gCSI.seals(sealId);
      expect(seal.executed).to.be.true;
    });

    it("Should prevent execution without quorum", async function () {
      await gCSI.connect(owner).createSeal(actionHash, "metadata");
      const sealId = await gCSI.getSealIdByIndex(0);

      await expect(
        gCSI.connect(owner).executeSeal(sealId)
      ).to.be.revertedWith("G-CSI: Quorum not reached");
    });

    it("Should prevent duplicate execution", async function () {
      await gCSI.connect(owner).createSeal(actionHash, "metadata");
      const sealId = await gCSI.getSealIdByIndex(0);

      await gCSI.connect(council1).signSeal(sealId);
      await gCSI.connect(owner).executeSeal(sealId);

      await expect(
        gCSI.connect(owner).executeSeal(sealId)
      ).to.be.revertedWith("G-CSI: Already executed");
    });

    it("Should prevent signing after execution", async function () {
      await gCSI.connect(owner).createSeal(actionHash, "metadata");
      const sealId = await gCSI.getSealIdByIndex(0);

      await gCSI.connect(council1).signSeal(sealId);
      await gCSI.connect(owner).executeSeal(sealId);

      await expect(
        gCSI.connect(council2).signSeal(sealId)
      ).to.be.revertedWith("G-CSI: Seal already executed");
    });
  });

  describe("Seal Verification", function () {
    let actionHash;

    beforeEach(async function () {
      await gCSI.addCouncilMember(council1.address, "Council 1");
      await gCSI.setQuorumRequirements(51, 2);
      actionHash = ethers.keccak256(ethers.toUtf8Bytes("test action"));
    });

    it("Should verify valid executed seal", async function () {
      await gCSI.connect(owner).createSeal(actionHash, "metadata");
      const sealId = await gCSI.getSealIdByIndex(0);

      await gCSI.connect(council1).signSeal(sealId);
      await gCSI.connect(owner).executeSeal(sealId);

      expect(await gCSI.verifySeal(sealId)).to.be.true;
    });

    it("Should not verify non-executed seal", async function () {
      await gCSI.connect(owner).createSeal(actionHash, "metadata");
      const sealId = await gCSI.getSealIdByIndex(0);

      await gCSI.connect(council1).signSeal(sealId);

      expect(await gCSI.verifySeal(sealId)).to.be.false;
    });

    it("Should not verify non-existent seal", async function () {
      const fakeSealId = ethers.keccak256(ethers.toUtf8Bytes("fake"));
      expect(await gCSI.verifySeal(fakeSealId)).to.be.false;
    });
  });

  describe("Query Functions", function () {
    let actionHash;

    beforeEach(async function () {
      await gCSI.addCouncilMember(council1.address, "Council 1");
      await gCSI.addCouncilMember(council2.address, "Council 2");
      actionHash = ethers.keccak256(ethers.toUtf8Bytes("test action"));
    });

    it("Should return seal count", async function () {
      expect(await gCSI.getSealCount()).to.equal(0);

      await gCSI.connect(owner).createSeal(actionHash, "Seal 1");
      expect(await gCSI.getSealCount()).to.equal(1);

      await gCSI.connect(owner).createSeal(ethers.keccak256(ethers.toUtf8Bytes("action2")), "Seal 2");
      expect(await gCSI.getSealCount()).to.equal(2);
    });

    it("Should return signers for a seal", async function () {
      await gCSI.connect(owner).createSeal(actionHash, "metadata");
      const sealId = await gCSI.getSealIdByIndex(0);

      await gCSI.connect(council1).signSeal(sealId);
      await gCSI.connect(council2).signSeal(sealId);

      const signers = await gCSI.getSigners(sealId);
      expect(signers.length).to.equal(3);
      expect(signers).to.include(owner.address);
      expect(signers).to.include(council1.address);
      expect(signers).to.include(council2.address);
    });

    it("Should prevent accessing out of bounds index", async function () {
      await expect(
        gCSI.getSealIdByIndex(0)
      ).to.be.revertedWith("G-CSI: Index out of bounds");
    });
  });
});
