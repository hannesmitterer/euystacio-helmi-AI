const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("TrustlessFundingProtocol (Legacy)", function () {
  it("should deploy and configure successfully", async function () {
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
    
    // Deploy TrustlessFundingProtocol
    const TFP = await ethers.getContractFactory("TrustlessFundingProtocol");
    const tfp = await TFP.deploy(owner.address);
    await tfp.waitForDeployment();
    
    await tfp.setSustainmentContract(await sustainment.getAddress());
    
    expect(await tfp.sustainmentContract()).to.equal(await sustainment.getAddress());
    expect(await tfp.governanceEnforced()).to.be.true;
  });
});
