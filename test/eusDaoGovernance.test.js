const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("EUSDaoGovernance", function () {
  let governance;
  let seedbringer;
  let user1;
  let user2;

  beforeEach(async function () {
    [seedbringer, user1, user2] = await ethers.getSigners();
    
    const EUSDaoGovernance = await ethers.getContractFactory("EUSDaoGovernance");
    governance = await EUSDaoGovernance.deploy(seedbringer.address);
    await governance.waitForDeployment();
  });

  it("should verify Seedbringer seal is keccak256('hannesmitterer')", async function () {
    const expectedSeal = ethers.keccak256(ethers.toUtf8Bytes("hannesmitterer"));
    expect(await governance.SEEDBRINGER_SEAL()).to.equal(expectedSeal);
  });

  it("should set Seedbringer as owner", async function () {
    expect(await governance.owner()).to.equal(seedbringer.address);
    expect(await governance.seedbringerAddress()).to.equal(seedbringer.address);
  });

  it("should only allow Seedbringer to mint tokens", async function () {
    const mintAmount = ethers.parseEther("100");
    
    await expect(
      governance.connect(user1).mint(user1.address, mintAmount)
    ).to.be.revertedWith("Only Seedbringer can call");
    
    await expect(
      governance.connect(seedbringer).mint(user1.address, mintAmount)
    ).to.not.be.reverted;
    
    expect(await governance.balanceOf(user1.address)).to.equal(mintAmount);
  });

  it("should only allow Seedbringer to set contribution scores", async function () {
    await expect(
      governance.connect(user1).setContributionScore(user1.address, 5)
    ).to.be.revertedWith("Only Seedbringer can call");
    
    await expect(
      governance.connect(seedbringer).setContributionScore(user1.address, 5)
    ).to.emit(governance, "ContributionScoreUpdated")
      .withArgs(user1.address, 5);
    
    expect(await governance.contributionScore(user1.address)).to.equal(5);
  });

  it("should calculate voting power correctly", async function () {
    const mintAmount = ethers.parseEther("100");
    const contributionScore = 2;
    
    await governance.connect(seedbringer).mint(user1.address, mintAmount);
    await governance.connect(seedbringer).setContributionScore(user1.address, contributionScore);
    
    // Voting power = balance * (1 + contributionScore)
    const expectedVotingPower = mintAmount * BigInt(1 + contributionScore);
    expect(await governance.votingPower(user1.address)).to.equal(expectedVotingPower);
  });

  it("should support batch setting contribution scores", async function () {
    const users = [user1.address, user2.address];
    const scores = [3, 5];
    
    await governance.connect(seedbringer).batchSetContributionScores(users, scores);
    
    expect(await governance.contributionScore(user1.address)).to.equal(3);
    expect(await governance.contributionScore(user2.address)).to.equal(5);
  });

  it("should revert batch set with mismatched arrays", async function () {
    const users = [user1.address, user2.address];
    const scores = [3]; // Mismatched length
    
    await expect(
      governance.connect(seedbringer).batchSetContributionScores(users, scores)
    ).to.be.revertedWith("Array length mismatch");
  });

  it("should allow Seedbringer to update their address", async function () {
    await expect(
      governance.connect(seedbringer).updateSeedbringer(user1.address)
    ).to.emit(governance, "SeedbringerUpdated")
      .withArgs(seedbringer.address, user1.address);
    
    expect(await governance.seedbringerAddress()).to.equal(user1.address);
    expect(await governance.owner()).to.equal(user1.address);
  });

  it("should only allow current Seedbringer to update address", async function () {
    await expect(
      governance.connect(user1).updateSeedbringer(user1.address)
    ).to.be.revertedWith("Only Seedbringer can call");
  });

  it("should return governance info correctly", async function () {
    const mintAmount = ethers.parseEther("100");
    const contributionScore = 3;
    
    await governance.connect(seedbringer).mint(user1.address, mintAmount);
    await governance.connect(seedbringer).setContributionScore(user1.address, contributionScore);
    
    const info = await governance.getGovernanceInfo(user1.address);
    expect(info.balance).to.equal(mintAmount);
    expect(info.contribution).to.equal(contributionScore);
    expect(info.voting).to.equal(mintAmount * BigInt(1 + contributionScore));
  });
});
