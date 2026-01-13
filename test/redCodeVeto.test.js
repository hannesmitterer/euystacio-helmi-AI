const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("RedCodeVeto", function () {
  let redCodeVeto;
  let owner;
  let councilMember1;
  let councilMember2;
  let nonMember;

  beforeEach(async function () {
    [owner, councilMember1, councilMember2, nonMember] = await ethers.getSigners();

    const RedCodeVeto = await ethers.getContractFactory("RedCodeVeto");
    redCodeVeto = await RedCodeVeto.deploy();
    await redCodeVeto.waitForDeployment();
  });

  describe("Council Management", function () {
    it("Should add owner as initial council member", async function () {
      expect(await redCodeVeto.councilMembers(owner.address)).to.be.true;
      expect(await redCodeVeto.councilMemberCount()).to.equal(1);
    });

    it("Should allow owner to add council members", async function () {
      await expect(redCodeVeto.addCouncilMember(councilMember1.address))
        .to.emit(redCodeVeto, "CouncilMemberAdded")
        .withArgs(councilMember1.address);

      expect(await redCodeVeto.councilMembers(councilMember1.address)).to.be.true;
      expect(await redCodeVeto.councilMemberCount()).to.equal(2);
    });

    it("Should prevent adding duplicate council members", async function () {
      await redCodeVeto.addCouncilMember(councilMember1.address);
      
      await expect(
        redCodeVeto.addCouncilMember(councilMember1.address)
      ).to.be.revertedWith("RedCodeVeto: Already a member");
    });

    it("Should allow owner to remove council members", async function () {
      await redCodeVeto.addCouncilMember(councilMember1.address);
      await redCodeVeto.addCouncilMember(councilMember2.address);

      await expect(redCodeVeto.removeCouncilMember(councilMember1.address))
        .to.emit(redCodeVeto, "CouncilMemberRemoved")
        .withArgs(councilMember1.address);

      expect(await redCodeVeto.councilMembers(councilMember1.address)).to.be.false;
      expect(await redCodeVeto.councilMemberCount()).to.equal(2);
    });

    it("Should prevent removing members if it would break quorum", async function () {
      // Only owner is a member, required signatures is 1
      await expect(
        redCodeVeto.removeCouncilMember(owner.address)
      ).to.be.revertedWith("RedCodeVeto: Cannot remove, would break quorum");
    });
  });

  describe("Required Signatures", function () {
    beforeEach(async function () {
      await redCodeVeto.addCouncilMember(councilMember1.address);
      await redCodeVeto.addCouncilMember(councilMember2.address);
    });

    it("Should allow owner to update required signatures", async function () {
      await expect(redCodeVeto.setRequiredSignatures(2))
        .to.emit(redCodeVeto, "RequiredSignaturesUpdated")
        .withArgs(1, 2);

      expect(await redCodeVeto.requiredSignatures()).to.equal(2);
    });

    it("Should prevent setting required signatures to 0", async function () {
      await expect(
        redCodeVeto.setRequiredSignatures(0)
      ).to.be.revertedWith("RedCodeVeto: Must require at least 1 signature");
    });

    it("Should prevent setting required signatures above council member count", async function () {
      await expect(
        redCodeVeto.setRequiredSignatures(10)
      ).to.be.revertedWith("RedCodeVeto: Cannot require more signatures than council members");
    });
  });

  describe("Veto Initiation", function () {
    beforeEach(async function () {
      await redCodeVeto.addCouncilMember(councilMember1.address);
    });

    it("Should allow council member to initiate SUSPENDED veto", async function () {
      const reason = "Security concern detected";
      
      const tx = await redCodeVeto.connect(councilMember1).initiateVeto(1, reason); // 1 = SUSPENDED
      const receipt = await tx.wait();
      
      expect(await redCodeVeto.currentState()).to.equal(1); // SUSPENDED
    });

    it("Should allow council member to initiate EMERGENCY veto", async function () {
      const reason = "Critical emergency";
      
      await redCodeVeto.connect(owner).initiateVeto(2, reason); // 2 = EMERGENCY
      
      expect(await redCodeVeto.currentState()).to.equal(2); // EMERGENCY
    });

    it("Should prevent non-council members from initiating veto", async function () {
      await expect(
        redCodeVeto.connect(nonMember).initiateVeto(1, "Reason")
      ).to.be.revertedWith("RedCodeVeto: Not a council member");
    });

    it("Should prevent initiating veto to ACTIVE state", async function () {
      await expect(
        redCodeVeto.connect(owner).initiateVeto(0, "Cannot use ACTIVE") // 0 = ACTIVE
      ).to.be.revertedWith("RedCodeVeto: Use resolveVeto to return to ACTIVE");
    });

    it("Should require a reason for veto", async function () {
      await expect(
        redCodeVeto.connect(owner).initiateVeto(1, "")
      ).to.be.revertedWith("RedCodeVeto: Reason required");
    });

    it("Should emit StateChanged and VetoInitiated events", async function () {
      const reason = "Test veto";
      
      await expect(redCodeVeto.connect(owner).initiateVeto(1, reason))
        .to.emit(redCodeVeto, "StateChanged")
        .to.emit(redCodeVeto, "VetoInitiated");
    });
  });

  describe("Veto Resolution", function () {
    let vetoId;

    beforeEach(async function () {
      await redCodeVeto.addCouncilMember(councilMember1.address);
      const tx = await redCodeVeto.connect(owner).initiateVeto(1, "Test veto");
      const receipt = await tx.wait();
      
      // Get veto ID from history
      vetoId = await redCodeVeto.getVetoIdByIndex(0);
    });

    it("Should allow council member to resolve veto", async function () {
      await expect(redCodeVeto.connect(councilMember1).resolveVeto(vetoId))
        .to.emit(redCodeVeto, "VetoResolved")
        .withArgs(vetoId, councilMember1.address);

      expect(await redCodeVeto.currentState()).to.equal(0); // ACTIVE
    });

    it("Should prevent resolving non-existent veto", async function () {
      const fakeVetoId = ethers.keccak256(ethers.toUtf8Bytes("fake"));
      
      await expect(
        redCodeVeto.connect(owner).resolveVeto(fakeVetoId)
      ).to.be.revertedWith("RedCodeVeto: Veto not active or doesn't exist");
    });

    it("Should prevent resolving already resolved veto", async function () {
      await redCodeVeto.connect(owner).resolveVeto(vetoId);
      
      await expect(
        redCodeVeto.connect(owner).resolveVeto(vetoId)
      ).to.be.revertedWith("RedCodeVeto: Veto not active or doesn't exist");
    });

    it("Should prevent non-council members from resolving veto", async function () {
      await expect(
        redCodeVeto.connect(nonMember).resolveVeto(vetoId)
      ).to.be.revertedWith("RedCodeVeto: Not a council member");
    });
  });

  describe("Emergency Override", function () {
    beforeEach(async function () {
      await redCodeVeto.connect(owner).initiateVeto(1, "Test veto");
    });

    it("Should allow owner to emergency override", async function () {
      const reason = "Emergency override needed";
      
      await expect(redCodeVeto.emergencyOverride(reason))
        .to.emit(redCodeVeto, "StateChanged");

      expect(await redCodeVeto.currentState()).to.equal(0); // ACTIVE
    });

    it("Should prevent non-owner from emergency override", async function () {
      await expect(
        redCodeVeto.connect(nonMember).emergencyOverride("Reason")
      ).to.be.revertedWith("Ownable: caller is not the owner");
    });
  });

  describe("Operations Check", function () {
    it("Should return true when in ACTIVE state", async function () {
      expect(await redCodeVeto.operationsAllowed()).to.be.true;
      expect(await redCodeVeto.isActiveState()).to.be.true;
    });

    it("Should return false when in SUSPENDED state", async function () {
      await redCodeVeto.connect(owner).initiateVeto(1, "Suspend");
      
      expect(await redCodeVeto.operationsAllowed()).to.be.false;
      expect(await redCodeVeto.isActiveState()).to.be.false;
    });

    it("Should return false when in EMERGENCY state", async function () {
      await redCodeVeto.connect(owner).initiateVeto(2, "Emergency");
      
      expect(await redCodeVeto.operationsAllowed()).to.be.false;
      expect(await redCodeVeto.isActiveState()).to.be.false;
    });
  });

  describe("Veto History", function () {
    it("Should track veto history", async function () {
      expect(await redCodeVeto.getVetoCount()).to.equal(0);

      await redCodeVeto.connect(owner).initiateVeto(1, "First veto");
      expect(await redCodeVeto.getVetoCount()).to.equal(1);

      const vetoId1 = await redCodeVeto.getVetoIdByIndex(0);
      await redCodeVeto.connect(owner).resolveVeto(vetoId1);

      await redCodeVeto.connect(owner).initiateVeto(2, "Second veto");
      expect(await redCodeVeto.getVetoCount()).to.equal(2);
    });

    it("Should prevent accessing out of bounds index", async function () {
      await expect(
        redCodeVeto.getVetoIdByIndex(0)
      ).to.be.revertedWith("RedCodeVeto: Index out of bounds");
    });
  });
});
