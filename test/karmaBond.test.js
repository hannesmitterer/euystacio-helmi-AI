const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("KarmaBond", function () {
  let karmaBond;
  let owner, seedbringer, foundationWallet, investor1, investor2;

  beforeEach(async function () {
    [owner, seedbringer, foundationWallet, investor1, investor2] = await ethers.getSigners();
    
    const KarmaBond = await ethers.getContractFactory("KarmaBond");
    karmaBond = await KarmaBond.deploy(foundationWallet.address, seedbringer.address);
    await karmaBond.deployed();
  });

  describe("Deployment", function () {
    it("should set the correct foundation wallet", async function () {
      expect(await karmaBond.foundationWallet()).to.equal(foundationWallet.address);
    });

    it("should set the correct Seedbringer", async function () {
      expect(await karmaBond.SEEDBRINGER()).to.equal(seedbringer.address);
    });

    it("should compute correct Seedbringer name seal", async function () {
      const expectedSeal = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("hannesmitterer"));
      expect(await karmaBond.SEEDBRINGER_NAME_SEAL()).to.equal(expectedSeal);
    });
  });

  describe("Investment", function () {
    it("should allow investment with minimum contribution", async function () {
      const minContribution = ethers.utils.parseEther("100");
      await expect(
        karmaBond.connect(investor1).investWithDuration(365 * 24 * 60 * 60, { value: minContribution })
      ).to.emit(karmaBond, "InvestmentMade");
    });

    it("should reject investment below minimum contribution", async function () {
      const belowMin = ethers.utils.parseEther("50");
      await expect(
        karmaBond.connect(investor1).investWithDuration(365 * 24 * 60 * 60, { value: belowMin })
      ).to.be.revertedWith("Minimum contribution is $100 equivalent");
    });

    it("should emit RedCodeComplianceChecked event", async function () {
      const minContribution = ethers.utils.parseEther("100");
      await expect(
        karmaBond.connect(investor1).investWithDuration(365 * 24 * 60 * 60, { value: minContribution })
      ).to.emit(karmaBond, "RedCodeComplianceChecked");
    });

    it("should track bond with flexible duration", async function () {
      const amount = ethers.utils.parseEther("100");
      const duration = 180 * 24 * 60 * 60; // 180 days
      
      await karmaBond.connect(investor1).investWithDuration(duration, { value: amount });
      
      const bond = await karmaBond.bonds(investor1.address);
      expect(bond.amount).to.equal(amount);
      expect(bond.duration).to.equal(duration);
      expect(bond.isActive).to.be.true;
    });
  });

  describe("Redemption", function () {
    beforeEach(async function () {
      const amount = ethers.utils.parseEther("100");
      await karmaBond.connect(investor1).investWithDuration(365 * 24 * 60 * 60, { value: amount });
      
      // Set favorable invariants
      await karmaBond.setInvariants(5, 50); // MATL = 5%, R1 = 5.0%
    });

    it("should apply 5% redemption fee", async function () {
      const investedAmount = ethers.utils.parseEther("100");
      const expectedFee = investedAmount.mul(5).div(100); // 5% fee
      const expectedNet = investedAmount.sub(expectedFee);
      
      // Fast forward time to bond maturity
      await ethers.provider.send("evm_increaseTime", [366 * 24 * 60 * 60]);
      await ethers.provider.send("evm_mine");
      
      const initialFoundationBalance = await ethers.provider.getBalance(foundationWallet.address);
      
      await karmaBond.redeem(investor1.address);
      
      const finalFoundationBalance = await ethers.provider.getBalance(foundationWallet.address);
      expect(finalFoundationBalance.sub(initialFoundationBalance)).to.equal(expectedFee);
    });

    it("should return net funds when invariants met and bond matured", async function () {
      // Fast forward time to bond maturity
      await ethers.provider.send("evm_increaseTime", [366 * 24 * 60 * 60]);
      await ethers.provider.send("evm_mine");
      
      const initialBalance = await ethers.provider.getBalance(investor1.address);
      await karmaBond.redeem(investor1.address);
      const finalBalance = await ethers.provider.getBalance(investor1.address);
      
      // Should receive approximately 95 ETH (after 5% fee)
      const expected = ethers.utils.parseEther("95");
      expect(finalBalance.sub(initialBalance)).to.be.closeTo(expected, ethers.utils.parseEther("0.1"));
    });

    it("should redirect to foundation when invariants not met", async function () {
      // Set unfavorable invariants
      await karmaBond.setInvariants(20, 30); // MATL too high, R1 too low
      
      // Fast forward time
      await ethers.provider.send("evm_increaseTime", [366 * 24 * 60 * 60]);
      await ethers.provider.send("evm_mine");
      
      const initialFoundationBalance = await ethers.provider.getBalance(foundationWallet.address);
      await karmaBond.redeem(investor1.address);
      const finalFoundationBalance = await ethers.provider.getBalance(foundationWallet.address);
      
      // Foundation should receive full amount (original + net)
      const expected = ethers.utils.parseEther("100");
      expect(finalFoundationBalance.sub(initialFoundationBalance)).to.equal(expected);
    });
  });
});
