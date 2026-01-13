const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Enhanced Security Integration", function () {
  let redCodeVeto;
  let gCSI;
  let livingCovenantAnchor;
  let tfp;
  let sustainment;
  let karmaBond;
  let mockToken;
  let owner;
  let council1;
  let council2;
  let foundation;
  let investor;

  const DECIMALS = 6;
  const MIN_USD = 10000;
  const MIN_SUSTAINMENT = MIN_USD * (10 ** DECIMALS);
  const SUSTAINMENT_PERCENT = 200;
  const COVENANT_URI = "ipfs://QmEuystacioLivingCovenant";
  const COVENANT_ROOT = ethers.keccak256(ethers.toUtf8Bytes("living covenant root"));

  beforeEach(async function () {
    [owner, council1, council2, foundation, investor] = await ethers.getSigners();

    // Deploy mock token
    const MockERC20 = await ethers.getContractFactory("MockERC20");
    mockToken = await MockERC20.deploy("Mock USDC", "USDC", DECIMALS);
    await mockToken.waitForDeployment();

    // Deploy Sustainment
    const Sustainment = await ethers.getContractFactory("Sustainment");
    sustainment = await Sustainment.deploy(
      await mockToken.getAddress(),
      DECIMALS,
      MIN_USD
    );
    await sustainment.waitForDeployment();

    // Deploy KarmaBond
    const KarmaBond = await ethers.getContractFactory("KarmaBond");
    karmaBond = await KarmaBond.deploy(
      await mockToken.getAddress(),
      await sustainment.getAddress(),
      foundation.address,
      BigInt(SUSTAINMENT_PERCENT)
    );
    await karmaBond.waitForDeployment();

    // Authorize KarmaBond
    await sustainment.setAuthorizedDepositor(await karmaBond.getAddress(), true);

    // Deploy Red Code Veto
    const RedCodeVeto = await ethers.getContractFactory("RedCodeVeto");
    redCodeVeto = await RedCodeVeto.deploy();
    await redCodeVeto.waitForDeployment();

    // Add council members
    await redCodeVeto.addCouncilMember(council1.address);
    await redCodeVeto.addCouncilMember(council2.address);

    // Deploy G-CSI
    const GCSI = await ethers.getContractFactory("GlobalConsensusSealIntegrity");
    gCSI = await GCSI.deploy();
    await gCSI.waitForDeployment();

    // Add council members to G-CSI
    await gCSI.addCouncilMember(council1.address, "Council Member 1");
    await gCSI.addCouncilMember(council2.address, "Council Member 2");
    await gCSI.setQuorumRequirements(51, 2);

    // Deploy Living Covenant Anchor
    const LCA = await ethers.getContractFactory("LivingCovenantAnchor");
    livingCovenantAnchor = await LCA.deploy(COVENANT_URI, COVENANT_ROOT);
    await livingCovenantAnchor.waitForDeployment();

    // Deploy TrustlessFundingProtocol
    const TFP = await ethers.getContractFactory("TrustlessFundingProtocol");
    tfp = await TFP.deploy(foundation.address);
    await tfp.waitForDeployment();

    // Authorize TFP to seal milestones
    await livingCovenantAnchor.addAuthorizedSealer(await tfp.getAddress());

    // Configure TFP with all security components
    await tfp.setSustainmentContract(await sustainment.getAddress());
    await tfp.setRedCodeVeto(await redCodeVeto.getAddress());
    await tfp.setGCSI(await gCSI.getAddress());
    await tfp.setLivingCovenantAnchor(await livingCovenantAnchor.getAddress());

    // Mint tokens to investor
    await mockToken.mint(investor.address, ethers.parseUnits("1000000", DECIMALS));
  });

  describe("Full Security Stack Integration", function () {
    it("Should successfully release tranche with all security checks passed", async function () {
      // 1. Fund sustainment to meet minimum
      const fundAmount = BigInt(MIN_SUSTAINMENT) * 55n;
      await mockToken.connect(investor).approve(await karmaBond.getAddress(), fundAmount);
      await karmaBond.connect(investor).mintBond(fundAmount);
      expect(await sustainment.isAboveMinimum()).to.be.true;

      // 2. Create and approve G-CSI seal
      const trancheId = 1;
      const proofHash = ethers.keccak256(ethers.toUtf8Bytes("proof for tranche 1"));
      const actionHash = ethers.keccak256(ethers.toUtf8Bytes("release tranche 1"));
      
      const sealTx = await gCSI.connect(owner).createSeal(actionHash, "Tranche 1 release approval");
      await sealTx.wait();
      const sealId = await gCSI.getSealIdByIndex(0);
      
      // Get quorum
      await gCSI.connect(council1).signSeal(sealId);
      await gCSI.connect(owner).executeSeal(sealId);
      
      expect(await gCSI.verifySeal(sealId)).to.be.true;

      // 3. Red Code Veto is in ACTIVE state (default)
      expect(await redCodeVeto.operationsAllowed()).to.be.true;

      // 4. Release tranche
      await expect(tfp.releaseTranche(trancheId, proofHash, sealId))
        .to.emit(tfp, "TrancheReleased")
        .to.emit(tfp, "MilestoneCreatedForTranche");

      expect(await tfp.trancheReleased(trancheId)).to.be.true;

      // 5. Verify milestone was created and sealed
      const milestoneId = await tfp.getTrancheMilestone(trancheId);
      expect(await livingCovenantAnchor.isMilestoneSealed(milestoneId)).to.be.true;
    });

    it("Should block tranche release when Red Code Veto is active", async function () {
      // Fund sustainment
      const fundAmount = BigInt(MIN_SUSTAINMENT) * 55n;
      await mockToken.connect(investor).approve(await karmaBond.getAddress(), fundAmount);
      await karmaBond.connect(investor).mintBond(fundAmount);

      // Create G-CSI seal
      const trancheId = 1;
      const proofHash = ethers.keccak256(ethers.toUtf8Bytes("proof"));
      const actionHash = ethers.keccak256(ethers.toUtf8Bytes("action"));
      
      await gCSI.connect(owner).createSeal(actionHash, "Test");
      const sealId = await gCSI.getSealIdByIndex(0);
      await gCSI.connect(council1).signSeal(sealId);
      await gCSI.connect(owner).executeSeal(sealId);

      // Activate Red Code Veto
      await redCodeVeto.connect(council1).initiateVeto(1, "Security concern");
      expect(await redCodeVeto.operationsAllowed()).to.be.false;

      // Attempt to release tranche
      await expect(
        tfp.releaseTranche(trancheId, proofHash, sealId)
      ).to.be.revertedWith("Red Code Veto: Operations not allowed");
    });

    it("Should block tranche release without G-CSI seal", async function () {
      // Fund sustainment
      const fundAmount = BigInt(MIN_SUSTAINMENT) * 55n;
      await mockToken.connect(investor).approve(await karmaBond.getAddress(), fundAmount);
      await karmaBond.connect(investor).mintBond(fundAmount);

      // Create seal but don't execute it
      const trancheId = 1;
      const proofHash = ethers.keccak256(ethers.toUtf8Bytes("proof"));
      const actionHash = ethers.keccak256(ethers.toUtf8Bytes("action"));
      
      await gCSI.connect(owner).createSeal(actionHash, "Test");
      const sealId = await gCSI.getSealIdByIndex(0);
      // Don't get quorum or execute

      // Attempt to release tranche
      await expect(
        tfp.releaseTranche(trancheId, proofHash, sealId)
      ).to.be.revertedWith("G-CSI: Seal not verified or executed");
    });

    it("Should block tranche release when sustainment is below minimum", async function () {
      // Create and approve G-CSI seal
      const trancheId = 1;
      const proofHash = ethers.keccak256(ethers.toUtf8Bytes("proof"));
      const actionHash = ethers.keccak256(ethers.toUtf8Bytes("action"));
      
      await gCSI.connect(owner).createSeal(actionHash, "Test");
      const sealId = await gCSI.getSealIdByIndex(0);
      await gCSI.connect(council1).signSeal(sealId);
      await gCSI.connect(owner).executeSeal(sealId);

      // Don't fund sustainment
      expect(await sustainment.isAboveMinimum()).to.be.false;

      // Attempt to release tranche
      await expect(
        tfp.releaseTranche(trancheId, proofHash, sealId)
      ).to.be.revertedWith("Sustainment below minimum");
    });

    it("Should allow checking tranche release status with all checks", async function () {
      const trancheId = 1;

      // Initially blocked by sustainment
      let [canRelease, reason] = await tfp.canReleaseTranche(trancheId);
      expect(canRelease).to.be.false;
      expect(reason).to.equal("Sustainment below minimum");

      // Fund sustainment
      const fundAmount = BigInt(MIN_SUSTAINMENT) * 55n;
      await mockToken.connect(investor).approve(await karmaBond.getAddress(), fundAmount);
      await karmaBond.connect(investor).mintBond(fundAmount);

      // Now should be allowed
      [canRelease, reason] = await tfp.canReleaseTranche(trancheId);
      expect(canRelease).to.be.true;

      // Activate veto
      await redCodeVeto.connect(council1).initiateVeto(1, "Block operations");
      
      [canRelease, reason] = await tfp.canReleaseTranche(trancheId);
      expect(canRelease).to.be.false;
      expect(reason).to.equal("Red Code Veto active");
    });
  });

  describe("Emergency Override Scenarios", function () {
    it("Should allow emergency override of Red Code Veto by owner", async function () {
      // Activate veto
      await redCodeVeto.connect(council1).initiateVeto(1, "Test veto");
      expect(await redCodeVeto.operationsAllowed()).to.be.false;

      // Emergency override
      await redCodeVeto.emergencyOverride("Emergency situation requires override");
      expect(await redCodeVeto.operationsAllowed()).to.be.true;

      // Now operations should proceed normally
      const fundAmount = BigInt(MIN_SUSTAINMENT) * 55n;
      await mockToken.connect(investor).approve(await karmaBond.getAddress(), fundAmount);
      await karmaBond.connect(investor).mintBond(fundAmount);

      const trancheId = 1;
      const proofHash = ethers.keccak256(ethers.toUtf8Bytes("proof"));
      
      // Can release without seal if we want
      await tfp.releaseTranche(trancheId, proofHash, ethers.ZeroHash);
      expect(await tfp.trancheReleased(trancheId)).to.be.true;
    });

    it("Should allow disabling governance enforcement", async function () {
      // Activate veto
      await redCodeVeto.connect(council1).initiateVeto(1, "Block");

      // Disable enforcement
      await tfp.setGovernanceEnforcement(false);

      const trancheId = 1;
      const proofHash = ethers.keccak256(ethers.toUtf8Bytes("proof"));

      // Should succeed even with veto active and no sustainment
      await tfp.releaseTranche(trancheId, proofHash, ethers.ZeroHash);
      expect(await tfp.trancheReleased(trancheId)).to.be.true;
    });
  });

  describe("Multiple Tranche Release with Security Checks", function () {
    it("Should handle multiple tranches with individual seals", async function () {
      // Fund sustainment once
      const fundAmount = BigInt(MIN_SUSTAINMENT) * 55n;
      await mockToken.connect(investor).approve(await karmaBond.getAddress(), fundAmount);
      await karmaBond.connect(investor).mintBond(fundAmount);

      // Release multiple tranches
      for (let i = 1; i <= 3; i++) {
        const proofHash = ethers.keccak256(ethers.toUtf8Bytes(`proof ${i}`));
        const actionHash = ethers.keccak256(ethers.toUtf8Bytes(`action ${i}`));
        
        // Create seal for each tranche
        await gCSI.connect(owner).createSeal(actionHash, `Tranche ${i} approval`);
        const sealId = await gCSI.getSealIdByIndex(i - 1);
        await gCSI.connect(council1).signSeal(sealId);
        await gCSI.connect(owner).executeSeal(sealId);

        // Release tranche
        await tfp.releaseTranche(i, proofHash, sealId);
        expect(await tfp.trancheReleased(i)).to.be.true;
        
        // Verify milestone created
        const milestoneId = await tfp.getTrancheMilestone(i);
        expect(await livingCovenantAnchor.isMilestoneSealed(milestoneId)).to.be.true;
      }

      // Verify all milestones tracked
      expect(await livingCovenantAnchor.getMilestoneCount()).to.equal(3);
    });
  });

  describe("Living Covenant Milestone Verification", function () {
    it("Should create proper milestone chain for governance actions", async function () {
      // Fund sustainment
      const fundAmount = BigInt(MIN_SUSTAINMENT) * 55n;
      await mockToken.connect(investor).approve(await karmaBond.getAddress(), fundAmount);
      await karmaBond.connect(investor).mintBond(fundAmount);

      const trancheId = 1;
      const proofHash = ethers.keccak256(ethers.toUtf8Bytes("proof"));
      const actionHash = ethers.keccak256(ethers.toUtf8Bytes("action"));
      
      // Create seal
      await gCSI.connect(owner).createSeal(actionHash, "Approval");
      const sealId = await gCSI.getSealIdByIndex(0);
      await gCSI.connect(council1).signSeal(sealId);
      await gCSI.connect(owner).executeSeal(sealId);

      // Release tranche
      await tfp.releaseTranche(trancheId, proofHash, sealId);

      // Verify milestone details
      const milestoneId = await tfp.getTrancheMilestone(trancheId);
      const milestone = await livingCovenantAnchor.milestones(milestoneId);

      expect(milestone.actionHash).to.equal(proofHash);
      expect(milestone.isSealed).to.be.true;

      // Verify anchor was created
      expect(await livingCovenantAnchor.getAnchorCount()).to.be.greaterThan(0);
      const anchorHash = await livingCovenantAnchor.getAnchorHashByIndex(0);
      expect(await livingCovenantAnchor.verifyAnchor(anchorHash)).to.be.true;
    });
  });
});
