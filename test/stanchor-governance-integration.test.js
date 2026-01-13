const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("EUSDaoGovernance and EuystacioSTAnchor Integration", function () {
  let governance;
  let anchor;
  let owner;
  let vetoAuthority;
  let user;

  beforeEach(async function () {
    [owner, vetoAuthority, user] = await ethers.getSigners();

    // Deploy EuystacioSTAnchor
    const EuystacioSTAnchor = await ethers.getContractFactory("EuystacioSTAnchor");
    anchor = await EuystacioSTAnchor.deploy(vetoAuthority.address);
    await anchor.waitForDeployment();

    // Deploy EUSDaoGovernance
    const Governance = await ethers.getContractFactory("EUSDaoGovernance");
    governance = await Governance.deploy();
    await governance.waitForDeployment();
  });

  describe("Integration Setup", function () {
    it("Should set STAnchor in governance contract", async function () {
      const anchorAddress = await anchor.getAddress();
      await expect(governance.setSTAnchor(anchorAddress))
        .to.emit(governance, "STAnchorSet")
        .withArgs(anchorAddress);
      
      expect(await governance.stAnchor()).to.equal(anchorAddress);
    });

    it("Should not set zero address as STAnchor", async function () {
      await expect(
        governance.setSTAnchor(ethers.ZeroAddress)
      ).to.be.revertedWith("Invalid STAnchor address");
    });

    it("Should enable Red Code Veto integration", async function () {
      const anchorAddress = await anchor.getAddress();
      await governance.setSTAnchor(anchorAddress);
      
      await expect(governance.setRedCodeVetoEnabled(true))
        .to.emit(governance, "RedCodeVetoEnabled")
        .withArgs(true);
      
      expect(await governance.redCodeVetoEnabled()).to.be.true;
    });

    it("Should not enable Red Code Veto without STAnchor set", async function () {
      await expect(
        governance.setRedCodeVetoEnabled(true)
      ).to.be.revertedWith("STAnchor not set");
    });
  });

  describe("Red Code Veto Integration", function () {
    beforeEach(async function () {
      const anchorAddress = await anchor.getAddress();
      await governance.setSTAnchor(anchorAddress);
      await governance.setRedCodeVetoEnabled(true);
      
      // Authorize governance contract to invoke veto
      const governanceAddress = await governance.getAddress();
      await anchor.setAuthorizedGovernanceContract(governanceAddress, true);
    });

    it("Should allow veto authority to invoke veto through governance", async function () {
      const reason = "Ethical violation in governance decision";
      
      await expect(
        governance.connect(vetoAuthority).invokeRedCodeVetoFromGovernance(reason)
      ).to.emit(governance, "RedCodeVetoInvokedInGovernance")
        .withArgs(vetoAuthority.address, reason);
    });

    it("Should not allow non-veto authority to invoke veto through governance", async function () {
      const reason = "Attempted unauthorized veto";
      
      await expect(
        governance.connect(user).invokeRedCodeVetoFromGovernance(reason)
      ).to.be.revertedWith("Not veto authority");
    });

    it("Should not invoke veto when integration disabled", async function () {
      await governance.setRedCodeVetoEnabled(false);
      const reason = "Attempted veto when disabled";
      
      await expect(
        governance.connect(vetoAuthority).invokeRedCodeVetoFromGovernance(reason)
      ).to.be.revertedWith("Red Code Veto not enabled");
    });
  });

  describe("Governance Sealing Status", function () {
    beforeEach(async function () {
      const anchorAddress = await anchor.getAddress();
      await governance.setSTAnchor(anchorAddress);
    });

    it("Should return false when not sealed", async function () {
      expect(await governance.isGovernanceSealed()).to.be.false;
    });

    it("Should return true when deployment sealed and governance locked", async function () {
      await anchor.sealDeployment();
      await anchor.lockGovernanceState();
      
      expect(await governance.isGovernanceSealed()).to.be.true;
    });

    it("Should return false when only deployment sealed", async function () {
      await anchor.sealDeployment();
      
      expect(await governance.isGovernanceSealed()).to.be.false;
    });

    it("Should return false when only governance locked", async function () {
      await anchor.lockGovernanceState();
      
      expect(await governance.isGovernanceSealed()).to.be.false;
    });

    it("Should return false when STAnchor not set", async function () {
      const Governance = await ethers.getContractFactory("EUSDaoGovernance");
      const newGovernance = await Governance.deploy();
      await newGovernance.waitForDeployment();
      
      expect(await newGovernance.isGovernanceSealed()).to.be.false;
    });
  });

  describe("Full Deployment Sealing Workflow", function () {
    it("Should complete full integration and sealing workflow", async function () {
      // 1. Set up integration
      const anchorAddress = await anchor.getAddress();
      await governance.setSTAnchor(anchorAddress);
      await governance.setRedCodeVetoEnabled(true);
      
      // Authorize governance contract
      const governanceAddress = await governance.getAddress();
      await anchor.setAuthorizedGovernanceContract(governanceAddress, true);
      
      // 2. Configure STAnchor with Red Code IPFS
      const redCodeCID = "QmRedCodeEthics123";
      await anchor.connect(vetoAuthority).setRedCodeIPFS(redCodeCID);
      
      // 3. Register deployment keys
      const keyId = ethers.id("governance.deploy.key");
      await anchor.registerDeploymentKey(
        keyId,
        "GovernanceDeployKey",
        ethers.id("keySecret123"),
        "QmDeployKey123"
      );
      
      // 4. Set runtime parameters
      const paramId = ethers.id("governance.max.supply");
      await anchor.setRuntimeParameter(
        paramId,
        "MaxGovernanceSupply",
        ethers.id("1000000000"),
        "Maximum governance token supply"
      );
      
      // 5. Anchor governance documents with G-CSI
      const docId = ethers.id("governance.charter");
      const docIPFS = "QmGovernanceCharter123";
      const contentHash = ethers.keccak256(ethers.toUtf8Bytes("Governance Charter Content"));
      await anchor.anchorGovernanceDocument(
        docId,
        "Governance Charter",
        docIPFS,
        contentHash
      );
      await anchor.validateGovernanceDocument(docId);
      
      // 6. Update G-CSI anchoring graph
      const gcsiCID = "QmGCSIGraph123";
      await anchor.updateGCSIAnchoringGraph(gcsiCID);
      
      // 7. Lock critical components
      await anchor.lockDeploymentKey(keyId);
      await anchor.lockRuntimeParameter(paramId);
      
      // 8. Seal deployment
      await anchor.lockGovernanceState();
      await anchor.sealDeployment();
      
      // 9. Verify sealed state
      expect(await anchor.deploymentSealed()).to.be.true;
      expect(await anchor.governanceStateLocked()).to.be.true;
      expect(await governance.isGovernanceSealed()).to.be.true;
      
      // 10. Verify Red Code Veto still works (ultimate override)
      const reason = "Post-seal ethical verification";
      await expect(
        governance.connect(vetoAuthority).invokeRedCodeVetoFromGovernance(reason)
      ).to.emit(governance, "RedCodeVetoInvokedInGovernance");
      
      // 11. Verify all anchored data is accessible
      expect(await anchor.redCodeIPFSCID()).to.equal(redCodeCID);
      expect(await anchor.gcsiAnchoringGraphCID()).to.equal(gcsiCID);
      
      const doc = await anchor.getGovernanceDocument(docId);
      expect(doc.ipfsCID).to.equal(docIPFS);
      expect(doc.validated).to.be.true;
      
      const key = await anchor.getDeploymentKey(keyId);
      expect(key.locked).to.be.true;
      
      const param = await anchor.getRuntimeParameter(paramId);
      expect(param.locked).to.be.true;
    });
  });
});
