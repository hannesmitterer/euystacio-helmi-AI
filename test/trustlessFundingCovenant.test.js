const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("TrustlessFundingProtocol_Covenant", function () {
  let covenant;
  let owner;
  let oracle;
  let seedbringer;
  let foundationWallet;
  let recipient;

  beforeEach(async function () {
    [owner, oracle, seedbringer, foundationWallet, recipient] = await ethers.getSigners();
    
    const TrustlessFundingProtocol_Covenant = await ethers.getContractFactory("TrustlessFundingProtocol_Covenant");
    covenant = await TrustlessFundingProtocol_Covenant.deploy(
      oracle.address,
      foundationWallet.address,
      seedbringer.address
    );
    await covenant.deployed();
  });

  it("should verify Seedbringer seal is keccak256('hannesmitterer')", async function () {
    const expectedSeal = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("hannesmitterer"));
    expect(await covenant.SEEDBRINGER_NAME_SEAL()).to.equal(expectedSeal);
  });

  it("should initialize project with tranches", async function () {
    const trancheAmounts = [
      ethers.utils.parseEther("1.0"),
      ethers.utils.parseEther("2.0"),
      ethers.utils.parseEther("1.5")
    ];
    const milestoneHashes = [
      ethers.utils.keccak256(ethers.utils.toUtf8Bytes("milestone-1")),
      ethers.utils.keccak256(ethers.utils.toUtf8Bytes("milestone-2")),
      ethers.utils.keccak256(ethers.utils.toUtf8Bytes("milestone-3"))
    ];
    
    await expect(
      covenant.connect(oracle).initializeProject(recipient.address, trancheAmounts, milestoneHashes)
    ).to.emit(covenant, "ProjectInitialized");
    
    const projectDetails = await covenant.getProjectDetails(0);
    expect(projectDetails.recipient).to.equal(recipient.address);
    expect(projectDetails.totalBudget).to.equal(
      ethers.utils.parseEther("4.5")
    );
  });

  it("should require Red Code compliance for tranche release", async function () {
    const trancheAmounts = [ethers.utils.parseEther("1.0")];
    const milestoneHashes = [ethers.utils.keccak256(ethers.utils.toUtf8Bytes("milestone-1"))];
    
    await covenant.connect(oracle).initializeProject(recipient.address, trancheAmounts, milestoneHashes);
    
    // Fund the contract
    await owner.sendTransaction({
      to: covenant.address,
      value: ethers.utils.parseEther("1.0")
    });
    
    // Try to release without Red Code compliance
    await expect(
      covenant.connect(oracle).releaseTranche(0, milestoneHashes[0])
    ).to.be.revertedWith("Red Code compliance not verified");
  });

  it("should automatically release tranche upon verified milestone and Red Code compliance", async function () {
    const trancheAmounts = [ethers.utils.parseEther("1.0")];
    const milestoneHashes = [ethers.utils.keccak256(ethers.utils.toUtf8Bytes("milestone-1"))];
    
    await covenant.connect(oracle).initializeProject(recipient.address, trancheAmounts, milestoneHashes);
    
    // Fund the contract
    await owner.sendTransaction({
      to: covenant.address,
      value: ethers.utils.parseEther("1.0")
    });
    
    // Set Red Code compliance
    await covenant.connect(oracle).updateRedCodeCompliance(0, true);
    
    const recipientBalanceBefore = await recipient.getBalance();
    
    // Release tranche
    await expect(
      covenant.connect(oracle).releaseTranche(0, milestoneHashes[0])
    ).to.emit(covenant, "TrancheReleased")
      .withArgs(0, 0, ethers.utils.parseEther("1.0"));
    
    const recipientBalanceAfter = await recipient.getBalance();
    expect(recipientBalanceAfter.sub(recipientBalanceBefore)).to.equal(
      ethers.utils.parseEther("1.0")
    );
  });

  it("should allow Seedbringer to override and release tranche", async function () {
    const trancheAmounts = [ethers.utils.parseEther("1.0")];
    const milestoneHashes = [ethers.utils.keccak256(ethers.utils.toUtf8Bytes("milestone-1"))];
    
    await covenant.connect(oracle).initializeProject(recipient.address, trancheAmounts, milestoneHashes);
    
    // Fund the contract
    await owner.sendTransaction({
      to: covenant.address,
      value: ethers.utils.parseEther("1.0")
    });
    
    const recipientBalanceBefore = await recipient.getBalance();
    
    // Seedbringer override
    await expect(
      covenant.connect(seedbringer).seedbringerOverrideTranche(0, 0, true)
    ).to.emit(covenant, "SeedbringerOverride");
    
    const recipientBalanceAfter = await recipient.getBalance();
    expect(recipientBalanceAfter.sub(recipientBalanceBefore)).to.equal(
      ethers.utils.parseEther("1.0")
    );
  });

  it("should only allow Seedbringer to use override functions", async function () {
    const trancheAmounts = [ethers.utils.parseEther("1.0")];
    const milestoneHashes = [ethers.utils.keccak256(ethers.utils.toUtf8Bytes("milestone-1"))];
    
    await covenant.connect(oracle).initializeProject(recipient.address, trancheAmounts, milestoneHashes);
    
    await expect(
      covenant.connect(owner).seedbringerOverrideTranche(0, 0, true)
    ).to.be.revertedWith("Only Seedbringer can call");
  });

  it("should verify milestone proof matches expected hash", async function () {
    const trancheAmounts = [ethers.utils.parseEther("1.0")];
    const correctHash = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("milestone-1"));
    const wrongHash = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("wrong-milestone"));
    
    await covenant.connect(oracle).initializeProject(recipient.address, trancheAmounts, [correctHash]);
    
    // Fund the contract
    await owner.sendTransaction({
      to: covenant.address,
      value: ethers.utils.parseEther("1.0")
    });
    
    // Set Red Code compliance
    await covenant.connect(oracle).updateRedCodeCompliance(0, true);
    
    // Try with wrong proof
    await expect(
      covenant.connect(oracle).releaseTranche(0, wrongHash)
    ).to.be.revertedWith("Milestone proof does not match");
  });
});
