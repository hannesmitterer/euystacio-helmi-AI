const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("KarmaBond (Legacy)", function () {
  it("should deploy successfully", async function () {
    const [owner] = await ethers.getSigners();
    
    // Deploy mock token
    const MockERC20 = await ethers.getContractFactory("MockERC20");
    const mockToken = await MockERC20.deploy("Mock USDC", "USDC", 6);
    await mockToken.waitForDeployment();
    
    // Deploy Sustainment
    const Sustainment = await ethers.getContractFactory("Sustainment");
    const sustainment = await Sustainment.deploy(
      await mockToken.getAddress(),
      6,
      10000
    );
    await sustainment.waitForDeployment();
    
    // Deploy KarmaBond
    const KarmaBond = await ethers.getContractFactory("KarmaBond");
    const karmaBond = await KarmaBond.deploy(
      await mockToken.getAddress(),
      await sustainment.getAddress(),
      owner.address,
      200
    );
    await karmaBond.waitForDeployment();
    
    expect(await karmaBond.sustainmentPercent()).to.equal(200);
  });
});
