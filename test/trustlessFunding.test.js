const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("TrustlessFundingProtocol", function () {
  let protocol;
  let owner;
  let seedbringer;
  let recipient;
  let foundation;

  beforeEach(async function () {
    [owner, seedbringer, recipient, foundation] = await ethers.getSigners();
    
    const TrustlessFundingProtocol = await ethers.getContractFactory("TrustlessFundingProtocol");
    protocol = await TrustlessFundingProtocol.deploy(foundation.address, seedbringer.address);
    await protocol.waitForDeployment();
    
    // Fund the contract
    await owner.sendTransaction({
      to: await protocol.getAddress(),
      value: ethers.parseEther("10.0")
    });
  });

  it("should create a new tranche", async function () {
    const amount = ethers.parseEther("1.0");
    
    await expect(
      protocol.connect(owner).createTranche(recipient.address, amount)
    ).to.emit(protocol, "TrancheCreated")
      .withArgs(0, recipient.address, amount);
    
    const tranche = await protocol.tranches(0);
    expect(tranche.recipient).to.equal(recipient.address);
    expect(tranche.amount).to.equal(amount);
  });

  it("should allow Seedbringer to certify Red Code", async function () {
    const amount = ethers.parseEther("1.0");
    await protocol.connect(owner).createTranche(recipient.address, amount);
    
    await expect(
      protocol.connect(seedbringer).certifyRedCode(0, true)
    ).to.emit(protocol, "RedCodeCertified")
      .withArgs(0, true);
    
    const tranche = await protocol.tranches(0);
    expect(tranche.redCodeCertified).to.be.true;
  });

  it("should automatically release tranche when proof submitted and Red Code certified", async function () {
    const amount = ethers.parseEther("1.0");
    await protocol.connect(owner).createTranche(recipient.address, amount);
    
    // Certify Red Code first
    await protocol.connect(seedbringer).certifyRedCode(0, true);
    
    const proofHash = ethers.keccak256(ethers.toUtf8Bytes("milestone proof"));
    
    await expect(
      protocol.connect(owner).submitMilestoneProof(0, proofHash)
    ).to.emit(protocol, "TrancheReleased");
    
    const tranche = await protocol.tranches(0);
    expect(tranche.released).to.be.true;
  });

  it("should not release tranche without Red Code certification", async function () {
    const amount = ethers.parseEther("1.0");
    await protocol.connect(owner).createTranche(recipient.address, amount);
    
    const proofHash = ethers.keccak256(ethers.toUtf8Bytes("milestone proof"));
    
    // Should submit proof but not release
    await protocol.connect(owner).submitMilestoneProof(0, proofHash);
    
    const tranche = await protocol.tranches(0);
    expect(tranche.released).to.be.false;
  });

  it("should allow Seedbringer to manually release tranche", async function () {
    const amount = ethers.parseEther("1.0");
    await protocol.connect(owner).createTranche(recipient.address, amount);
    
    await expect(
      protocol.connect(seedbringer).seedbringerRelease(0)
    ).to.emit(protocol, "TrancheReleased");
    
    const tranche = await protocol.tranches(0);
    expect(tranche.released).to.be.true;
  });

  it("should allow Seedbringer to veto a tranche", async function () {
    const amount = ethers.parseEther("1.0");
    await protocol.connect(owner).createTranche(recipient.address, amount);
    
    await expect(
      protocol.connect(seedbringer).vetoTranche(0)
    ).to.emit(protocol, "TrancheVetoed")
      .withArgs(0, seedbringer.address);
    
    const tranche = await protocol.tranches(0);
    expect(tranche.vetoedBySeedbringer).to.be.true;
  });

  it("should prevent release of vetoed tranche", async function () {
    const amount = ethers.parseEther("1.0");
    await protocol.connect(owner).createTranche(recipient.address, amount);
    
    // Veto the tranche
    await protocol.connect(seedbringer).vetoTranche(0);
    
    // Try to submit proof
    const proofHash = ethers.keccak256(ethers.toUtf8Bytes("milestone proof"));
    await expect(
      protocol.connect(owner).submitMilestoneProof(0, proofHash)
    ).to.be.revertedWith("Vetoed by Seedbringer");
  });

  it("should prevent non-Seedbringer from certifying Red Code", async function () {
    const amount = ethers.parseEther("1.0");
    await protocol.connect(owner).createTranche(recipient.address, amount);
    
    await expect(
      protocol.connect(recipient).certifyRedCode(0, true)
    ).to.be.revertedWith("Only Seedbringer");
  });
});
