const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("TrustlessFundingProtocol", function () {
  let trustlessFunding;
  let owner, seedbringer, foundationWallet, recipient;

  beforeEach(async function () {
    [owner, seedbringer, foundationWallet, recipient] = await ethers.getSigners();
    
    const TrustlessFundingProtocol = await ethers.getContractFactory("TrustlessFundingProtocol");
    trustlessFunding = await TrustlessFundingProtocol.deploy(foundationWallet.address, seedbringer.address);
    await trustlessFunding.deployed();
  });

  describe("Deployment", function () {
    it("should set the correct foundation wallet", async function () {
      expect(await trustlessFunding.foundationWallet()).to.equal(foundationWallet.address);
    });

    it("should set the correct Seedbringer", async function () {
      expect(await trustlessFunding.SEEDBRINGER()).to.equal(seedbringer.address);
    });

    it("should compute correct Seedbringer name seal", async function () {
      const expectedSeal = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("hannesmitterer"));
      expect(await trustlessFunding.SEEDBRINGER_NAME_SEAL()).to.equal(expectedSeal);
    });
  });

  describe("Tranche Creation", function () {
    it("should create tranche with milestone hash", async function () {
      const amount = ethers.utils.parseEther("100");
      const milestoneHash = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("milestone1"));
      
      await expect(
        trustlessFunding.createTranche(amount, milestoneHash)
      ).to.emit(trustlessFunding, "TrancheCreated")
        .withArgs(0, amount, milestoneHash);
      
      const tranche = await trustlessFunding.tranches(0);
      expect(tranche.amount).to.equal(amount);
      expect(tranche.milestoneHash).to.equal(milestoneHash);
      expect(tranche.released).to.be.false;
      expect(tranche.ethicallyCompliant).to.be.false;
      expect(tranche.vetoed).to.be.false;
    });

    it("should reject zero amount", async function () {
      const milestoneHash = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("milestone1"));
      await expect(
        trustlessFunding.createTranche(0, milestoneHash)
      ).to.be.revertedWith("Amount must be positive");
    });

    it("should reject invalid milestone hash", async function () {
      const amount = ethers.utils.parseEther("100");
      await expect(
        trustlessFunding.createTranche(amount, ethers.constants.HashZero)
      ).to.be.revertedWith("Invalid milestone hash");
    });
  });

  describe("Ethical Compliance Verification", function () {
    beforeEach(async function () {
      const amount = ethers.utils.parseEther("100");
      const milestoneHash = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("milestone1"));
      await trustlessFunding.createTranche(amount, milestoneHash);
    });

    it("should allow Seedbringer to verify ethical compliance", async function () {
      await expect(
        trustlessFunding.connect(seedbringer).verifyEthicalCompliance(0, true)
      ).to.emit(trustlessFunding, "EthicalComplianceVerified")
        .withArgs(0, true);
      
      const tranche = await trustlessFunding.tranches(0);
      expect(tranche.ethicallyCompliant).to.be.true;
    });

    it("should allow owner to verify ethical compliance", async function () {
      await expect(
        trustlessFunding.connect(owner).verifyEthicalCompliance(0, true)
      ).to.emit(trustlessFunding, "EthicalComplianceVerified")
        .withArgs(0, true);
    });

    it("should reject verification from unauthorized address", async function () {
      await expect(
        trustlessFunding.connect(recipient).verifyEthicalCompliance(0, true)
      ).to.be.revertedWith("Only Seedbringer or owner");
    });
  });

  describe("Tranche Veto", function () {
    beforeEach(async function () {
      const amount = ethers.utils.parseEther("100");
      const milestoneHash = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("milestone1"));
      await trustlessFunding.createTranche(amount, milestoneHash);
    });

    it("should allow Seedbringer to veto tranche", async function () {
      await expect(
        trustlessFunding.connect(seedbringer).vetoTranche(0)
      ).to.emit(trustlessFunding, "TrancheVetoed")
        .withArgs(0, seedbringer.address);
      
      const tranche = await trustlessFunding.tranches(0);
      expect(tranche.vetoed).to.be.true;
    });

    it("should reject veto from non-Seedbringer", async function () {
      await expect(
        trustlessFunding.connect(owner).vetoTranche(0)
      ).to.be.revertedWith("Only Seedbringer can veto");
    });

    it("should prevent release of vetoed tranche", async function () {
      await trustlessFunding.connect(seedbringer).vetoTranche(0);
      
      // Should not be able to verify ethical compliance after veto
      await expect(
        trustlessFunding.connect(owner).verifyEthicalCompliance(0, true)
      ).to.be.revertedWith("Tranche vetoed");
    });
  });

  describe("Tranche Release", function () {
    const amount = ethers.utils.parseEther("100");
    let milestoneHash;

    beforeEach(async function () {
      milestoneHash = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("milestone1"));
      await trustlessFunding.createTranche(amount, milestoneHash);
    });

    it("should release tranche with valid proof and ethical compliance", async function () {
      await trustlessFunding.connect(seedbringer).verifyEthicalCompliance(0, true);
      
      await expect(
        trustlessFunding.connect(seedbringer).releaseTranche(0, milestoneHash)
      ).to.emit(trustlessFunding, "TrancheReleased");
      
      const tranche = await trustlessFunding.tranches(0);
      expect(tranche.released).to.be.true;
      expect(await trustlessFunding.trancheReleased(0)).to.be.true;
    });

    it("should allow owner to release with Seedbringer approval", async function () {
      await trustlessFunding.connect(seedbringer).verifyEthicalCompliance(0, true);
      
      await expect(
        trustlessFunding.connect(owner).releaseTranche(0, milestoneHash)
      ).to.emit(trustlessFunding, "TrancheReleased");
    });

    it("should reject release without ethical compliance", async function () {
      await expect(
        trustlessFunding.connect(seedbringer).releaseTranche(0, milestoneHash)
      ).to.be.revertedWith("Ethical compliance not verified");
    });

    it("should reject release with wrong proof", async function () {
      await trustlessFunding.connect(seedbringer).verifyEthicalCompliance(0, true);
      
      const wrongHash = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("wrongmilestone"));
      await expect(
        trustlessFunding.connect(seedbringer).releaseTranche(0, wrongHash)
      ).to.be.revertedWith("Proof does not match milestone");
    });

    it("should reject release from unauthorized address", async function () {
      await trustlessFunding.connect(seedbringer).verifyEthicalCompliance(0, true);
      
      await expect(
        trustlessFunding.connect(recipient).releaseTranche(0, milestoneHash)
      ).to.be.revertedWith("Only Seedbringer or owner");
    });

    it("should prevent double release", async function () {
      await trustlessFunding.connect(seedbringer).verifyEthicalCompliance(0, true);
      await trustlessFunding.connect(seedbringer).releaseTranche(0, milestoneHash);
      
      await expect(
        trustlessFunding.connect(seedbringer).releaseTranche(0, milestoneHash)
      ).to.be.revertedWith("Already released");
    });
  });
});
