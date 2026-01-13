const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("EuystacioSTAnchor", function () {
  let anchor;
  let owner;
  let vetoAuthority;
  let user;

  beforeEach(async function () {
    [owner, vetoAuthority, user] = await ethers.getSigners();

    const EuystacioSTAnchor = await ethers.getContractFactory("EuystacioSTAnchor");
    anchor = await EuystacioSTAnchor.deploy(vetoAuthority.address);
    await anchor.waitForDeployment();
  });

  describe("Deployment", function () {
    it("Should set the correct Red Code Veto Authority", async function () {
      expect(await anchor.redCodeVetoAuthority()).to.equal(vetoAuthority.address);
    });

    it("Should not be sealed initially", async function () {
      expect(await anchor.deploymentSealed()).to.be.false;
    });

    it("Should not have governance locked initially", async function () {
      expect(await anchor.governanceStateLocked()).to.be.false;
    });

    it("Should revert if veto authority is zero address", async function () {
      const EuystacioSTAnchor = await ethers.getContractFactory("EuystacioSTAnchor");
      await expect(
        EuystacioSTAnchor.deploy(ethers.ZeroAddress)
      ).to.be.revertedWith("Invalid veto authority");
    });
  });

  describe("Red Code Veto Functions", function () {
    it("Should allow veto authority to invoke Red Code Veto", async function () {
      const reason = "Ethical violation detected";
      await expect(anchor.connect(vetoAuthority).invokeRedCodeVeto(reason))
        .to.emit(anchor, "RedCodeVetoInvoked")
        .withArgs(vetoAuthority.address, reason, await (await ethers.provider.getBlock('latest')).timestamp + 1);
    });

    it("Should not allow non-veto authority to invoke Red Code Veto", async function () {
      const reason = "Ethical violation detected";
      await expect(
        anchor.connect(user).invokeRedCodeVeto(reason)
      ).to.be.revertedWith("Only Red Code Veto Authority or authorized governance");
    });
    
    it("Should allow authorized governance contract to invoke veto", async function () {
      // Authorize user as governance contract for testing
      await anchor.setAuthorizedGovernanceContract(user.address, true);
      
      const reason = "Governance veto invoked";
      await expect(anchor.connect(user).invokeRedCodeVeto(reason))
        .to.emit(anchor, "RedCodeVetoInvoked")
        .withArgs(user.address, reason, await (await ethers.provider.getBlock('latest')).timestamp + 1);
    });
    
    it("Should allow owner to authorize/deauthorize governance contracts", async function () {
      await expect(anchor.setAuthorizedGovernanceContract(user.address, true))
        .to.emit(anchor, "GovernanceContractAuthorized")
        .withArgs(user.address, true);
      
      expect(await anchor.authorizedGovernanceContracts(user.address)).to.be.true;
      
      await expect(anchor.setAuthorizedGovernanceContract(user.address, false))
        .to.emit(anchor, "GovernanceContractAuthorized")
        .withArgs(user.address, false);
      
      expect(await anchor.authorizedGovernanceContracts(user.address)).to.be.false;
    });

    it("Should allow veto authority to set Red Code IPFS CID", async function () {
      const ipfsCID = "QmRedCodeEthicsFramework123";
      await expect(anchor.connect(vetoAuthority).setRedCodeIPFS(ipfsCID))
        .to.emit(anchor, "RedCodeIPFSUpdated");
      
      expect(await anchor.redCodeIPFSCID()).to.equal(ipfsCID);
    });

    it("Should not allow setting Red Code IPFS after deployment sealed", async function () {
      const ipfsCID = "QmRedCodeEthicsFramework123";
      await anchor.sealDeployment();
      
      await expect(
        anchor.connect(vetoAuthority).setRedCodeIPFS(ipfsCID)
      ).to.be.revertedWith("Deployment is sealed");
    });
  });

  describe("Deployment Sealing", function () {
    it("Should allow owner to seal deployment", async function () {
      await expect(anchor.sealDeployment())
        .to.emit(anchor, "DeploymentSealed");
      
      expect(await anchor.deploymentSealed()).to.be.true;
    });

    it("Should not allow non-owner to seal deployment", async function () {
      await expect(
        anchor.connect(user).sealDeployment()
      ).to.be.reverted;
    });

    it("Should not allow sealing deployment twice", async function () {
      await anchor.sealDeployment();
      await expect(anchor.sealDeployment()).to.be.revertedWith("Deployment is sealed");
    });

    it("Should allow owner to lock governance state", async function () {
      await expect(anchor.lockGovernanceState())
        .to.emit(anchor, "GovernanceStateLocked");
      
      expect(await anchor.governanceStateLocked()).to.be.true;
    });

    it("Should not allow locking governance state twice", async function () {
      await anchor.lockGovernanceState();
      await expect(anchor.lockGovernanceState()).to.be.revertedWith("Governance state is locked");
    });
  });

  describe("Deployment Key Management", function () {
    const keyId = ethers.id("deployment.key.1");
    const keyName = "MainDeploymentKey";
    const keyHash = ethers.id("secretKeyValue");
    const ipfsCID = "QmDeploymentKeyDoc123";

    it("Should register a deployment key", async function () {
      await expect(anchor.registerDeploymentKey(keyId, keyName, keyHash, ipfsCID))
        .to.emit(anchor, "DeploymentKeyRegistered")
        .withArgs(keyId, keyName, ipfsCID);
      
      const key = await anchor.getDeploymentKey(keyId);
      expect(key.name).to.equal(keyName);
      expect(key.keyHash).to.equal(keyHash);
      expect(key.locked).to.be.false;
      expect(key.ipfsCID).to.equal(ipfsCID);
    });

    it("Should lock a deployment key", async function () {
      await anchor.registerDeploymentKey(keyId, keyName, keyHash, ipfsCID);
      
      await expect(anchor.lockDeploymentKey(keyId))
        .to.emit(anchor, "DeploymentKeyLocked");
      
      expect(await anchor.isDeploymentKeyLocked(keyId)).to.be.true;
    });

    it("Should not register deployment key when sealed", async function () {
      await anchor.sealDeployment();
      
      await expect(
        anchor.registerDeploymentKey(keyId, keyName, keyHash, ipfsCID)
      ).to.be.revertedWith("Deployment is sealed");
    });

    it("Should not allow locking same key twice", async function () {
      await anchor.registerDeploymentKey(keyId, keyName, keyHash, ipfsCID);
      await anchor.lockDeploymentKey(keyId);
      
      await expect(anchor.lockDeploymentKey(keyId)).to.be.revertedWith("Key already locked");
    });

    it("Should not register key with invalid parameters", async function () {
      await expect(
        anchor.registerDeploymentKey(keyId, "", keyHash, ipfsCID)
      ).to.be.revertedWith("Invalid name");

      await expect(
        anchor.registerDeploymentKey(keyId, keyName, ethers.ZeroHash, ipfsCID)
      ).to.be.revertedWith("Invalid key hash");
    });
  });

  describe("Runtime Parameter Management", function () {
    const paramId = ethers.id("runtime.param.1");
    const paramName = "MaxSupply";
    const valueHash = ethers.id("1000000");
    const description = "Maximum token supply parameter";

    it("Should set a runtime parameter", async function () {
      await expect(anchor.setRuntimeParameter(paramId, paramName, valueHash, description))
        .to.emit(anchor, "RuntimeParameterSet")
        .withArgs(paramId, paramName, valueHash);
      
      const param = await anchor.getRuntimeParameter(paramId);
      expect(param.name).to.equal(paramName);
      expect(param.valueHash).to.equal(valueHash);
      expect(param.locked).to.be.false;
      expect(param.description).to.equal(description);
    });

    it("Should lock a runtime parameter", async function () {
      await anchor.setRuntimeParameter(paramId, paramName, valueHash, description);
      
      await expect(anchor.lockRuntimeParameter(paramId))
        .to.emit(anchor, "RuntimeParameterLocked");
      
      expect(await anchor.isRuntimeParameterLocked(paramId)).to.be.true;
    });

    it("Should not set parameter when governance locked", async function () {
      await anchor.lockGovernanceState();
      
      await expect(
        anchor.setRuntimeParameter(paramId, paramName, valueHash, description)
      ).to.be.revertedWith("Governance state is locked");
    });

    it("Should not update locked parameter", async function () {
      await anchor.setRuntimeParameter(paramId, paramName, valueHash, description);
      await anchor.lockRuntimeParameter(paramId);
      
      const newValueHash = ethers.id("2000000");
      await expect(
        anchor.setRuntimeParameter(paramId, paramName, newValueHash, description)
      ).to.be.revertedWith("Parameter is locked");
    });

    it("Should not set parameter with invalid values", async function () {
      await expect(
        anchor.setRuntimeParameter(paramId, "", valueHash, description)
      ).to.be.revertedWith("Invalid name");

      await expect(
        anchor.setRuntimeParameter(paramId, paramName, ethers.ZeroHash, description)
      ).to.be.revertedWith("Invalid value hash");
    });
  });

  describe("G-CSI IPFS Anchoring", function () {
    const docId = ethers.id("governance.doc.1");
    const docName = "Core Governance Charter";
    const ipfsCID = "QmGovernanceDoc123";
    const contentHash = ethers.id("documentContentForValidation");

    it("Should anchor a governance document", async function () {
      await expect(anchor.anchorGovernanceDocument(docId, docName, ipfsCID, contentHash))
        .to.emit(anchor, "GovernanceDocumentAnchored")
        .withArgs(docId, ipfsCID, contentHash);
      
      const doc = await anchor.getGovernanceDocument(docId);
      expect(doc.name).to.equal(docName);
      expect(doc.ipfsCID).to.equal(ipfsCID);
      expect(doc.contentHash).to.equal(contentHash);
      expect(doc.validated).to.be.false;
    });

    it("Should validate a governance document", async function () {
      await anchor.anchorGovernanceDocument(docId, docName, ipfsCID, contentHash);
      await anchor.validateGovernanceDocument(docId);
      
      const doc = await anchor.getGovernanceDocument(docId);
      expect(doc.validated).to.be.true;
    });

    it("Should not anchor document when sealed", async function () {
      await anchor.sealDeployment();
      
      await expect(
        anchor.anchorGovernanceDocument(docId, docName, ipfsCID, contentHash)
      ).to.be.revertedWith("Deployment is sealed");
    });

    it("Should not validate non-existent document", async function () {
      await expect(
        anchor.validateGovernanceDocument(docId)
      ).to.be.revertedWith("Document does not exist");
    });

    it("Should not validate document twice", async function () {
      await anchor.anchorGovernanceDocument(docId, docName, ipfsCID, contentHash);
      await anchor.validateGovernanceDocument(docId);
      
      await expect(
        anchor.validateGovernanceDocument(docId)
      ).to.be.revertedWith("Document already validated");
    });

    it("Should update G-CSI anchoring graph", async function () {
      const graphCID = "QmGCSIAnchoringGraph123";
      
      await expect(anchor.updateGCSIAnchoringGraph(graphCID))
        .to.emit(anchor, "GCSIAnchoringGraphUpdated")
        .withArgs(graphCID, await (await ethers.provider.getBlock('latest')).timestamp + 1);
      
      expect(await anchor.gcsiAnchoringGraphCID()).to.equal(graphCID);
    });

    it("Should not update G-CSI graph when sealed", async function () {
      const graphCID = "QmGCSIAnchoringGraph123";
      await anchor.sealDeployment();
      
      await expect(
        anchor.updateGCSIAnchoringGraph(graphCID)
      ).to.be.revertedWith("Deployment is sealed");
    });

    it("Should not anchor document with invalid parameters", async function () {
      await expect(
        anchor.anchorGovernanceDocument(docId, "", ipfsCID, contentHash)
      ).to.be.revertedWith("Invalid name");

      await expect(
        anchor.anchorGovernanceDocument(docId, docName, "", contentHash)
      ).to.be.revertedWith("Invalid IPFS CID");

      await expect(
        anchor.anchorGovernanceDocument(docId, docName, ipfsCID, ethers.ZeroHash)
      ).to.be.revertedWith("Invalid content hash");
    });
  });

  describe("Integration Scenarios", function () {
    it("Should complete full deployment sealing workflow", async function () {
      // 1. Set Red Code IPFS
      const redCodeCID = "QmRedCode123";
      await anchor.connect(vetoAuthority).setRedCodeIPFS(redCodeCID);
      
      // 2. Register deployment keys
      const keyId = ethers.id("deploy.key.1");
      await anchor.registerDeploymentKey(
        keyId,
        "MainKey",
        ethers.id("secret"),
        "QmKey123"
      );
      
      // 3. Set runtime parameters
      const paramId = ethers.id("param.1");
      await anchor.setRuntimeParameter(
        paramId,
        "MaxSupply",
        ethers.id("1000000"),
        "Max supply"
      );
      
      // 4. Anchor governance documents
      const docId = ethers.id("doc.1");
      await anchor.anchorGovernanceDocument(
        docId,
        "Charter",
        "QmDoc123",
        ethers.id("content")
      );
      await anchor.validateGovernanceDocument(docId);
      
      // 5. Update G-CSI graph
      await anchor.updateGCSIAnchoringGraph("QmGCSI123");
      
      // 6. Lock everything
      await anchor.lockDeploymentKey(keyId);
      await anchor.lockRuntimeParameter(paramId);
      await anchor.lockGovernanceState();
      await anchor.sealDeployment();
      
      // 7. Verify everything is locked
      expect(await anchor.isDeploymentKeyLocked(keyId)).to.be.true;
      expect(await anchor.isRuntimeParameterLocked(paramId)).to.be.true;
      expect(await anchor.governanceStateLocked()).to.be.true;
      expect(await anchor.deploymentSealed()).to.be.true;
    });

    it("Should allow veto authority to invoke veto even when sealed", async function () {
      await anchor.sealDeployment();
      
      // Veto can still be invoked even when sealed (ultimate override)
      await expect(
        anchor.connect(vetoAuthority).invokeRedCodeVeto("Emergency ethical override")
      ).to.emit(anchor, "RedCodeVetoInvoked");
    });
  });
});
