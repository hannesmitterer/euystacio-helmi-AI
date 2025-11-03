const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("KarmaBond", function () {
  let karmaBond;
  let owner;
  let investor1;
  let investor2;
  let foundationWallet;
  const initialEthPrice = ethers.utils.parseUnits("2000", 2); // 2000 USD in cents

  beforeEach(async function () {
    [owner, investor1, investor2, foundationWallet] = await ethers.getSigners();
    
    const KarmaBond = await ethers.getContractFactory("KarmaBond");
    karmaBond = await KarmaBond.deploy(foundationWallet.address, initialEthPrice);
    await karmaBond.deployed();
  });

  it("should enforce minimum investment of 100 USD", async function () {
    // Try to invest less than 100 USD (0.01 ETH at 2000 USD/ETH = 20 USD)
    const tooSmall = ethers.utils.parseEther("0.01");
    
    await expect(
      karmaBond.connect(investor1).invest(0, { value: tooSmall })
    ).to.be.revertedWith("Minimum investment is 100 USD");
  });

  it("should allow investment above minimum", async function () {
    // Invest 0.1 ETH at 2000 USD/ETH = 200 USD
    const validAmount = ethers.utils.parseEther("0.1");
    
    await expect(
      karmaBond.connect(investor1).invest(0, { value: validAmount })
    ).to.emit(karmaBond, "InvestmentMade")
      .withArgs(investor1.address, validAmount, 0);
    
    const bond = await karmaBond.bonds(investor1.address);
    expect(bond.amount).to.equal(validAmount);
  });

  it("should support flexible duration", async function () {
    const amount = ethers.utils.parseEther("0.1");
    const duration = 86400; // 1 day
    
    await karmaBond.connect(investor1).invest(duration, { value: amount });
    
    const bond = await karmaBond.bonds(investor1.address);
    expect(bond.duration).to.equal(duration);
  });

  it("should apply 5% redemption fee when Red Code compliant", async function () {
    const amount = ethers.utils.parseEther("1.0");
    await karmaBond.connect(investor1).invest(0, { value: amount });
    
    // Set Red Code compliant invariants
    await karmaBond.setInvariants(10, 45);
    
    const initialBalance = await investor1.getBalance();
    const initialFoundationBalance = await foundationWallet.getBalance();
    
    await karmaBond.redeem(investor1.address);
    
    const finalBalance = await investor1.getBalance();
    const finalFoundationBalance = await foundationWallet.getBalance();
    
    // Check that investor received 95% of investment
    const expectedNet = amount.mul(95).div(100);
    const expectedFee = amount.mul(5).div(100);
    
    expect(finalBalance.sub(initialBalance)).to.equal(expectedNet);
    expect(finalFoundationBalance.sub(initialFoundationBalance)).to.equal(expectedFee);
  });

  it("should redirect all funds to foundation when Red Code not compliant", async function () {
    const amount = ethers.utils.parseEther("1.0");
    await karmaBond.connect(investor1).invest(0, { value: amount });
    
    // Set Red Code non-compliant invariants
    await karmaBond.setInvariants(50, 10);
    
    const initialFoundationBalance = await foundationWallet.getBalance();
    
    await karmaBond.redeem(investor1.address);
    
    const finalFoundationBalance = await foundationWallet.getBalance();
    
    // All funds should go to foundation
    expect(finalFoundationBalance.sub(initialFoundationBalance)).to.equal(amount);
  });

  it("should respect lock duration", async function () {
    const amount = ethers.utils.parseEther("0.1");
    const duration = 86400; // 1 day
    
    await karmaBond.connect(investor1).invest(duration, { value: amount });
    
    // Set Red Code compliant
    await karmaBond.setInvariants(10, 45);
    
    // Try to redeem immediately - should fail
    await expect(
      karmaBond.redeem(investor1.address)
    ).to.be.revertedWith("Lock period not elapsed");
  });
});
