const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("EuystacioSTAnchor", function () {
  let anchor;
  let owner, council1, council2, council3, nonCouncil;
  const rootCommit = ethers.keccak256(ethers.toUtf8Bytes("ROOT-ETERNAL-C48B2A7"));

  beforeEach(async function () {
    [owner, council1, council2, council3, nonCouncil] = await ethers.getSigners();
    
    const EuystacioSTAnchor = await ethers.getContractFactory("EuystacioSTAnchor");
    anchor = await EuystacioSTAnchor.deploy(
      rootCommit,
      [council1.address, council2.address, council3.address],
      2 // quorum of 2
    );
    await anchor.waitForDeployment();
  });

  describe("Constructor validation", function () {
    it("should reject zero quorum", async function () {
      const EuystacioSTAnchor = await ethers.getContractFactory("EuystacioSTAnchor");
      await expect(
        EuystacioSTAnchor.deploy(
          rootCommit,
          [council1.address, council2.address],
          0 // invalid quorum
        )
      ).to.be.revertedWith("quorum must be positive");
    });

    it("should reject council smaller than quorum", async function () {
      const EuystacioSTAnchor = await ethers.getContractFactory("EuystacioSTAnchor");
      await expect(
        EuystacioSTAnchor.deploy(
          rootCommit,
          [council1.address], // only 1 council member
          2 // quorum of 2
        )
      ).to.be.revertedWith("council size must meet quorum");
    });

    it("should reject zero address in council", async function () {
      const EuystacioSTAnchor = await ethers.getContractFactory("EuystacioSTAnchor");
      await expect(
        EuystacioSTAnchor.deploy(
          rootCommit,
          [council1.address, ethers.ZeroAddress, council3.address],
          2
        )
      ).to.be.revertedWith("invalid council address");
    });
  });

  describe("Anchor confirmation with quorum", function () {
    let anchorId;
    const metricsHash = ethers.keccak256(ethers.toUtf8Bytes("metrics"));
    const metadataURI = "ipfs://QmTest";
    const witnessSig = "0x1234";

    beforeEach(async function () {
      const tx = await anchor.submitAnchor(metricsHash, metadataURI, witnessSig);
      const receipt = await tx.wait();
      anchorId = 1; // First anchor ID
    });

    it("should emit QuorumReached event when quorum is met", async function () {
      await anchor.connect(council1).confirmAnchor(anchorId);
      
      await expect(anchor.connect(council2).confirmAnchor(anchorId))
        .to.emit(anchor, "QuorumReached")
        .withArgs(anchorId, 2);
    });

    it("should prevent confirming already verified anchor", async function () {
      await anchor.connect(council1).confirmAnchor(anchorId);
      await anchor.connect(council2).confirmAnchor(anchorId);
      
      // Anchor is now verified, third council member cannot confirm
      await expect(
        anchor.connect(council3).confirmAnchor(anchorId)
      ).to.be.revertedWith("already verified");
    });

    it("should verify anchor when quorum is reached", async function () {
      await anchor.connect(council1).confirmAnchor(anchorId);
      await anchor.connect(council2).confirmAnchor(anchorId);
      
      const anchorData = await anchor.getAnchor(anchorId);
      expect(anchorData.verified).to.be.true;
    });
  });
});
