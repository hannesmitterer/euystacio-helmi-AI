const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("TokenomicsV2 Integration", function () {
  let tokenomics;
  let datasetRegistry;
  let retrainingEscrow;
  let eim;
  let ksyncOracle;
  let owner;
  let researcher;
  let validator1;
  let validator2;
  let provider;
  let operator;

  const INITIAL_SUPPLY = ethers.parseEther("10000000"); // 10M tokens

  beforeEach(async function () {
    [owner, researcher, validator1, validator2, provider, operator] = await ethers.getSigners();

    // Deploy TokenomicsV2
    const TokenomicsV2 = await ethers.getContractFactory("TokenomicsV2");
    tokenomics = await TokenomicsV2.deploy(INITIAL_SUPPLY);
    await tokenomics.waitForDeployment();

    // Deploy EthicalDatasetRegistry
    const EthicalDatasetRegistry = await ethers.getContractFactory("EthicalDatasetRegistry");
    datasetRegistry = await EthicalDatasetRegistry.deploy(await tokenomics.getAddress());
    await datasetRegistry.waitForDeployment();

    // Deploy ModelRetrainingEscrow
    const ModelRetrainingEscrow = await ethers.getContractFactory("ModelRetrainingEscrow");
    retrainingEscrow = await ModelRetrainingEscrow.deploy(
      await tokenomics.getAddress(),
      await tokenomics.getAddress()
    );
    await retrainingEscrow.waitForDeployment();

    // Deploy EcosystemInteractionModule
    const EcosystemInteractionModule = await ethers.getContractFactory("EcosystemInteractionModule");
    eim = await EcosystemInteractionModule.deploy(await tokenomics.getAddress());
    await eim.waitForDeployment();

    // Deploy KSyncOracle
    const KSyncOracle = await ethers.getContractFactory("KSyncOracle");
    ksyncOracle = await KSyncOracle.deploy(
      await tokenomics.getAddress(),
      await tokenomics.getAddress()
    );
    await ksyncOracle.waitForDeployment();

    // Authorize all distributor contracts
    await tokenomics.setAuthorizedDistributor(await datasetRegistry.getAddress(), true);
    await tokenomics.setAuthorizedDistributor(await retrainingEscrow.getAddress(), true);
    await tokenomics.setAuthorizedDistributor(await eim.getAddress(), true);
    await tokenomics.setAuthorizedDistributor(await ksyncOracle.getAddress(), true);
  });

  describe("Complete Dataset Validation Flow", function () {
    it("Should allow complete dataset proposal and reward flow", async function () {
      // 1. Researcher submits dataset proposal
      const tx = await datasetRegistry.connect(researcher).submitProposal(
        "QmDatasetCID123",
        "Fixed critical bias in training data",
        75 // High impact factor
      );
      
      await expect(tx)
        .to.emit(datasetRegistry, "ProposalCreated")
        .withArgs(0, researcher.address, "QmDatasetCID123", 75);

      // 2. Validators vote on the proposal
      await datasetRegistry.connect(validator1).castVote(0, true, ethers.parseEther("1000"));
      await datasetRegistry.connect(validator2).castVote(0, true, ethers.parseEther("1500"));

      // 3. Fast forward past voting period
      await ethers.provider.send("evm_increaseTime", [3 * 24 * 60 * 60 + 1]);
      await ethers.provider.send("evm_mine");

      // 4. Execute proposal
      const researcherBalanceBefore = await tokenomics.balanceOf(researcher.address);
      await datasetRegistry.executeProposal(0);

      // 5. Verify researcher received reward
      const researcherBalanceAfter = await tokenomics.balanceOf(researcher.address);
      expect(researcherBalanceAfter).to.be.gt(researcherBalanceBefore);

      // 6. Distribute validator rewards
      await datasetRegistry.distributeValidatorRewards(0, [validator1.address, validator2.address]);

      // 7. Verify validators received rewards
      expect(await tokenomics.balanceOf(validator1.address)).to.be.gt(0);
      expect(await tokenomics.balanceOf(validator2.address)).to.be.gt(0);
    });

    it("Should calculate rewards based on impact factor", async function () {
      // Submit low impact proposal
      await datasetRegistry.connect(researcher).submitProposal(
        "QmLowImpact",
        "Minor correction",
        10
      );

      // Submit high impact proposal
      await datasetRegistry.connect(researcher).submitProposal(
        "QmHighImpact",
        "Critical fix",
        90
      );

      const lowImpactReward = await datasetRegistry.calculateReward(10);
      const highImpactReward = await datasetRegistry.calculateReward(90);

      expect(highImpactReward).to.be.gt(lowImpactReward);
    });
  });

  describe("Ecosystem Provider Integration", function () {
    it("Should register provider and reward queries", async function () {
      // 1. Register trusted provider
      await eim.registerProvider(provider.address, "Ocean Protocol Integration");

      const [isActive, , , , serviceType, reputationScore] = await eim.getProvider(provider.address);
      expect(isActive).to.be.true;
      expect(serviceType).to.equal("Ocean Protocol Integration");
      expect(reputationScore).to.equal(50); // Default reputation

      // 2. Award integration bonus
      const balanceBefore = await tokenomics.balanceOf(provider.address);
      await eim.awardIntegrationBonus(provider.address, "New Ocean Protocol integration");
      
      const balanceAfter = await tokenomics.balanceOf(provider.address);
      expect(balanceAfter).to.be.gt(balanceBefore);
    });

    it("Should track provider query statistics", async function () {
      await eim.registerProvider(provider.address, "Test Service");

      // Check initial stats
      const [, , totalQueriesBefore, totalRewardsBefore, ,] = await eim.getProvider(provider.address);
      expect(totalQueriesBefore).to.equal(0);
      expect(totalRewardsBefore).to.equal(0);

      // Award integration bonus (which updates stats)
      await eim.awardIntegrationBonus(provider.address, "Integration bonus");

      const [, , totalQueriesAfter, totalRewardsAfter, ,] = await eim.getProvider(provider.address);
      expect(totalRewardsAfter).to.be.gt(totalRewardsBefore);
    });
  });

  describe("K-Sync Operator Automation", function () {
    it("Should register operator and track executions", async function () {
      // Operator needs tokens to stake - withdraw from community reserve
      const stakeAmount = ethers.parseEther("500");
      await tokenomics.withdrawCommunityReserve(operator.address, stakeAmount);
      await tokenomics.connect(operator).approve(await ksyncOracle.getAddress(), stakeAmount);

      // Register operator
      await ksyncOracle.connect(operator).registerOperator(
        stakeAmount,
        "https://ksync.example.com"
      );

      const [isActive, stakedAmount, , totalExecutions, , , endpoint] = 
        await ksyncOracle.getOperator(operator.address);

      expect(isActive).to.be.true;
      expect(stakedAmount).to.equal(stakeAmount);
      expect(totalExecutions).to.equal(0);
      expect(endpoint).to.equal("https://ksync.example.com");
    });

    it("Should complete retraining execution and distribute rewards", async function () {
      // Setup: Register and stake
      const stakeAmount = ethers.parseEther("500");
      await tokenomics.withdrawCommunityReserve(operator.address, stakeAmount);
      await tokenomics.connect(operator).approve(await ksyncOracle.getAddress(), stakeAmount);
      await ksyncOracle.connect(operator).registerOperator(stakeAmount, "https://ksync.example.com");

      // Start execution
      await ksyncOracle.startExecution(
        operator.address,
        "QmDataset123",
        "QmOldModel456"
      );

      // Complete execution
      const balanceBefore = await tokenomics.balanceOf(operator.address);
      await ksyncOracle.completeExecution(0, "QmNewModel789", 100000);

      // Verify reward was distributed
      const balanceAfter = await tokenomics.balanceOf(operator.address);
      expect(balanceAfter).to.be.gt(balanceBefore);

      // Verify execution stats updated
      const [, , , totalExecutions, successfulExecutions, ,] = 
        await ksyncOracle.getOperator(operator.address);
      expect(totalExecutions).to.equal(1);
      expect(successfulExecutions).to.equal(1);
    });
  });

  describe("Cross-Contract Token Flow", function () {
    it("Should maintain correct pool balances across distributions", async function () {
      // Get initial pool balances
      const initialResearchersPool = await tokenomics.ethicalResearchersPool();
      const initialOperatorsPool = await tokenomics.operatorsPool();
      const initialProvidersPool = await tokenomics.trustedProvidersPool();

      // Distribute researcher reward through authorized dataset registry
      const researcherReward = ethers.parseEther("100");
      await datasetRegistry.connect(owner).submitProposal(
        "QmTestCID",
        "Test dataset",
        50
      );
      await datasetRegistry.connect(validator1).castVote(0, true, ethers.parseEther("1000"));
      await ethers.provider.send("evm_increaseTime", [3 * 24 * 60 * 60 + 1]);
      await ethers.provider.send("evm_mine");
      await datasetRegistry.executeProposal(0);

      // Distribute operator reward through authorized oracle
      const stakeAmount = ethers.parseEther("500");
      await tokenomics.withdrawCommunityReserve(operator.address, stakeAmount);
      await tokenomics.connect(operator).approve(await ksyncOracle.getAddress(), stakeAmount);
      await ksyncOracle.connect(operator).registerOperator(stakeAmount, "https://test.com");
      await ksyncOracle.startExecution(operator.address, "QmData", "QmOld");
      await ksyncOracle.completeExecution(0, "QmNew", 100000);

      // Distribute provider reward through authorized EIM
      await eim.registerProvider(provider.address, "Test");
      await eim.awardIntegrationBonus(provider.address, "Test bonus");

      // Verify pools decreased
      expect(await tokenomics.ethicalResearchersPool()).to.be.lt(initialResearchersPool);
      expect(await tokenomics.operatorsPool()).to.be.lt(initialOperatorsPool);
      expect(await tokenomics.trustedProvidersPool()).to.be.lt(initialProvidersPool);

      // Verify total supply remained constant (no inflation yet)
      expect(await tokenomics.totalSupply()).to.equal(INITIAL_SUPPLY);
    });

    it("Should handle multiple reward distributions correctly", async function () {
      // Register provider
      await eim.registerProvider(provider.address, "Test Service");

      // Award multiple integration bonuses
      for (let i = 0; i < 3; i++) {
        await eim.awardIntegrationBonus(provider.address, `Integration ${i}`);
      }

      // Verify provider received all rewards
      const [, , , totalRewards, ,] = await eim.getProvider(provider.address);
      const expectedRewards = (await eim.integrationBonus()) * 3n;
      expect(totalRewards).to.equal(expectedRewards);
    });
  });

  describe("Authorization and Security", function () {
    it("Should prevent unauthorized distributions", async function () {
      await expect(
        tokenomics.connect(researcher).distributeEthicalResearcherReward(
          researcher.address,
          ethers.parseEther("100"),
          "Unauthorized"
        )
      ).to.be.revertedWith("Not authorized");
    });

    it("Should allow owner to authorize/deauthorize distributors", async function () {
      const newDistributor = validator1.address;

      // Initially not authorized
      expect(await tokenomics.authorizedDistributors(newDistributor)).to.be.false;

      // Authorize
      await tokenomics.setAuthorizedDistributor(newDistributor, true);
      expect(await tokenomics.authorizedDistributors(newDistributor)).to.be.true;

      // Can now distribute
      await tokenomics.connect(validator1).distributeEthicalResearcherReward(
        researcher.address,
        ethers.parseEther("10"),
        "Authorized distribution"
      );

      // Deauthorize
      await tokenomics.setAuthorizedDistributor(newDistributor, false);
      
      // Cannot distribute anymore
      await expect(
        tokenomics.connect(validator1).distributeEthicalResearcherReward(
          researcher.address,
          ethers.parseEther("10"),
          "Should fail"
        )
      ).to.be.revertedWith("Not authorized");
    });
  });
});
