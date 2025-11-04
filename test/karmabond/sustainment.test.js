const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Sustainment", function () {
  let sustainment;
  let mockToken;
  let owner;
  let depositor;
  let user;

  const DECIMALS = 6;
  const MIN_USD = 10000;
  const MIN_SUSTAINMENT = MIN_USD * (10 ** DECIMALS); // 10,000 USDC

  beforeEach(async function () {
    [owner, depositor, user] = await ethers.getSigners();

    // Deploy mock ERC20 token (simulating USDC)
    const MockERC20 = await ethers.getContractFactory("MockERC20");
    mockToken = await MockERC20.deploy("Mock USDC", "USDC", DECIMALS);
    await mockToken.waitForDeployment();

    // Deploy Sustainment contract
    const Sustainment = await ethers.getContractFactory("Sustainment");
    sustainment = await Sustainment.deploy(
      await mockToken.getAddress(),
      DECIMALS,
      MIN_USD
    );
    await sustainment.waitForDeployment();

    // Mint tokens to users for testing
    await mockToken.mint(owner.address, ethers.parseUnits("100000", DECIMALS));
    await mockToken.mint(depositor.address, ethers.parseUnits("100000", DECIMALS));
    await mockToken.mint(user.address, ethers.parseUnits("100000", DECIMALS));
  });

  describe("Deployment", function () {
    it("Should set the correct stable token", async function () {
      expect(await sustainment.stableToken()).to.equal(await mockToken.getAddress());
    });

    it("Should set the correct decimals", async function () {
      expect(await sustainment.stableDecimals()).to.equal(DECIMALS);
    });

    it("Should set the correct minimum sustainment", async function () {
      expect(await sustainment.minSustainment()).to.equal(MIN_SUSTAINMENT);
    });

    it("Should start with zero reserve", async function () {
      expect(await sustainment.getSustainmentReserve()).to.equal(0);
    });

    it("Should not be above minimum initially", async function () {
      expect(await sustainment.isAboveMinimum()).to.be.false;
    });
  });

  describe("Authorization", function () {
    it("Should allow owner to authorize depositors", async function () {
      await sustainment.setAuthorizedDepositor(depositor.address, true);
      expect(await sustainment.authorizedDepositors(depositor.address)).to.be.true;
    });

    it("Should allow owner to revoke depositors", async function () {
      await sustainment.setAuthorizedDepositor(depositor.address, true);
      await sustainment.setAuthorizedDepositor(depositor.address, false);
      expect(await sustainment.authorizedDepositors(depositor.address)).to.be.false;
    });

    it("Should emit event when depositor is updated", async function () {
      await expect(sustainment.setAuthorizedDepositor(depositor.address, true))
        .to.emit(sustainment, "AuthorizedDepositorUpdated")
        .withArgs(depositor.address, true);
    });

    it("Should reject non-owner authorization attempts", async function () {
      await expect(
        sustainment.connect(user).setAuthorizedDepositor(depositor.address, true)
      ).to.be.revertedWith("Ownable: caller is not the owner");
    });
  });

  describe("Deposits", function () {
    beforeEach(async function () {
      await sustainment.setAuthorizedDepositor(depositor.address, true);
    });

    it("Should allow authorized depositor to deposit", async function () {
      const amount = ethers.parseUnits("5000", DECIMALS);
      await mockToken.connect(depositor).approve(await sustainment.getAddress(), amount);
      
      await expect(sustainment.connect(depositor).depositToSustainment(amount))
        .to.emit(sustainment, "SustainmentDeposited")
        .withArgs(depositor.address, amount);
      
      expect(await sustainment.getSustainmentReserve()).to.equal(amount);
    });

    it("Should allow owner to deposit", async function () {
      const amount = ethers.parseUnits("5000", DECIMALS);
      await mockToken.connect(owner).approve(await sustainment.getAddress(), amount);
      
      await sustainment.connect(owner).depositToSustainment(amount);
      expect(await sustainment.getSustainmentReserve()).to.equal(amount);
    });

    it("Should reject unauthorized deposits", async function () {
      const amount = ethers.parseUnits("5000", DECIMALS);
      await mockToken.connect(user).approve(await sustainment.getAddress(), amount);
      
      await expect(
        sustainment.connect(user).depositToSustainment(amount)
      ).to.be.revertedWith("Not authorized");
    });

    it("Should reject zero amount deposits", async function () {
      await expect(
        sustainment.connect(depositor).depositToSustainment(0)
      ).to.be.revertedWith("Amount must be positive");
    });

    it("Should emit threshold alert when depositing below minimum", async function () {
      const amount = ethers.parseUnits("5000", DECIMALS);
      await mockToken.connect(depositor).approve(await sustainment.getAddress(), amount);
      
      await expect(sustainment.connect(depositor).depositToSustainment(amount))
        .to.emit(sustainment, "SustainmentAlertNearThreshold")
        .withArgs(amount, MIN_SUSTAINMENT);
    });
  });

  describe("Bond Share Deposits", function () {
    beforeEach(async function () {
      await sustainment.setAuthorizedDepositor(depositor.address, true);
    });

    it("Should allow authorized contract to receive bond share", async function () {
      const amount = ethers.parseUnits("100", DECIMALS);
      
      // Transfer tokens first (simulating KarmaBond behavior)
      await mockToken.connect(depositor).transfer(await sustainment.getAddress(), amount);
      
      await expect(sustainment.connect(depositor).receiveShareFromBond(amount))
        .to.emit(sustainment, "SustainmentDeposited")
        .withArgs(depositor.address, amount);
      
      expect(await sustainment.getSustainmentReserve()).to.equal(amount);
    });

    it("Should reject unauthorized bond share deposits", async function () {
      const amount = ethers.parseUnits("100", DECIMALS);
      
      await expect(
        sustainment.connect(user).receiveShareFromBond(amount)
      ).to.be.revertedWith("Not authorized bond contract");
    });
  });

  describe("Minimum Sustainment", function () {
    it("Should allow owner to update minimum", async function () {
      const newMin = 15000;
      
      await expect(sustainment.setMinSustainment(newMin))
        .to.emit(sustainment, "MinSustainmentUpdated")
        .withArgs(MIN_SUSTAINMENT, newMin * (10 ** DECIMALS));
      
      expect(await sustainment.minSustainment()).to.equal(newMin * (10 ** DECIMALS));
    });

    it("Should reject non-owner minimum updates", async function () {
      await expect(
        sustainment.connect(user).setMinSustainment(15000)
      ).to.be.revertedWith("Ownable: caller is not the owner");
    });

    it("Should correctly report isAboveMinimum", async function () {
      await sustainment.setAuthorizedDepositor(depositor.address, true);
      
      // Below minimum
      expect(await sustainment.isAboveMinimum()).to.be.false;
      
      // Exactly at minimum
      await mockToken.connect(depositor).approve(await sustainment.getAddress(), MIN_SUSTAINMENT);
      await sustainment.connect(depositor).depositToSustainment(MIN_SUSTAINMENT);
      expect(await sustainment.isAboveMinimum()).to.be.true;
      
      // Above minimum
      const extra = ethers.parseUnits("1000", DECIMALS);
      await mockToken.connect(depositor).approve(await sustainment.getAddress(), extra);
      await sustainment.connect(depositor).depositToSustainment(extra);
      expect(await sustainment.isAboveMinimum()).to.be.true;
    });
  });

  describe("Withdrawals", function () {
    beforeEach(async function () {
      // Setup: deposit enough to be above minimum
      await sustainment.setAuthorizedDepositor(depositor.address, true);
      const amount = ethers.parseUnits("15000", DECIMALS);
      await mockToken.connect(depositor).approve(await sustainment.getAddress(), amount);
      await sustainment.connect(depositor).depositToSustainment(amount);
    });

    it("Should allow owner to withdraw", async function () {
      const withdrawAmount = ethers.parseUnits("1000", DECIMALS);
      const initialBalance = await mockToken.balanceOf(user.address);
      
      await expect(sustainment.withdrawSustainment(user.address, withdrawAmount))
        .to.emit(sustainment, "SustainmentWithdrawn")
        .withArgs(user.address, withdrawAmount);
      
      expect(await mockToken.balanceOf(user.address)).to.equal(
        initialBalance + withdrawAmount
      );
    });

    it("Should reject non-owner withdrawals", async function () {
      const withdrawAmount = ethers.parseUnits("1000", DECIMALS);
      
      await expect(
        sustainment.connect(user).withdrawSustainment(user.address, withdrawAmount)
      ).to.be.revertedWith("Ownable: caller is not the owner");
    });

    it("Should reject withdrawals exceeding reserve", async function () {
      const excessAmount = ethers.parseUnits("20000", DECIMALS);
      
      await expect(
        sustainment.withdrawSustainment(user.address, excessAmount)
      ).to.be.revertedWith("Insufficient reserve");
    });

    it("Should reject zero amount withdrawals", async function () {
      await expect(
        sustainment.withdrawSustainment(user.address, 0)
      ).to.be.revertedWith("Amount must be positive");
    });

    it("Should reject withdrawals to zero address", async function () {
      const withdrawAmount = ethers.parseUnits("1000", DECIMALS);
      
      await expect(
        sustainment.withdrawSustainment("0x0000000000000000000000000000000000000000", withdrawAmount)
      ).to.be.revertedWith("Invalid recipient");
    });
  });

  describe("Threshold Checks", function () {
    beforeEach(async function () {
      await sustainment.setAuthorizedDepositor(depositor.address, true);
    });

    it("Should check if would remain above minimum", async function () {
      const depositAmount = ethers.parseUnits("15000", DECIMALS);
      await mockToken.connect(depositor).approve(await sustainment.getAddress(), depositAmount);
      await sustainment.connect(depositor).depositToSustainment(depositAmount);
      
      // Small withdrawal should keep above minimum
      expect(
        await sustainment.wouldRemainAboveMinimum(ethers.parseUnits("1000", DECIMALS))
      ).to.be.true;
      
      // Large withdrawal would go below minimum
      expect(
        await sustainment.wouldRemainAboveMinimum(ethers.parseUnits("6000", DECIMALS))
      ).to.be.false;
    });

    it("Should emit alert when near threshold", async function () {
      // Deposit to just above minimum (within 5%)
      const amount = ethers.parseUnits("10100", DECIMALS); // 1% above minimum
      await mockToken.connect(depositor).approve(await sustainment.getAddress(), amount);
      
      await expect(sustainment.connect(depositor).depositToSustainment(amount))
        .to.emit(sustainment, "SustainmentAlertNearThreshold")
        .withArgs(amount, MIN_SUSTAINMENT);
    });
  });
});
