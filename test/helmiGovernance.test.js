const { expect } = require("chai");
const { ethers } = require("hardhat");
const { time } = require("@nomicfoundation/hardhat-network-helpers");

describe("HelmiGovernance - Sensisara Principle Implementation", function () {
  let helmiGov;
  let owner, proposer, voter1, voter2, voter3;
  
  const PROPOSAL_COOLDOWN = 3 * 24 * 60 * 60; // 3 days
  const VOTING_PERIOD = 7 * 24 * 60 * 60; // 7 days
  const QUORUM_PERCENTAGE = 30;
  
  beforeEach(async function () {
    [owner, proposer, voter1, voter2, voter3] = await ethers.getSigners();
    
    const HelmiGovernance = await ethers.getContractFactory("HelmiGovernance");
    helmiGov = await HelmiGovernance.deploy();
    await helmiGov.waitForDeployment();
    
    // Mint tokens to enable governance participation
    await helmiGov.mint(proposer.address, ethers.parseEther("100"));
    await helmiGov.mint(voter1.address, ethers.parseEther("100"));
    await helmiGov.mint(voter2.address, ethers.parseEther("100"));
    await helmiGov.mint(voter3.address, ethers.parseEther("50"));
  });
  
  describe("Deployment", function () {
    it("Should set the correct token name and symbol", async function () {
      expect(await helmiGov.name()).to.equal("Helmi Governance Token");
      expect(await helmiGov.symbol()).to.equal("HELMI");
    });
    
    it("Should have correct governance parameters", async function () {
      expect(await helmiGov.PROPOSAL_COOLDOWN()).to.equal(PROPOSAL_COOLDOWN);
      expect(await helmiGov.VOTING_PERIOD()).to.equal(VOTING_PERIOD);
      expect(await helmiGov.QUORUM_PERCENTAGE()).to.equal(QUORUM_PERCENTAGE);
    });
  });
  
  describe("Voting Power - Sensisara Pattern", function () {
    it("Should calculate voting power based on balance and contribution", async function () {
      // Base voting power (balance * 1 when no contribution score)
      expect(await helmiGov.votingPower(voter1.address)).to.equal(ethers.parseEther("100"));
      
      // Set contribution score
      await helmiGov.setContributionScore(voter1.address, 2);
      
      // Enhanced voting power (balance * (1 + contribution))
      expect(await helmiGov.votingPower(voter1.address)).to.equal(ethers.parseEther("300"));
    });
    
    it("Should emit event when contribution score is updated", async function () {
      await expect(helmiGov.setContributionScore(voter1.address, 5))
        .to.emit(helmiGov, "ContributionScoreUpdated")
        .withArgs(voter1.address, 5);
    });
  });
  
  describe("Proposal Creation - Natural Constraints", function () {
    it("Should create a proposal with IPFS CID", async function () {
      const ipfsCid = "QmT6S1Z7d3hJ9kL5mN2xV8pQzYvXwA8bC0dE1fG2H3I4J5";
      const title = "Test Proposal";
      
      const tx = await helmiGov.connect(proposer).createProposal(ipfsCid, title);
      const receipt = await tx.wait();
      const block = await ethers.provider.getBlock(receipt.blockNumber);
      
      await expect(tx)
        .to.emit(helmiGov, "ProposalCreated")
        .withArgs(1, proposer.address, ipfsCid, title, block.timestamp, block.timestamp + VOTING_PERIOD);
      
      expect(await helmiGov.proposalCount()).to.equal(1);
    });
    
    it("Should require IPFS CID", async function () {
      await expect(
        helmiGov.connect(proposer).createProposal("", "Test")
      ).to.be.revertedWith("IPFS CID required for verifiability");
    });
    
    it("Should require title", async function () {
      await expect(
        helmiGov.connect(proposer).createProposal("QmXxx", "")
      ).to.be.revertedWith("Title required");
    });
    
    it("Should require token balance to propose", async function () {
      const [_, __, ___, ____, noTokens] = await ethers.getSigners();
      
      await expect(
        helmiGov.connect(noTokens).createProposal("QmXxx", "Test")
      ).to.be.revertedWith("Must hold tokens to propose");
    });
    
    it("Should enforce cooldown period (circadian rhythm)", async function () {
      await helmiGov.connect(proposer).createProposal("QmXxx1", "Proposal 1");
      
      await expect(
        helmiGov.connect(proposer).createProposal("QmXxx2", "Proposal 2")
      ).to.be.revertedWith("Cooldown period active - system needs rest");
    });
    
    it("Should allow proposal after cooldown period", async function () {
      await helmiGov.connect(proposer).createProposal("QmXxx1", "Proposal 1");
      
      // Advance time past cooldown
      await time.increase(PROPOSAL_COOLDOWN + 1);
      
      await expect(
        helmiGov.connect(proposer).createProposal("QmXxx2", "Proposal 2")
      ).to.emit(helmiGov, "ProposalCreated");
    });
    
    it("Should enforce rate limiting (refractory period)", async function () {
      const RATE_LIMIT_WINDOW = 24 * 60 * 60; // 1 day
      const MAX_PROPOSALS = 3;
      
      // Create multiple proposers with tokens
      const proposers = [proposer, voter1, voter2, voter3];
      
      // First 3 proposals should succeed
      for (let i = 0; i < MAX_PROPOSALS; i++) {
        await helmiGov.connect(proposers[i]).createProposal(`QmXxx${i}`, `Proposal ${i}`);
        await time.increase(PROPOSAL_COOLDOWN + 1);
      }
      
      // 4th proposal in same window should fail
      await expect(
        helmiGov.connect(proposer).createProposal("QmXxx4", "Proposal 4")
      ).to.be.revertedWith("Rate limit exceeded - too many proposals in this period");
    });
  });
  
  describe("Voting - Quorum Sensing", function () {
    let proposalId;
    
    beforeEach(async function () {
      const tx = await helmiGov.connect(proposer).createProposal("QmXxx", "Test Proposal");
      await tx.wait();
      proposalId = 1;
    });
    
    it("Should allow voting with correct weight", async function () {
      await expect(helmiGov.connect(voter1).vote(proposalId, true))
        .to.emit(helmiGov, "VoteCast")
        .withArgs(proposalId, voter1.address, true, ethers.parseEther("100"));
      
      const proposal = await helmiGov.getProposal(proposalId);
      expect(proposal.votesFor).to.equal(ethers.parseEther("100"));
    });
    
    it("Should prevent double voting", async function () {
      await helmiGov.connect(voter1).vote(proposalId, true);
      
      await expect(
        helmiGov.connect(voter1).vote(proposalId, true)
      ).to.be.revertedWith("Already voted");
    });
    
    it("Should check if user has voted", async function () {
      expect(await helmiGov.hasVoted(proposalId, voter1.address)).to.be.false;
      
      await helmiGov.connect(voter1).vote(proposalId, true);
      
      expect(await helmiGov.hasVoted(proposalId, voter1.address)).to.be.true;
    });
    
    it("Should require voting during voting period", async function () {
      // Advance past voting period
      await time.increase(VOTING_PERIOD + 1);
      
      await expect(
        helmiGov.connect(voter1).vote(proposalId, true)
      ).to.be.revertedWith("Voting ended");
    });
    
    it("Should calculate quorum correctly (30%)", async function () {
      // Total supply = 350 tokens
      // Quorum = 105 tokens (30%)
      
      // Vote with 100 tokens - should not reach quorum
      await helmiGov.connect(voter1).vote(proposalId, true);
      expect(await helmiGov.hasQuorum(proposalId)).to.be.false;
      
      // Vote with another 50 tokens - should reach quorum
      await helmiGov.connect(voter3).vote(proposalId, false);
      expect(await helmiGov.hasQuorum(proposalId)).to.be.true;
    });
    
    it("Should determine if proposal passed", async function () {
      // More votes for than against
      await helmiGov.connect(voter1).vote(proposalId, true);
      await helmiGov.connect(voter2).vote(proposalId, true);
      await helmiGov.connect(voter3).vote(proposalId, false);
      
      expect(await helmiGov.isPassed(proposalId)).to.be.true;
    });
  });
  
  describe("Proposal Execution", function () {
    let proposalId;
    
    beforeEach(async function () {
      const tx = await helmiGov.connect(proposer).createProposal("QmXxx", "Test Proposal");
      await tx.wait();
      proposalId = 1;
      
      // Vote to reach quorum and pass
      await helmiGov.connect(voter1).vote(proposalId, true);
      await helmiGov.connect(voter2).vote(proposalId, true);
      await helmiGov.connect(voter3).vote(proposalId, false);
    });
    
    it("Should execute proposal after voting period ends", async function () {
      // Advance past voting period
      await time.increase(VOTING_PERIOD + 1);
      
      await expect(helmiGov.executeProposal(proposalId))
        .to.emit(helmiGov, "ProposalExecuted")
        .withArgs(proposalId);
      
      const proposal = await helmiGov.getProposal(proposalId);
      expect(proposal.executed).to.be.true;
    });
    
    it("Should require quorum to execute", async function () {
      // Create new proposal with insufficient votes
      await time.increase(PROPOSAL_COOLDOWN + 1);
      const tx = await helmiGov.connect(proposer).createProposal("QmYyy", "Low Quorum");
      await tx.wait();
      const newProposalId = 2;
      
      // Only one small vote
      await helmiGov.connect(voter3).vote(newProposalId, true);
      
      // Advance past voting period
      await time.increase(VOTING_PERIOD + 1);
      
      await expect(
        helmiGov.executeProposal(newProposalId)
      ).to.be.revertedWith("Quorum not reached");
    });
    
    it("Should require proposal to have passed", async function () {
      // Create new proposal that will fail
      await time.increase(PROPOSAL_COOLDOWN + 1);
      const tx = await helmiGov.connect(proposer).createProposal("QmZzz", "Failing Proposal");
      await tx.wait();
      const failProposalId = 2;
      
      // Vote against
      await helmiGov.connect(voter1).vote(failProposalId, false);
      await helmiGov.connect(voter2).vote(failProposalId, false);
      
      // Advance past voting period
      await time.increase(VOTING_PERIOD + 1);
      
      await expect(
        helmiGov.executeProposal(failProposalId)
      ).to.be.revertedWith("Proposal not passed");
    });
  });
  
  describe("Proposal Cancellation", function () {
    it("Should allow owner to cancel proposal", async function () {
      const tx = await helmiGov.connect(proposer).createProposal("QmXxx", "Test");
      await tx.wait();
      
      await expect(helmiGov.cancelProposal(1))
        .to.emit(helmiGov, "ProposalCancelled")
        .withArgs(1);
      
      const proposal = await helmiGov.getProposal(1);
      expect(proposal.cancelled).to.be.true;
    });
    
    it("Should prevent execution of cancelled proposals", async function () {
      const tx = await helmiGov.connect(proposer).createProposal("QmXxx", "Test");
      await tx.wait();
      
      await helmiGov.cancelProposal(1);
      
      await expect(
        helmiGov.connect(voter1).vote(1, true)
      ).to.be.revertedWith("Proposal cancelled");
    });
  });
  
  describe("Proposal Data Retrieval", function () {
    it("Should retrieve complete proposal data", async function () {
      const ipfsCid = "QmT6S1Z7d3hJ9kL5mN2xV8pQzYvXwA8bC0dE1fG2H3I4J5";
      const title = "Integration Test";
      
      await helmiGov.connect(proposer).createProposal(ipfsCid, title);
      
      const proposal = await helmiGov.getProposal(1);
      
      expect(proposal.proposer).to.equal(proposer.address);
      expect(proposal.ipfsCid).to.equal(ipfsCid);
      expect(proposal.title).to.equal(title);
      expect(proposal.votesFor).to.equal(0);
      expect(proposal.votesAgainst).to.equal(0);
      expect(proposal.executed).to.be.false;
      expect(proposal.cancelled).to.be.false;
    });
  });
});
