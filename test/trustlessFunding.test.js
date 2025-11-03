const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("TrustlessFundingProtocol", function () {
  let protocol;
  let owner;
  let foundationWallet;

  beforeEach(async function () {
    [owner, foundationWallet] = await ethers.getSigners();
    
    const TrustlessFundingProtocol = await ethers.getContractFactory("TrustlessFundingProtocol");
    protocol = await TrustlessFundingProtocol.deploy(foundationWallet.address);
    await protocol.deployed();
  });

  it("should require Red Code compliance before releasing tranche", async function () {
    const trancheId = 1;
    const proofHash = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("milestone-proof"));
    
    // Try to release without Red Code compliance
    await expect(
      protocol.releaseTranche(trancheId, proofHash)
    ).to.be.revertedWith("Red Code compliance not verified");
  });

  it("should release tranche with proof and Red Code compliance", async function () {
    const trancheId = 1;
    const proofHash = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("milestone-proof"));
    
    // Set Red Code compliance
    await protocol.updateRedCodeCompliance(trancheId, true);
    
    // Release tranche
    await expect(
      protocol.releaseTranche(trancheId, proofHash)
    ).to.emit(protocol, "TrancheReleased")
      .withArgs(trancheId, proofHash, await ethers.provider.getBlock("latest").then(b => b.timestamp + 1));
    
    expect(await protocol.trancheReleased(trancheId)).to.be.true;
  });

  it("should not allow releasing same tranche twice", async function () {
    const trancheId = 1;
    const proofHash = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("milestone-proof"));
    
    await protocol.updateRedCodeCompliance(trancheId, true);
    await protocol.releaseTranche(trancheId, proofHash);
    
    await expect(
      protocol.releaseTranche(trancheId, proofHash)
    ).to.be.revertedWith("Already released");
  });
});
