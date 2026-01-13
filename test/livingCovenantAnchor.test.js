const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("LivingCovenantAnchor", function () {
  let lca;
  let owner;
  let user1;
  let user2;

  const COVENANT_URI = "ipfs://QmTest123";
  const COVENANT_ROOT_HASH = ethers.keccak256(ethers.toUtf8Bytes("covenant root"));

  beforeEach(async function () {
    [owner, user1, user2] = await ethers.getSigners();

    const LCA = await ethers.getContractFactory("LivingCovenantAnchor");
    lca = await LCA.deploy(COVENANT_URI, COVENANT_ROOT_HASH);
    await lca.waitForDeployment();
  });

  describe("Initialization", function () {
    it("Should initialize with covenant URI and root hash", async function () {
      const [uri, rootHash, lastUpdate] = await lca.getCovenantInfo();
      
      expect(uri).to.equal(COVENANT_URI);
      expect(rootHash).to.equal(COVENANT_ROOT_HASH);
      expect(lastUpdate).to.be.greaterThan(0);
    });
  });

  describe("Milestone Creation", function () {
    it("Should allow creating a milestone", async function () {
      const description = "First governance milestone";
      const actionHash = ethers.keccak256(ethers.toUtf8Bytes("action1"));
      const covenantRef = ethers.keccak256(ethers.toUtf8Bytes("covenant section 1"));

      await expect(lca.connect(user1).createMilestone(description, actionHash, covenantRef))
        .to.emit(lca, "MilestoneCreated");

      expect(await lca.getMilestoneCount()).to.equal(1);
    });

    it("Should prevent creating milestone with empty description", async function () {
      const actionHash = ethers.keccak256(ethers.toUtf8Bytes("action"));
      const covenantRef = ethers.keccak256(ethers.toUtf8Bytes("ref"));

      await expect(
        lca.createMilestone("", actionHash, covenantRef)
      ).to.be.revertedWith("LCA: Description required");
    });

    it("Should prevent creating milestone with invalid action hash", async function () {
      await expect(
        lca.createMilestone("Description", ethers.ZeroHash, ethers.ZeroHash)
      ).to.be.revertedWith("LCA: Invalid action hash");
    });

    it("Should store milestone details correctly", async function () {
      const description = "Test milestone";
      const actionHash = ethers.keccak256(ethers.toUtf8Bytes("action"));
      const covenantRef = ethers.keccak256(ethers.toUtf8Bytes("ref"));

      const tx = await lca.connect(user1).createMilestone(description, actionHash, covenantRef);
      await tx.wait();

      const milestoneId = await lca.getMilestoneIdByIndex(0);
      const milestone = await lca.milestones(milestoneId);

      expect(milestone.description).to.equal(description);
      expect(milestone.actionHash).to.equal(actionHash);
      expect(milestone.covenantReference).to.equal(covenantRef);
      expect(milestone.initiator).to.equal(user1.address);
      expect(milestone.isSealed).to.be.false;
    });
  });

  describe("Anchor Creation", function () {
    let milestoneId;

    beforeEach(async function () {
      const description = "Test milestone";
      const actionHash = ethers.keccak256(ethers.toUtf8Bytes("action"));
      const covenantRef = ethers.keccak256(ethers.toUtf8Bytes("ref"));

      await lca.createMilestone(description, actionHash, covenantRef);
      milestoneId = await lca.getMilestoneIdByIndex(0);
    });

    it("Should allow creating an anchor for a milestone", async function () {
      const anchorType = "governance";
      const contentHash = ethers.keccak256(ethers.toUtf8Bytes("content"));

      await expect(lca.createAnchor(milestoneId, anchorType, contentHash))
        .to.emit(lca, "AnchorCreated");

      expect(await lca.getAnchorCount()).to.equal(1);
    });

    it("Should prevent creating anchor for non-existent milestone", async function () {
      const fakeMilestoneId = ethers.keccak256(ethers.toUtf8Bytes("fake"));
      const anchorType = "governance";
      const contentHash = ethers.keccak256(ethers.toUtf8Bytes("content"));

      await expect(
        lca.createAnchor(fakeMilestoneId, anchorType, contentHash)
      ).to.be.revertedWith("LCA: Milestone does not exist");
    });

    it("Should prevent creating anchor with invalid content hash", async function () {
      await expect(
        lca.createAnchor(milestoneId, "governance", ethers.ZeroHash)
      ).to.be.revertedWith("LCA: Invalid content hash");
    });

    it("Should prevent creating anchor with empty type", async function () {
      const contentHash = ethers.keccak256(ethers.toUtf8Bytes("content"));

      await expect(
        lca.createAnchor(milestoneId, "", contentHash)
      ).to.be.revertedWith("LCA: Anchor type required");
    });

    it("Should store anchor details correctly", async function () {
      const anchorType = "covenant";
      const contentHash = ethers.keccak256(ethers.toUtf8Bytes("content"));

      const tx = await lca.createAnchor(milestoneId, anchorType, contentHash);
      await tx.wait();

      const anchorHash = await lca.getAnchorHashByIndex(0);
      const anchor = await lca.anchors(anchorHash);

      expect(anchor.milestoneId).to.equal(milestoneId);
      expect(anchor.anchorType).to.equal(anchorType);
      expect(anchor.contentHash).to.equal(contentHash);
      expect(anchor.permanent).to.be.true;
    });
  });

  describe("Anchor Linking", function () {
    let milestoneId;
    let anchorHash;

    beforeEach(async function () {
      const description = "Test milestone";
      const actionHash = ethers.keccak256(ethers.toUtf8Bytes("action"));
      const covenantRef = ethers.keccak256(ethers.toUtf8Bytes("ref"));

      await lca.createMilestone(description, actionHash, covenantRef);
      milestoneId = await lca.getMilestoneIdByIndex(0);

      const contentHash = ethers.keccak256(ethers.toUtf8Bytes("content"));
      await lca.createAnchor(milestoneId, "governance", contentHash);
      anchorHash = await lca.getAnchorHashByIndex(0);
    });

    it("Should allow linking anchor to milestone", async function () {
      const contentHash2 = ethers.keccak256(ethers.toUtf8Bytes("content2"));
      await lca.createAnchor(milestoneId, "covenant", contentHash2);
      const anchorHash2 = await lca.getAnchorHashByIndex(1);

      await expect(lca.linkAnchor(milestoneId, anchorHash2))
        .to.emit(lca, "AnchorLinked")
        .withArgs(milestoneId, anchorHash2);

      const linkedAnchors = await lca.getLinkedAnchors(milestoneId);
      expect(linkedAnchors).to.include(anchorHash2);
    });

    it("Should prevent linking to non-existent milestone", async function () {
      const fakeMilestoneId = ethers.keccak256(ethers.toUtf8Bytes("fake"));

      await expect(
        lca.linkAnchor(fakeMilestoneId, anchorHash)
      ).to.be.revertedWith("LCA: Milestone does not exist");
    });

    it("Should prevent linking non-existent anchor", async function () {
      const fakeAnchorHash = ethers.keccak256(ethers.toUtf8Bytes("fake"));

      await expect(
        lca.linkAnchor(milestoneId, fakeAnchorHash)
      ).to.be.revertedWith("LCA: Anchor does not exist");
    });

    it("Should prevent linking to sealed milestone", async function () {
      await lca.sealMilestone(milestoneId, anchorHash);

      const contentHash2 = ethers.keccak256(ethers.toUtf8Bytes("content2"));
      await lca.createAnchor(milestoneId, "covenant", contentHash2);
      const anchorHash2 = await lca.getAnchorHashByIndex(1);

      await expect(
        lca.linkAnchor(milestoneId, anchorHash2)
      ).to.be.revertedWith("LCA: Milestone already sealed");
    });
  });

  describe("Milestone Sealing", function () {
    let milestoneId;
    let anchorHash;

    beforeEach(async function () {
      const description = "Test milestone";
      const actionHash = ethers.keccak256(ethers.toUtf8Bytes("action"));
      const covenantRef = ethers.keccak256(ethers.toUtf8Bytes("ref"));

      await lca.createMilestone(description, actionHash, covenantRef);
      milestoneId = await lca.getMilestoneIdByIndex(0);

      const contentHash = ethers.keccak256(ethers.toUtf8Bytes("content"));
      await lca.createAnchor(milestoneId, "governance", contentHash);
      anchorHash = await lca.getAnchorHashByIndex(0);
    });

    it("Should allow owner to seal milestone", async function () {
      await expect(lca.sealMilestone(milestoneId, anchorHash))
        .to.emit(lca, "MilestoneSealed")
        .withArgs(milestoneId, anchorHash);

      expect(await lca.isMilestoneSealed(milestoneId)).to.be.true;
    });

    it("Should prevent non-authorized from sealing milestone", async function () {
      await expect(
        lca.connect(user1).sealMilestone(milestoneId, anchorHash)
      ).to.be.revertedWith("LCA: Not authorized");
    });

    it("Should prevent sealing non-existent milestone", async function () {
      const fakeMilestoneId = ethers.keccak256(ethers.toUtf8Bytes("fake"));

      await expect(
        lca.sealMilestone(fakeMilestoneId, anchorHash)
      ).to.be.revertedWith("LCA: Milestone does not exist");
    });

    it("Should prevent sealing already sealed milestone", async function () {
      await lca.sealMilestone(milestoneId, anchorHash);

      await expect(
        lca.sealMilestone(milestoneId, anchorHash)
      ).to.be.revertedWith("LCA: Already sealed");
    });
  });

  describe("Covenant Updates", function () {
    it("Should allow owner to update covenant", async function () {
      const newURI = "ipfs://QmNewCovenant";
      const newRootHash = ethers.keccak256(ethers.toUtf8Bytes("new covenant root"));

      await expect(lca.updateCovenant(newURI, newRootHash))
        .to.emit(lca, "CovenantUpdated")
        .withArgs(COVENANT_ROOT_HASH, newRootHash, newURI);

      const [uri, rootHash] = await lca.getCovenantInfo();
      expect(uri).to.equal(newURI);
      expect(rootHash).to.equal(newRootHash);
    });

    it("Should prevent updating with empty URI", async function () {
      const newRootHash = ethers.keccak256(ethers.toUtf8Bytes("new root"));

      await expect(
        lca.updateCovenant("", newRootHash)
      ).to.be.revertedWith("LCA: URI required");
    });

    it("Should prevent updating with invalid root hash", async function () {
      await expect(
        lca.updateCovenant("ipfs://test", ethers.ZeroHash)
      ).to.be.revertedWith("LCA: Invalid root hash");
    });

    it("Should prevent non-owner from updating covenant", async function () {
      const newURI = "ipfs://test";
      const newRootHash = ethers.keccak256(ethers.toUtf8Bytes("root"));

      await expect(
        lca.connect(user1).updateCovenant(newURI, newRootHash)
      ).to.be.revertedWith("Ownable: caller is not the owner");
    });
  });

  describe("Verification", function () {
    let anchorHash;

    beforeEach(async function () {
      const description = "Test milestone";
      const actionHash = ethers.keccak256(ethers.toUtf8Bytes("action"));
      const covenantRef = ethers.keccak256(ethers.toUtf8Bytes("ref"));

      await lca.createMilestone(description, actionHash, covenantRef);
      const milestoneId = await lca.getMilestoneIdByIndex(0);

      const contentHash = ethers.keccak256(ethers.toUtf8Bytes("content"));
      await lca.createAnchor(milestoneId, "governance", contentHash);
      anchorHash = await lca.getAnchorHashByIndex(0);
    });

    it("Should verify valid anchor", async function () {
      expect(await lca.verifyAnchor(anchorHash)).to.be.true;
    });

    it("Should not verify non-existent anchor", async function () {
      const fakeAnchorHash = ethers.keccak256(ethers.toUtf8Bytes("fake"));
      expect(await lca.verifyAnchor(fakeAnchorHash)).to.be.false;
    });
  });

  describe("Query Functions", function () {
    it("Should track milestone and anchor counts", async function () {
      expect(await lca.getMilestoneCount()).to.equal(0);
      expect(await lca.getAnchorCount()).to.equal(0);

      const actionHash1 = ethers.keccak256(ethers.toUtf8Bytes("action1"));
      await lca.createMilestone("Milestone 1", actionHash1, ethers.ZeroHash);
      expect(await lca.getMilestoneCount()).to.equal(1);

      const milestoneId1 = await lca.getMilestoneIdByIndex(0);
      const contentHash1 = ethers.keccak256(ethers.toUtf8Bytes("content1"));
      await lca.createAnchor(milestoneId1, "governance", contentHash1);
      expect(await lca.getAnchorCount()).to.equal(1);

      const actionHash2 = ethers.keccak256(ethers.toUtf8Bytes("action2"));
      await lca.createMilestone("Milestone 2", actionHash2, ethers.ZeroHash);
      expect(await lca.getMilestoneCount()).to.equal(2);
    });

    it("Should prevent accessing out of bounds milestone index", async function () {
      await expect(
        lca.getMilestoneIdByIndex(0)
      ).to.be.revertedWith("LCA: Index out of bounds");
    });

    it("Should prevent accessing out of bounds anchor index", async function () {
      await expect(
        lca.getAnchorHashByIndex(0)
      ).to.be.revertedWith("LCA: Index out of bounds");
    });
  });

  describe("Integration Scenarios", function () {
    it("Should support complete milestone workflow", async function () {
      // Create milestone
      const description = "Complete governance action";
      const actionHash = ethers.keccak256(ethers.toUtf8Bytes("action"));
      const covenantRef = ethers.keccak256(ethers.toUtf8Bytes("covenant ref"));

      await lca.createMilestone(description, actionHash, covenantRef);
      const milestoneId = await lca.getMilestoneIdByIndex(0);

      // Create multiple anchors
      const contentHash1 = ethers.keccak256(ethers.toUtf8Bytes("content1"));
      await lca.createAnchor(milestoneId, "governance", contentHash1);
      
      const contentHash2 = ethers.keccak256(ethers.toUtf8Bytes("content2"));
      await lca.createAnchor(milestoneId, "covenant", contentHash2);

      // Link anchors
      const anchorHash2 = await lca.getAnchorHashByIndex(1);
      await lca.linkAnchor(milestoneId, anchorHash2);

      // Seal milestone
      const finalAnchorHash = await lca.getAnchorHashByIndex(0);
      await lca.sealMilestone(milestoneId, finalAnchorHash);

      // Verify final state
      expect(await lca.isMilestoneSealed(milestoneId)).to.be.true;
      const linkedAnchors = await lca.getLinkedAnchors(milestoneId);
      expect(linkedAnchors.length).to.equal(1);
      expect(await lca.verifyAnchor(anchorHash2)).to.be.true;
    });
  });
});
