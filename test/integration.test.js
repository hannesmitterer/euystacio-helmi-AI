const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Contract Integration", function () {
  let karmaBond, trustlessFunding, governance;
  let owner, seedbringer, foundationWallet, investor, recipient;

  beforeEach(async function () {
    [owner, seedbringer, foundationWallet, investor, recipient] = await ethers.getSigners();
    
    // Deploy all contracts
    const KarmaBond = await ethers.getContractFactory("KarmaBond");
    karmaBond = await KarmaBond.deploy(foundationWallet.address, seedbringer.address);
    await karmaBond.deployed();
    
    const TrustlessFundingProtocol = await ethers.getContractFactory("TrustlessFundingProtocol");
    trustlessFunding = await TrustlessFundingProtocol.deploy(foundationWallet.address, seedbringer.address);
    await trustlessFunding.deployed();
    
    const EUSDaoGovernance = await ethers.getContractFactory("EUSDaoGovernance");
    governance = await EUSDaoGovernance.deploy(seedbringer.address);
    await governance.deployed();
  });

  describe("Full Workflow Integration", function () {
    it("should complete full bond investment to governance token flow", async function () {
      // Step 1: Investor creates a bond with minimum contribution
      const bondAmount = ethers.utils.parseEther("100");
      const duration = 365 * 24 * 60 * 60; // 1 year
      
      await karmaBond.connect(investor).investWithDuration(duration, { value: bondAmount });
      
      const bond = await karmaBond.bonds(investor.address);
      expect(bond.amount).to.equal(bondAmount);
      expect(bond.isActive).to.be.true;
      
      // Step 2: Sync bond contribution to governance
      await governance.connect(owner).syncBondContribution(investor.address, bondAmount);
      
      const bondContribution = await governance.bondContributions(investor.address);
      expect(bondContribution).to.equal(bondAmount);
      
      // Step 3: Mint governance tokens based on contribution score
      const contributionScore = await governance.contributionScore(investor.address);
      expect(contributionScore).to.equal(100); // 100 ETH = 100 points
      
      // Seedbringer mints tokens
      const tokenAmount = ethers.utils.parseEther("10");
      await governance.connect(seedbringer).mint(investor.address, tokenAmount);
      
      // Step 4: Check voting power
      const votingPower = await governance.votingPower(investor.address);
      // votingPower = balance * (contributionScore + 1) = 10 * (100 + 1) = 1010
      const expectedPower = ethers.utils.parseEther("1010");
      expect(votingPower).to.equal(expectedPower);
    });

    it("should handle tranche funding with governance oversight", async function () {
      // Step 1: Create a tranche
      const amount = ethers.utils.parseEther("100");
      const milestoneHash = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("milestone1"));
      
      await trustlessFunding.connect(owner).createTranche(amount, milestoneHash);
      
      // Step 2: Seedbringer verifies ethical compliance
      await trustlessFunding.connect(seedbringer).verifyEthicalCompliance(0, true);
      
      const tranche = await trustlessFunding.tranches(0);
      expect(tranche.ethicallyCompliant).to.be.true;
      
      // Step 3: Release tranche with proof
      await trustlessFunding.connect(seedbringer).releaseTranche(0, milestoneHash);
      
      const updatedTranche = await trustlessFunding.tranches(0);
      expect(updatedTranche.released).to.be.true;
      
      // Step 4: Sync tranche distribution to governance
      await governance.connect(owner).syncTrancheDistribution(recipient.address, amount);
      
      const trancheDistribution = await governance.trancheDistributions(recipient.address);
      expect(trancheDistribution).to.equal(amount);
    });

    it("should verify Seedbringer authority across all contracts", async function () {
      // Verify Seedbringer address is consistent
      expect(await karmaBond.SEEDBRINGER()).to.equal(seedbringer.address);
      expect(await trustlessFunding.SEEDBRINGER()).to.equal(seedbringer.address);
      expect(await governance.SEEDBRINGER()).to.equal(seedbringer.address);
      
      // Verify Seedbringer name seal is consistent
      const expectedSeal = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("hannesmitterer"));
      expect(await karmaBond.SEEDBRINGER_NAME_SEAL()).to.equal(expectedSeal);
      expect(await trustlessFunding.SEEDBRINGER_NAME_SEAL()).to.equal(expectedSeal);
      expect(await governance.SEEDBRINGER_NAME_SEAL()).to.equal(expectedSeal);
    });

    it("should enforce Red Code principles in bond investments", async function () {
      const bondAmount = ethers.utils.parseEther("100");
      const duration = 180 * 24 * 60 * 60; // 180 days
      
      // Investment emits Red Code compliance check
      await expect(
        karmaBond.connect(investor).investWithDuration(duration, { value: bondAmount })
      ).to.emit(karmaBond, "RedCodeComplianceChecked")
        .withArgs(investor.address, true);
    });

    it("should demonstrate unified wallet management", async function () {
      // All contracts point to same foundation wallet
      expect(await karmaBond.foundationWallet()).to.equal(foundationWallet.address);
      expect(await trustlessFunding.foundationWallet()).to.equal(foundationWallet.address);
      
      // Verify initial balance
      const initialBalance = await ethers.provider.getBalance(foundationWallet.address);
      
      // Create and redeem a bond - fees go to foundation wallet
      const bondAmount = ethers.utils.parseEther("100");
      await karmaBond.connect(investor).investWithDuration(365 * 24 * 60 * 60, { value: bondAmount });
      
      // Set favorable invariants
      await karmaBond.setInvariants(5, 50);
      
      // Fast forward time
      await ethers.provider.send("evm_increaseTime", [366 * 24 * 60 * 60]);
      await ethers.provider.send("evm_mine");
      
      // Redeem - 5% fee goes to foundation wallet
      await karmaBond.redeem(investor.address);
      
      const finalBalance = await ethers.provider.getBalance(foundationWallet.address);
      const expectedFee = bondAmount.mul(5).div(100);
      
      // Foundation should have received the fee
      expect(finalBalance.sub(initialBalance)).to.equal(expectedFee);
    });
  });

  describe("Seedbringer Veto Power", function () {
    it("should allow Seedbringer to veto non-compliant tranches", async function () {
      const amount = ethers.utils.parseEther("100");
      const milestoneHash = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("milestone1"));
      
      // Create tranche
      await trustlessFunding.connect(owner).createTranche(amount, milestoneHash);
      
      // Seedbringer vetoes
      await trustlessFunding.connect(seedbringer).vetoTranche(0);
      
      const tranche = await trustlessFunding.tranches(0);
      expect(tranche.vetoed).to.be.true;
      
      // Cannot verify ethical compliance after veto
      await expect(
        trustlessFunding.connect(seedbringer).verifyEthicalCompliance(0, true)
      ).to.be.revertedWith("Tranche vetoed");
    });
  });

  describe("Future-proofing Mechanisms", function () {
    it("should support togglable sustainment mechanism", async function () {
      // Initially disabled
      expect(await governance.sustainmentEnabled()).to.be.false;
      
      // Only Seedbringer can toggle
      await governance.connect(seedbringer).toggleSustainment(true);
      expect(await governance.sustainmentEnabled()).to.be.true;
      
      // Can be disabled again
      await governance.connect(seedbringer).toggleSustainment(false);
      expect(await governance.sustainmentEnabled()).to.be.false;
    });

    it("should maintain constant sustainment amount for future use", async function () {
      const expectedAmount = ethers.utils.parseEther("10000");
      expect(await governance.SEEDBRINGER_SUSTAINMENT_MONTHLY()).to.equal(expectedAmount);
    });
  });
});
