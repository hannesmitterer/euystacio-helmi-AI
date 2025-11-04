const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("EUSDaoGovernance", function () {
  let governance;
  let owner;
  let seedbringer;
  let user1;
  let user2;

  beforeEach(async function () {
    [owner, seedbringer, user1, user2] = await ethers.getSigners();
    
    const EUSDaoGovernance = await ethers.getContractFactory("EUSDaoGovernance");
    governance = await EUSDaoGovernance.deploy(seedbringer.address);
    await governance.waitForDeployment();
  });

  it("should allow Seedbringer to mint tokens", async function () {
    const amount = ethers.parseEther("1000");
    
    await expect(
      governance.connect(seedbringer).mint(user1.address, amount)
    ).to.emit(governance, "Transfer")
      .withArgs(ethers.ZeroAddress, user1.address, amount);
    
    expect(await governance.balanceOf(user1.address)).to.equal(amount);
  });

  it("should prevent non-Seedbringer from minting", async function () {
    const amount = ethers.parseEther("1000");
    
    await expect(
      governance.connect(user1).mint(user1.address, amount)
    ).to.be.revertedWith("Only Seedbringer");
  });

  it("should allow Seedbringer to set contribution scores", async function () {
    const score = 100;
    
    await expect(
      governance.connect(seedbringer).setContributionScore(user1.address, score)
    ).to.emit(governance, "ContributionScoreUpdated")
      .withArgs(user1.address, score);
    
    const metrics = await governance.getContributionMetrics(user1.address);
    expect(metrics.score).to.equal(score);
    expect(metrics.active).to.be.true;
  });

  it("should calculate voting power correctly with contribution scores", async function () {
    const tokenAmount = ethers.parseEther("1000");
    const score = 10; // 10 contribution points
    
    // Mint tokens
    await governance.connect(seedbringer).mint(user1.address, tokenAmount);
    
    // Set contribution score
    await governance.connect(seedbringer).setContributionScore(user1.address, score);
    
    // Voting power = balance * (1 + (score * 0.01))
    // = 1000 * (1 + (10 * 0.01)) = 1000 * 1.1 = 1100
    const expectedPower = tokenAmount * BigInt(10000 + (score * 100)) / 10000n;
    const actualPower = await governance.votingPower(user1.address);
    
    expect(actualPower).to.equal(expectedPower);
  });

  it("should allow Seedbringer to recalibrate contributions", async function () {
    const newScore = 50;
    const totalContributions = 10;
    
    await expect(
      governance.connect(seedbringer).recalibrateContribution(
        user1.address, 
        newScore, 
        totalContributions
      )
    ).to.emit(governance, "ContributionRecalibrated")
      .withArgs(user1.address, newScore);
    
    const metrics = await governance.getContributionMetrics(user1.address);
    expect(metrics.score).to.equal(newScore);
    expect(metrics.totalContributions).to.equal(totalContributions);
  });

  it("should allow Seedbringer to batch update scores", async function () {
    const users = [user1.address, user2.address];
    const scores = [100, 200];
    
    await governance.connect(seedbringer).batchUpdateScores(users, scores);
    
    const metrics1 = await governance.getContributionMetrics(user1.address);
    const metrics2 = await governance.getContributionMetrics(user2.address);
    
    expect(metrics1.score).to.equal(100);
    expect(metrics2.score).to.equal(200);
  });

  it("should allow Seedbringer to execute governance actions", async function () {
    const action = "Implement new protocol upgrade";
    
    await expect(
      governance.connect(seedbringer).executeGovernanceAction(action)
    ).to.emit(governance, "GovernanceActionExecuted")
      .withArgs(seedbringer.address, action);
  });

  it("should allow Seedbringer to deactivate contributors", async function () {
    // First activate by setting score
    await governance.connect(seedbringer).setContributionScore(user1.address, 100);
    
    let metrics = await governance.getContributionMetrics(user1.address);
    expect(metrics.active).to.be.true;
    
    // Deactivate
    await governance.connect(seedbringer).deactivateContributor(user1.address);
    
    metrics = await governance.getContributionMetrics(user1.address);
    expect(metrics.active).to.be.false;
  });

  it("should allow Seedbringer to update Seedbringer address", async function () {
    await expect(
      governance.connect(seedbringer).updateSeedbringer(user1.address)
    ).to.emit(governance, "SeedbringerUpdated")
      .withArgs(user1.address);
    
    expect(await governance.seedbringer()).to.equal(user1.address);
  });

  it("should allow owner to perform admin mint", async function () {
    const amount = ethers.parseEther("500");
    
    await governance.connect(owner).adminMint(user1.address, amount);
    expect(await governance.balanceOf(user1.address)).to.equal(amount);
  });

  it("should allow users to burn their own tokens", async function () {
    const amount = ethers.parseEther("1000");
    const burnAmount = ethers.parseEther("300");
    
    await governance.connect(seedbringer).mint(user1.address, amount);
    
    await governance.connect(user1).burn(burnAmount);
    expect(await governance.balanceOf(user1.address)).to.equal(amount - burnAmount);
  });

  it("should calculate voting power as balance only for inactive contributors", async function () {
    const tokenAmount = ethers.parseEther("1000");
    
    await governance.connect(seedbringer).mint(user1.address, tokenAmount);
    
    // Without active contribution metrics, voting power equals balance
    const votingPower = await governance.votingPower(user1.address);
    expect(votingPower).to.equal(tokenAmount);
  });
});
