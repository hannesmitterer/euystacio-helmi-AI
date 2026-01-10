const { expect } = require("chai");
const { ethers } = require("hardhat");

// NOTE: These tests are for an older TrustlessFundingProtocol/KarmaBond implementation
// with ERC20 tokens, Sustainment contract, and different governance patterns.
// The current contracts use native ETH with Seedbringer authority.
// These tests are skipped pending migration to the new contract interface.
describe.skip("Governance Enforcement", function () {
  let tfp;
  let sustainment;
  let karmaBond;
  let mockToken;
  let owner;
  let foundation;
  let investor;

  const DECIMALS = 6;
  const MIN_USD = 10000;
  const MIN_SUSTAINMENT = MIN_USD * (10 ** DECIMALS);
  const SUSTAINMENT_PERCENT = 200;

  beforeEach(async function () {
    [owner, foundation, investor] = await ethers.getSigners();

    // Deploy mock token
    const MockERC20 = await ethers.getContractFactory("MockERC20");
    mockToken = await MockERC20.deploy("Mock USDC", "USDC", DECIMALS);
    await mockToken.waitForDeployment();

    // Deploy Sustainment
    const Sustainment = await ethers.getContractFactory("Sustainment");
    sustainment = await Sustainment.deploy(
      await mockToken.getAddress(),
      DECIMALS,
      MIN_USD
    );
    await sustainment.waitForDeployment();

    // Deploy KarmaBond
    const KarmaBond = await ethers.getContractFactory("KarmaBond");
    karmaBond = await KarmaBond.deploy(
      await mockToken.getAddress(),
      await sustainment.getAddress(),
      foundation.address,
      BigInt(SUSTAINMENT_PERCENT)
    );
    await karmaBond.waitForDeployment();

    // Authorize KarmaBond
    await sustainment.setAuthorizedDepositor(await karmaBond.getAddress(), true);

    // Deploy TrustlessFundingProtocol
    const TFP = await ethers.getContractFactory("TrustlessFundingProtocol");
    tfp = await TFP.deploy(foundation.address);
    await tfp.waitForDeployment();

    // Configure TFP with Sustainment
    await tfp.setSustainmentContract(await sustainment.getAddress());

    // Mint tokens to investor
    await mockToken.mint(investor.address, ethers.parseUnits("1000000", DECIMALS)); // 1M tokens for testing
  });

  describe("Tranche Release Enforcement", function () {
    it("Should block tranche release when sustainment below minimum", async function () {
      const trancheId = 1n;
      const proofHash = ethers.keccak256(ethers.toUtf8Bytes("proof"));

      // Sustainment is empty (below minimum)
      expect(await sustainment.isAboveMinimum()).to.be.false;

      await expect(
        tfp.releaseTranche(trancheId, proofHash)
      ).to.be.revertedWith("Sustainment below minimum");
    });

    it("Should allow tranche release when sustainment above minimum", async function () {
      const trancheId = 1n;
      const proofHash = ethers.keccak256(ethers.toUtf8Bytes("proof"));

      // Fund sustainment above minimum
      await mockToken.connect(investor).approve(await karmaBond.getAddress(), BigInt(MIN_SUSTAINMENT) * 55n);
      await karmaBond.connect(investor).mintBond(BigInt(MIN_SUSTAINMENT) * 55n);

      expect(await sustainment.isAboveMinimum()).to.be.true;

      await expect(tfp.releaseTranche(trancheId, proofHash))
        .to.emit(tfp, "TrancheReleased");
    });

    it("Should emit rejection event when sustainment insufficient", async function () {
      const trancheId = 1;
      const proofHash = ethers.keccak256(ethers.toUtf8Bytes("proof"));

      // Partially fund sustainment (below minimum) - need to mint enough so 2% reaches half of minimum
      // To get MIN_SUSTAINMENT/2 in sustainment pool, we need to mint: (MIN_SUSTAINMENT/2) * 50 = MIN_SUSTAINMENT * 25
      const mintAmount = BigInt(MIN_SUSTAINMENT) * 25n;
      await mockToken.connect(investor).approve(await karmaBond.getAddress(), mintAmount);
      await karmaBond.connect(investor).mintBond(mintAmount);

      const currentReserve = await sustainment.getSustainmentReserve();
      
      // Should be below minimum
      expect(await sustainment.isAboveMinimum()).to.be.false;

      // Transaction should revert
      await expect(
        tfp.releaseTranche(trancheId, proofHash)
      ).to.be.revertedWith("Sustainment below minimum");
    });

    it("Should allow emergency override via governance toggle", async function () {
      const trancheId = 1n;
      const proofHash = ethers.keccak256(ethers.toUtf8Bytes("proof"));

      // Disable enforcement
      await tfp.setGovernanceEnforcement(false);

      // Should now allow tranche release even with empty sustainment
      expect(await sustainment.isAboveMinimum()).to.be.false;

      await tfp.releaseTranche(trancheId, proofHash);
      expect(await tfp.trancheReleased(trancheId)).to.be.true;
    });

    it("Should emit event when governance enforcement toggled", async function () {
      await expect(tfp.setGovernanceEnforcement(false))
        .to.emit(tfp, "GovernanceEnforcementToggled")
        .withArgs(false);

      await expect(tfp.setGovernanceEnforcement(true))
        .to.emit(tfp, "GovernanceEnforcementToggled")
        .withArgs(true);
    });
  });

  describe("Tranche Check View Function", function () {
    it("Should report tranche cannot be released when below minimum", async function () {
      const trancheId = 1n;

      const [canRelease, reason] = await tfp.canReleaseTranche(trancheId);
      
      expect(canRelease).to.be.false;
      expect(reason).to.equal("Sustainment below minimum");
    });

    it("Should report tranche can be released when above minimum", async function () {
      const trancheId = 1n;

      // Fund sustainment
      await mockToken.connect(investor).approve(await karmaBond.getAddress(), BigInt(MIN_SUSTAINMENT) * 55n);
      await karmaBond.connect(investor).mintBond(BigInt(MIN_SUSTAINMENT) * 55n);

      const [canRelease, reason] = await tfp.canReleaseTranche(trancheId);
      
      expect(canRelease).to.be.true;
      expect(reason).to.equal("");
    });

    it("Should report already released tranches", async function () {
      const trancheId = 1n;
      const proofHash = ethers.keccak256(ethers.toUtf8Bytes("proof"));

      // Fund and release
      await mockToken.connect(investor).approve(await karmaBond.getAddress(), BigInt(MIN_SUSTAINMENT) * 55n);
      await karmaBond.connect(investor).mintBond(BigInt(MIN_SUSTAINMENT) * 55n);
      await tfp.releaseTranche(trancheId, proofHash);

      const [canRelease, reason] = await tfp.canReleaseTranche(trancheId);
      
      expect(canRelease).to.be.false;
      expect(reason).to.equal("Already released");
    });
  });

  describe("Sustainment Contract Configuration", function () {
    it("Should allow owner to update sustainment contract", async function () {
      const newSustainment = ethers.Wallet.createRandom().address;

      await expect(tfp.setSustainmentContract(newSustainment))
        .to.emit(tfp, "SustainmentContractUpdated")
        .withArgs(await sustainment.getAddress(), newSustainment);

      expect(await tfp.sustainmentContract()).to.equal(newSustainment);
    });

    it("Should work without sustainment contract when enforcement disabled", async function () {
      const trancheId = 1n;
      const proofHash = ethers.keccak256(ethers.toUtf8Bytes("proof"));

      // Remove sustainment contract and disable enforcement
      await tfp.setSustainmentContract("0x0000000000000000000000000000000000000000");
      await tfp.setGovernanceEnforcement(false);

      await tfp.releaseTranche(trancheId, proofHash);
      expect(await tfp.trancheReleased(trancheId)).to.be.true;
    });
  });

  describe("Integration Scenarios", function () {
    it("Should enforce sustainment across multiple tranche releases", async function () {
      // Fund sustainment to exactly minimum
      const fundAmount = BigInt(MIN_SUSTAINMENT) * 10000n / BigInt(SUSTAINMENT_PERCENT);
      await mockToken.connect(investor).approve(await karmaBond.getAddress(), fundAmount);
      await karmaBond.connect(investor).mintBond(fundAmount);

      expect(await sustainment.isAboveMinimum()).to.be.true;

      // Release first tranche
      await tfp.releaseTranche(1, ethers.keccak256(ethers.toUtf8Bytes("proof1")));
      
      // Release second tranche
      await tfp.releaseTranche(2, ethers.keccak256(ethers.toUtf8Bytes("proof2")));
      
      expect(await tfp.trancheReleased(1)).to.be.true;
      expect(await tfp.trancheReleased(2)).to.be.true;
    });

    it("Should prevent tranche release if sustainment withdrawn below minimum", async function () {
      // Fund sustainment
      const fundAmount = BigInt(MIN_SUSTAINMENT) * 10000n / BigInt(SUSTAINMENT_PERCENT);
      await mockToken.connect(investor).approve(await karmaBond.getAddress(), fundAmount);
      await karmaBond.connect(investor).mintBond(fundAmount);

      // Release first tranche successfully
      await tfp.releaseTranche(1, ethers.keccak256(ethers.toUtf8Bytes("proof1")));

      // Withdraw sustainment below minimum
      const currentReserve = await sustainment.getSustainmentReserve();
      const withdrawAmount = BigInt(currentReserve) - BigInt(MIN_SUSTAINMENT) + 1000n;
      await sustainment.withdrawSustainment(owner.address, withdrawAmount);

      expect(await sustainment.isAboveMinimum()).to.be.false;

      // Second tranche should fail
      await expect(
        tfp.releaseTranche(2, ethers.keccak256(ethers.toUtf8Bytes("proof2")))
      ).to.be.revertedWith("Sustainment below minimum");
    });

    it("Should allow governance to continue after sustainment replenished", async function () {
      const trancheId = 1n;
      const proofHash = ethers.keccak256(ethers.toUtf8Bytes("proof"));

      // Initially empty
      await expect(
        tfp.releaseTranche(trancheId, proofHash)
      ).to.be.revertedWith("Sustainment below minimum");

      // Replenish sustainment
      const fundAmount = BigInt(MIN_SUSTAINMENT) * 10000n / BigInt(SUSTAINMENT_PERCENT);
      await mockToken.connect(investor).approve(await karmaBond.getAddress(), fundAmount);
      await karmaBond.connect(investor).mintBond(fundAmount);

      // Now should succeed
      await tfp.releaseTranche(trancheId, proofHash);
      expect(await tfp.trancheReleased(trancheId)).to.be.true;
    });
  });

  describe("Security", function () {
    it("Should reject duplicate tranche releases", async function () {
      const trancheId = 1n;
      const proofHash = ethers.keccak256(ethers.toUtf8Bytes("proof"));

      // Fund sustainment
      const fundAmount = BigInt(MIN_SUSTAINMENT) * 10000n / BigInt(SUSTAINMENT_PERCENT);
      await mockToken.connect(investor).approve(await karmaBond.getAddress(), fundAmount);
      await karmaBond.connect(investor).mintBond(fundAmount);

      // Release once
      await tfp.releaseTranche(trancheId, proofHash);

      // Try to release again
      await expect(
        tfp.releaseTranche(trancheId, proofHash)
      ).to.be.revertedWith("Already released");
    });

    it("Should reject invalid proof hash", async function () {
      await expect(
        tfp.releaseTranche(1, "0x0000000000000000000000000000000000000000000000000000000000000000")
      ).to.be.revertedWith("Invalid proof");
    });

    it("Should reject non-owner tranche releases", async function () {
      const fundAmount = BigInt(MIN_SUSTAINMENT) * 10000n / BigInt(SUSTAINMENT_PERCENT);
      await mockToken.connect(investor).approve(await karmaBond.getAddress(), fundAmount);
      await karmaBond.connect(investor).mintBond(fundAmount);

      await expect(
        tfp.connect(investor).releaseTranche(1, ethers.keccak256(ethers.toUtf8Bytes("proof")))
      ).to.be.revertedWith("Ownable: caller is not the owner");
    });
  });
});
