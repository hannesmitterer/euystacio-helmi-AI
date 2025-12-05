const { expect } = require("chai");
const { ethers } = require("hardhat");

// NOTE: These tests are for an ERC20-based KarmaBond contract implementation.
// The current KarmaBond contract uses native ETH with Seedbringer authority.
// These tests are skipped pending migration to the new contract interface.
describe.skip("KarmaBond Integration", function () {
  let karmaBond;
  let sustainment;
  let mockToken;
  let owner;
  let foundation;
  let investor;

  const DECIMALS = 6;
  const MIN_USD = 10000;
  const SUSTAINMENT_PERCENT = 200; // 2%

  beforeEach(async function () {
    [owner, foundation, investor] = await ethers.getSigners();

    // Deploy mock ERC20 token
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

    // Authorize KarmaBond in Sustainment
    await sustainment.setAuthorizedDepositor(await karmaBond.getAddress(), true);

    // Mint tokens to investors
    await mockToken.mint(investor.address, ethers.parseUnits("100000", DECIMALS));
  });

  describe("Bond Minting", function () {
    it("Should mint bonds and allocate sustainment share", async function () {
      const mintAmount = ethers.parseUnits("1000", DECIMALS);
      const expectedSustainment = mintAmount * BigInt(SUSTAINMENT_PERCENT) / 10000n;
      const expectedReserve = mintAmount - expectedSustainment;

      await mockToken.connect(investor).approve(await karmaBond.getAddress(), mintAmount);

      await expect(karmaBond.connect(investor).mintBond(mintAmount))
        .to.emit(karmaBond, "BondMinted")
        .withArgs(investor.address, mintAmount, mintAmount)
        .to.emit(karmaBond, "SustainmentAllocated")
        .withArgs(investor.address, mintAmount, expectedSustainment);

      expect(await karmaBond.bondBalances(investor.address)).to.equal(mintAmount);
      expect(await karmaBond.stableReserve()).to.equal(expectedReserve);
      expect(await sustainment.getSustainmentReserve()).to.equal(expectedSustainment);
    });

    it("Should handle zero sustainment allocation", async function () {
      // Set sustainment to 0%
      await karmaBond.setSustainmentPercent(0);

      const mintAmount = ethers.parseUnits("1000", DECIMALS);
      await mockToken.connect(investor).approve(await karmaBond.getAddress(), mintAmount);
      
      await karmaBond.connect(investor).mintBond(mintAmount);

      expect(await karmaBond.stableReserve()).to.equal(mintAmount);
      expect(await sustainment.getSustainmentReserve()).to.equal(0);
    });

    it("Should reject minting with zero amount", async function () {
      await expect(
        karmaBond.connect(investor).mintBond(0)
      ).to.be.revertedWith("Amount must be positive");
    });

    it("Should accumulate multiple mints", async function () {
      const mintAmount = ethers.parseUnits("1000", DECIMALS);
      
      await mockToken.connect(investor).approve(await karmaBond.getAddress(), mintAmount * 3n);
      
      await karmaBond.connect(investor).mintBond(mintAmount);
      await karmaBond.connect(investor).mintBond(mintAmount);
      await karmaBond.connect(investor).mintBond(mintAmount);

      const expectedBonds = mintAmount * 3n;
      const expectedSustainment = expectedBonds * BigInt(SUSTAINMENT_PERCENT) / 10000n;

      expect(await karmaBond.bondBalances(investor.address)).to.equal(expectedBonds);
      expect(await sustainment.getSustainmentReserve()).to.equal(expectedSustainment);
    });
  });

  describe("Bond Redemption", function () {
    beforeEach(async function () {
      // Mint some bonds first
      const mintAmount = ethers.parseUnits("10000", DECIMALS);
      await mockToken.connect(investor).approve(await karmaBond.getAddress(), mintAmount);
      await karmaBond.connect(investor).mintBond(mintAmount);
      
      // Set favorable invariants for redemption
      await karmaBond.setInvariants(10, 45n);
    });

    it("Should redeem bonds when invariants are met", async function () {
      const redeemAmount = ethers.parseUnits("5000", DECIMALS);
      const expectedPayout = redeemAmount - redeemAmount * BigInt(SUSTAINMENT_PERCENT) / 10000n;

      const initialBalance = await mockToken.balanceOf(investor.address);

      await expect(karmaBond.redeemBond(investor.address, redeemAmount))
        .to.emit(karmaBond, "BondRedeemed")
        .withArgs(investor.address, redeemAmount, expectedPayout);

      expect(await mockToken.balanceOf(investor.address)).to.equal(
        initialBalance + expectedPayout
      );
    });

    it("Should redirect to foundation when invariants violated", async function () {
      // Set unfavorable invariants
      await karmaBond.setInvariants(50, 10n);

      const redeemAmount = ethers.parseUnits("5000", DECIMALS);
      const expectedPayout = redeemAmount - redeemAmount * BigInt(SUSTAINMENT_PERCENT) / 10000n;

      const initialFoundationBalance = await mockToken.balanceOf(foundation.address);

      await karmaBond.redeemBond(investor.address, redeemAmount);

      expect(await mockToken.balanceOf(foundation.address)).to.equal(
        initialFoundationBalance + expectedPayout
      );
    });

    it("Should reject redemption exceeding balance", async function () {
      const excessAmount = ethers.parseUnits("20000", DECIMALS);

      await expect(
        karmaBond.redeemBond(investor.address, excessAmount)
      ).to.be.revertedWith("Insufficient bond balance");
    });

    it("Should reject redemption by non-owner", async function () {
      const redeemAmount = ethers.parseUnits("1000", DECIMALS);

      await expect(
        karmaBond.connect(investor).redeemBond(investor.address, redeemAmount)
      ).to.be.revertedWith("Ownable: caller is not the owner");
    });
  });

  describe("Sustainment Configuration", function () {
    it("Should allow owner to change sustainment percent", async function () {
      const newPercent = 300n; // 3%

      await expect(karmaBond.setSustainmentPercent(newPercent))
        .to.emit(karmaBond, "SustainmentPercentUpdated")
        .withArgs(SUSTAINMENT_PERCENT, newPercent);

      expect(await karmaBond.sustainmentPercent()).to.equal(newPercent);
    });

    it("Should reject sustainment percent over 100%", async function () {
      await expect(
        karmaBond.setSustainmentPercent(10001)
      ).to.be.revertedWith("Percent exceeds 100%");
    });

    it("Should allow owner to change sustainment contract", async function () {
      const newSustainment = ethers.Wallet.createRandom().address;

      await expect(karmaBond.setSustainmentContract(newSustainment))
        .to.emit(karmaBond, "SustainmentContractUpdated")
        .withArgs(await sustainment.getAddress(), newSustainment);

      expect(await karmaBond.sustainmentContract()).to.equal(newSustainment);
    });
  });

  describe("Excess Withdrawals", function () {
    it("Should not allow withdrawing bond reserves", async function () {
      const mintAmount = ethers.parseUnits("10000", DECIMALS);
      await mockToken.connect(investor).approve(await karmaBond.getAddress(), mintAmount);
      await karmaBond.connect(investor).mintBond(mintAmount);

      const reserve = await karmaBond.stableReserve();

      await expect(
        karmaBond.withdrawExcessStable(owner.address, reserve)
      ).to.be.revertedWith("Amount exceeds excess reserves");
    });

    it("Should allow withdrawing excess (accidentally sent tokens)", async function () {
      // Send extra tokens directly to contract
      const extraAmount = ethers.parseUnits("1000", DECIMALS);
      await mockToken.mint(await karmaBond.getAddress(), extraAmount);

      await karmaBond.withdrawExcessStable(owner.address, extraAmount);
      expect(await mockToken.balanceOf(owner.address)).to.equal(extraAmount);
    });
  });

  describe("Edge Cases", function () {
    it("Should handle tiny amounts that compute to zero sustainment", async function () {
      // Set high sustainment percent for testing
      await karmaBond.setSustainmentPercent(200);

      // Mint tiny amount (1 base unit)
      const tinyAmount = 1n;
      await mockToken.mint(investor.address, tinyAmount);
      await mockToken.connect(investor).approve(await karmaBond.getAddress(), tinyAmount);
      
      await karmaBond.connect(investor).mintBond(tinyAmount);

      // Should still work, sustainment share rounds to 0
      expect(await karmaBond.bondBalances(investor.address)).to.equal(tinyAmount);
    });

    it("Should handle maximum sustainment percent (100%)", async function () {
      await karmaBond.setSustainmentPercent(10000); // 100%

      const mintAmount = ethers.parseUnits("1000", DECIMALS);
      await mockToken.connect(investor).approve(await karmaBond.getAddress(), mintAmount);
      
      await karmaBond.connect(investor).mintBond(mintAmount);

      // All goes to sustainment
      expect(await sustainment.getSustainmentReserve()).to.equal(mintAmount);
      expect(await karmaBond.stableReserve()).to.equal(0);
    });
  });
});
