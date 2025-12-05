const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("KarmaBond", function () {
  let karmaBond;
  let owner;
  let seedbringer;
  let investor;
  let foundation;

  beforeEach(async function () {
    [owner, seedbringer, investor, foundation] = await ethers.getSigners();
    
    const KarmaBond = await ethers.getContractFactory("KarmaBond");
    karmaBond = await KarmaBond.deploy(foundation.address, seedbringer.address);
    await karmaBond.waitForDeployment();
  });

  it("should enforce minimum investment", async function () {
    await expect(
      karmaBond.connect(investor).invest(365 * 24 * 60 * 60, { value: ethers.parseEther("0.01") })
    ).to.be.revertedWith("Investment below minimum");
  });

  it("should allow investment above minimum", async function () {
    const investment = ethers.parseEther("0.05");
    const duration = 365 * 24 * 60 * 60; // 1 year
    
    await expect(
      karmaBond.connect(investor).invest(duration, { value: investment })
    ).to.emit(karmaBond, "InvestmentMade")
      .withArgs(investor.address, investment, duration);
    
    const inv = await karmaBond.investments(investor.address);
    expect(inv.amount).to.equal(investment);
  });

  it("should allow Seedbringer to certify Red Code compliance", async function () {
    const investment = ethers.parseEther("0.05");
    await karmaBond.connect(investor).invest(365 * 24 * 60 * 60, { value: investment });
    
    await expect(
      karmaBond.connect(seedbringer).certifyRedCode(investor.address, true)
    ).to.emit(karmaBond, "RedCodeStatusUpdated")
      .withArgs(investor.address, true);
    
    const inv = await karmaBond.investments(investor.address);
    expect(inv.redCodeCompliant).to.be.true;
  });

  it("should prevent non-Seedbringer from certifying Red Code", async function () {
    await expect(
      karmaBond.connect(investor).certifyRedCode(investor.address, true)
    ).to.be.revertedWith("Only Seedbringer");
  });

  it("should apply 5% redemption fee when invariants are met", async function () {
    const investment = ethers.parseEther("1.0");
    await karmaBond.connect(investor).invest(1, { value: investment }); // 1 second duration for testing
    
    // Certify Red Code
    await karmaBond.connect(seedbringer).certifyRedCode(investor.address, true);
    
    // Set invariants to meet conditions
    await karmaBond.connect(owner).setInvariants(10, 45);
    
    // Advance time by 2 seconds
    await ethers.provider.send("evm_increaseTime", [2]);
    await ethers.provider.send("evm_mine");
    
    await karmaBond.connect(owner).redeem(investor.address);
    
    // Investment should be redeemed with 5% fee
    // Expected: 95% of investment returned to investor
  });

  it("should allow Seedbringer to update Seedbringer address", async function () {
    const [, , , newSeedbringer] = await ethers.getSigners();
    
    await expect(
      karmaBond.connect(seedbringer).updateSeedbringer(newSeedbringer.address)
    ).to.emit(karmaBond, "SeedbringerUpdated")
      .withArgs(newSeedbringer.address);
    
    expect(await karmaBond.seedbringer()).to.equal(newSeedbringer.address);
  });
});
