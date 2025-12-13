const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("TFKVerifier", function () {
  let tfkVerifier;
  let owner;
  let verifier1;
  let verifier2;
  let unauthorized;

  beforeEach(async function () {
    [owner, verifier1, verifier2, unauthorized] = await ethers.getSigners();

    const TFKVerifier = await ethers.getContractFactory("TFKVerifier");
    tfkVerifier = await TFKVerifier.deploy();
    await tfkVerifier.waitForDeployment();
  });

  describe("Deployment", function () {
    it("Should set the correct owner", async function () {
      expect(await tfkVerifier.owner()).to.equal(owner.address);
    });

    it("Should authorize owner as verifier by default", async function () {
      expect(await tfkVerifier.authorizedVerifiers(owner.address)).to.be.true;
    });

    it("Should initialize record count to 0", async function () {
      expect(await tfkVerifier.recordCount()).to.equal(0);
    });
  });

  describe("Verifier Authorization", function () {
    it("Should allow owner to authorize verifiers", async function () {
      await expect(tfkVerifier.setAuthorizedVerifier(verifier1.address, true))
        .to.emit(tfkVerifier, "VerifierAuthorized")
        .withArgs(verifier1.address, true);

      expect(await tfkVerifier.authorizedVerifiers(verifier1.address)).to.be.true;
    });

    it("Should allow owner to revoke verifiers", async function () {
      await tfkVerifier.setAuthorizedVerifier(verifier1.address, true);
      
      await expect(tfkVerifier.setAuthorizedVerifier(verifier1.address, false))
        .to.emit(tfkVerifier, "VerifierAuthorized")
        .withArgs(verifier1.address, false);

      expect(await tfkVerifier.authorizedVerifiers(verifier1.address)).to.be.false;
    });

    it("Should reject zero address for verifier", async function () {
      await expect(
        tfkVerifier.setAuthorizedVerifier(ethers.ZeroAddress, true)
      ).to.be.revertedWith("TFKVerifier: invalid verifier address");
    });

    it("Should reject non-owner from authorizing", async function () {
      await expect(
        tfkVerifier.connect(unauthorized).setAuthorizedVerifier(verifier1.address, true)
      ).to.be.revertedWith("TFKVerifier: caller is not the owner");
    });
  });

  describe("Recording Integrity Checks", function () {
    const tfkHash = ethers.keccak256(ethers.toUtf8Bytes("test-tfk-data"));
    const cidReference = "QmTest123456789";

    beforeEach(async function () {
      await tfkVerifier.setAuthorizedVerifier(verifier1.address, true);
    });

    it("Should record valid integrity check", async function () {
      const tx = await tfkVerifier.connect(verifier1).recordIntegrityCheck(
        tfkHash,
        cidReference,
        true
      );

      await expect(tx)
        .to.emit(tfkVerifier, "IntegrityRecorded")
        .withArgs(0, tfkHash, cidReference, await getBlockTimestamp(tx), true);

      expect(await tfkVerifier.recordCount()).to.equal(1);
    });

    it("Should record invalid integrity check and emit violation", async function () {
      const tx = await tfkVerifier.connect(verifier1).recordIntegrityCheck(
        tfkHash,
        cidReference,
        false
      );

      await expect(tx)
        .to.emit(tfkVerifier, "IntegrityViolationDetected")
        .withArgs(0, tfkHash, cidReference);
    });

    it("Should reject empty TFK hash", async function () {
      await expect(
        tfkVerifier.connect(verifier1).recordIntegrityCheck(
          ethers.ZeroHash,
          cidReference,
          true
        )
      ).to.be.revertedWith("TFKVerifier: invalid TFK hash");
    });

    it("Should reject empty CID reference", async function () {
      await expect(
        tfkVerifier.connect(verifier1).recordIntegrityCheck(
          tfkHash,
          "",
          true
        )
      ).to.be.revertedWith("TFKVerifier: invalid CID reference");
    });

    it("Should reject unauthorized verifier", async function () {
      await expect(
        tfkVerifier.connect(unauthorized).recordIntegrityCheck(
          tfkHash,
          cidReference,
          true
        )
      ).to.be.revertedWith("TFKVerifier: caller is not authorized");
    });

    it("Should increment record count correctly", async function () {
      await tfkVerifier.connect(verifier1).recordIntegrityCheck(tfkHash, cidReference, true);
      await tfkVerifier.connect(verifier1).recordIntegrityCheck(tfkHash, "QmTest2", true);
      
      expect(await tfkVerifier.recordCount()).to.equal(2);
    });
  });

  describe("Batch Recording", function () {
    const tfkHashes = [
      ethers.keccak256(ethers.toUtf8Bytes("data1")),
      ethers.keccak256(ethers.toUtf8Bytes("data2")),
      ethers.keccak256(ethers.toUtf8Bytes("data3"))
    ];
    const cidReferences = ["QmTest1", "QmTest2", "QmTest3"];
    const validityFlags = [true, true, false];

    beforeEach(async function () {
      await tfkVerifier.setAuthorizedVerifier(verifier1.address, true);
    });

    it("Should batch record multiple integrity checks", async function () {
      const tx = await tfkVerifier.connect(verifier1).batchRecordIntegrityChecks(
        tfkHashes,
        cidReferences,
        validityFlags
      );

      expect(await tfkVerifier.recordCount()).to.equal(3);
    });

    it("Should reject mismatched array lengths", async function () {
      await expect(
        tfkVerifier.connect(verifier1).batchRecordIntegrityChecks(
          tfkHashes,
          ["QmTest1", "QmTest2"], // Shorter array
          validityFlags
        )
      ).to.be.revertedWith("TFKVerifier: array length mismatch");
    });

    it("Should reject empty arrays", async function () {
      await expect(
        tfkVerifier.connect(verifier1).batchRecordIntegrityChecks([], [], [])
      ).to.be.revertedWith("TFKVerifier: empty arrays");
    });

    it("Should reject batch size too large", async function () {
      const largeBatch = new Array(101).fill(ethers.keccak256(ethers.toUtf8Bytes("test")));
      const largeCids = new Array(101).fill("QmTest");
      const largeFlags = new Array(101).fill(true);

      await expect(
        tfkVerifier.connect(verifier1).batchRecordIntegrityChecks(
          largeBatch,
          largeCids,
          largeFlags
        )
      ).to.be.revertedWith("TFKVerifier: batch size too large");
    });
  });

  describe("Querying Records", function () {
    const tfkHash1 = ethers.keccak256(ethers.toUtf8Bytes("data1"));
    const tfkHash2 = ethers.keccak256(ethers.toUtf8Bytes("data2"));
    const cid1 = "QmTest1";
    const cid2 = "QmTest2";

    beforeEach(async function () {
      await tfkVerifier.setAuthorizedVerifier(verifier1.address, true);
      await tfkVerifier.connect(verifier1).recordIntegrityCheck(tfkHash1, cid1, true);
      await tfkVerifier.connect(verifier1).recordIntegrityCheck(tfkHash2, cid2, false);
    });

    it("Should get integrity record by ID", async function () {
      const record = await tfkVerifier.getIntegrityRecord(0);
      
      expect(record.tfkHash).to.equal(tfkHash1);
      expect(record.cidReference).to.equal(cid1);
      expect(record.verifier).to.equal(verifier1.address);
      expect(record.isValid).to.be.true;
    });

    it("Should reject invalid record ID", async function () {
      await expect(
        tfkVerifier.getIntegrityRecord(999)
      ).to.be.revertedWith("TFKVerifier: invalid record ID");
    });

    it("Should get recent integrity records", async function () {
      const records = await tfkVerifier.getRecentIntegrityRecords(2);
      
      expect(records.length).to.equal(2);
      expect(records[0].tfkHash).to.equal(tfkHash1);
      expect(records[1].tfkHash).to.equal(tfkHash2);
    });

    it("Should handle request for more records than exist", async function () {
      const records = await tfkVerifier.getRecentIntegrityRecords(100);
      
      expect(records.length).to.equal(2);
    });
  });

  describe("Integrity Validation", function () {
    const tfkHash1 = ethers.keccak256(ethers.toUtf8Bytes("valid-data"));
    const tfkHash2 = ethers.keccak256(ethers.toUtf8Bytes("invalid-data"));
    const tfkHash3 = ethers.keccak256(ethers.toUtf8Bytes("unknown-data"));

    beforeEach(async function () {
      await tfkVerifier.setAuthorizedVerifier(verifier1.address, true);
      await tfkVerifier.connect(verifier1).recordIntegrityCheck(tfkHash1, "QmValid", true);
      await tfkVerifier.connect(verifier1).recordIntegrityCheck(tfkHash2, "QmInvalid", false);
    });

    it("Should return true for valid TFK hash", async function () {
      expect(await tfkVerifier.hasValidIntegrity(tfkHash1)).to.be.true;
    });

    it("Should return false for invalid TFK hash", async function () {
      expect(await tfkVerifier.hasValidIntegrity(tfkHash2)).to.be.false;
    });

    it("Should return false for unknown TFK hash", async function () {
      expect(await tfkVerifier.hasValidIntegrity(tfkHash3)).to.be.false;
    });

    it("Should use most recent record for a hash", async function () {
      // Record same hash with different validity
      await tfkVerifier.connect(verifier1).recordIntegrityCheck(tfkHash1, "QmUpdated", false);
      
      expect(await tfkVerifier.hasValidIntegrity(tfkHash1)).to.be.false;
    });
  });

  describe("Violation Counting", function () {
    beforeEach(async function () {
      await tfkVerifier.setAuthorizedVerifier(verifier1.address, true);
    });

    it("Should count violations in time range", async function () {
      const tx1 = await tfkVerifier.connect(verifier1).recordIntegrityCheck(
        ethers.keccak256(ethers.toUtf8Bytes("data1")),
        "QmTest1",
        true
      );
      const time1 = await getBlockTimestamp(tx1);

      const tx2 = await tfkVerifier.connect(verifier1).recordIntegrityCheck(
        ethers.keccak256(ethers.toUtf8Bytes("data2")),
        "QmTest2",
        false
      );
      const time2 = await getBlockTimestamp(tx2);

      await tfkVerifier.connect(verifier1).recordIntegrityCheck(
        ethers.keccak256(ethers.toUtf8Bytes("data3")),
        "QmTest3",
        false
      );

      const count = await tfkVerifier.getViolationCount(time1, time2);
      expect(count).to.equal(1);
    });

    it("Should reject invalid time range", async function () {
      await expect(
        tfkVerifier.getViolationCount(1000, 500)
      ).to.be.revertedWith("TFKVerifier: invalid time range");
    });
  });

  describe("High Load and Edge Cases", function () {
    beforeEach(async function () {
      await tfkVerifier.setAuthorizedVerifier(verifier1.address, true);
    });

    it("Should handle rapid sequential integrity checks", async function () {
      const promises = [];
      for (let i = 0; i < 20; i++) {
        const hash = ethers.keccak256(ethers.toUtf8Bytes(`data${i}`));
        promises.push(
          tfkVerifier.connect(verifier1).recordIntegrityCheck(hash, `QmTest${i}`, i % 2 === 0)
        );
      }
      
      await Promise.all(promises);
      expect(await tfkVerifier.recordCount()).to.equal(20);
    });

    it("Should handle maximum batch size", async function () {
      const maxSize = 100;
      const hashes = Array.from({ length: maxSize }, (_, i) => 
        ethers.keccak256(ethers.toUtf8Bytes(`data${i}`))
      );
      const cids = Array.from({ length: maxSize }, (_, i) => `QmTest${i}`);
      const flags = Array.from({ length: maxSize }, (_, i) => i % 2 === 0);

      await tfkVerifier.connect(verifier1).batchRecordIntegrityChecks(hashes, cids, flags);
      expect(await tfkVerifier.recordCount()).to.equal(100);
    });

    it("Should handle multiple verifiers recording concurrently", async function () {
      await tfkVerifier.setAuthorizedVerifier(verifier2.address, true);

      await Promise.all([
        tfkVerifier.connect(verifier1).recordIntegrityCheck(
          ethers.keccak256(ethers.toUtf8Bytes("v1-data")),
          "QmV1",
          true
        ),
        tfkVerifier.connect(verifier2).recordIntegrityCheck(
          ethers.keccak256(ethers.toUtf8Bytes("v2-data")),
          "QmV2",
          true
        )
      ]);

      expect(await tfkVerifier.recordCount()).to.equal(2);
    });

    it("Should handle long CID references", async function () {
      const longCid = "Qm" + "a".repeat(100);
      await expect(
        tfkVerifier.connect(verifier1).recordIntegrityCheck(
          ethers.keccak256(ethers.toUtf8Bytes("data")),
          longCid,
          true
        )
      ).to.not.be.reverted;
    });
  });

  // Helper function to get block timestamp
  async function getBlockTimestamp(tx) {
    const receipt = await tx.wait();
    const block = await ethers.provider.getBlock(receipt.blockNumber);
    return block.timestamp;
  }
});
