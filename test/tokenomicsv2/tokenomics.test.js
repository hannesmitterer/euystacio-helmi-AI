const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("TokenomicsV2", function () {
  let tokenomics;
  let owner;
  let researcher;
  let validator;
  let provider;
  let operator;
  let distributor;

  const INITIAL_SUPPLY = ethers.parseEther("10000000"); // 10M tokens
  const ETHICAL_RESEARCHERS_POOL = (INITIAL_SUPPLY * 3500n) / 10000n; // 35%
  const DAO_VALIDATORS_POOL = (INITIAL_SUPPLY * 2000n) / 10000n; // 20%
  const TRUSTED_PROVIDERS_POOL = (INITIAL_SUPPLY * 1500n) / 10000n; // 15%
  const OPERATORS_POOL = (INITIAL_SUPPLY * 2000n) / 10000n; // 20%
  const COMMUNITY_RESERVE_POOL = (INITIAL_SUPPLY * 1000n) / 10000n; // 10%

  beforeEach(async function () {
    [owner, researcher, validator, provider, operator, distributor] = await ethers.getSigners();

    const TokenomicsV2 = await ethers.getContractFactory("TokenomicsV2");
    tokenomics = await TokenomicsV2.deploy(INITIAL_SUPPLY);
    await tokenomics.waitForDeployment();
  });

  describe("Deployment", function () {
    it("Should set the correct initial supply", async function () {
      const totalSupply = await tokenomics.totalSupply();
      expect(totalSupply).to.equal(INITIAL_SUPPLY);
    });

    it("Should allocate tokens to pools correctly", async function () {
      expect(await tokenomics.ethicalResearchersPool()).to.equal(ETHICAL_RESEARCHERS_POOL);
      expect(await tokenomics.daoValidatorsPool()).to.equal(DAO_VALIDATORS_POOL);
      expect(await tokenomics.trustedProvidersPool()).to.equal(TRUSTED_PROVIDERS_POOL);
      expect(await tokenomics.operatorsPool()).to.equal(OPERATORS_POOL);
      expect(await tokenomics.communityReservePool()).to.equal(COMMUNITY_RESERVE_POOL);
    });

    it("Should set correct token name and symbol", async function () {
      expect(await tokenomics.name()).to.equal("Sensisara Token");
      expect(await tokenomics.symbol()).to.equal("SENS");
    });
  });

  describe("Distributor Authorization", function () {
    it("Should allow owner to authorize distributor", async function () {
      await tokenomics.setAuthorizedDistributor(distributor.address, true);
      expect(await tokenomics.authorizedDistributors(distributor.address)).to.be.true;
    });

    it("Should emit event when authorizing distributor", async function () {
      await expect(tokenomics.setAuthorizedDistributor(distributor.address, true))
        .to.emit(tokenomics, "DistributorAuthorized")
        .withArgs(distributor.address, true);
    });

    it("Should allow deauthorizing distributor", async function () {
      await tokenomics.setAuthorizedDistributor(distributor.address, true);
      await tokenomics.setAuthorizedDistributor(distributor.address, false);
      expect(await tokenomics.authorizedDistributors(distributor.address)).to.be.false;
    });

    it("Should reject zero address as distributor", async function () {
      await expect(
        tokenomics.setAuthorizedDistributor(ethers.ZeroAddress, true)
      ).to.be.revertedWith("Invalid distributor");
    });

    it("Should reject non-owner authorization", async function () {
      await expect(
        tokenomics.connect(researcher).setAuthorizedDistributor(distributor.address, true)
      ).to.be.revertedWith("Ownable: caller is not the owner");
    });
  });

  describe("Ethical Researcher Rewards", function () {
    beforeEach(async function () {
      await tokenomics.setAuthorizedDistributor(distributor.address, true);
    });

    it("Should distribute rewards to ethical researcher", async function () {
      const rewardAmount = ethers.parseEther("100");
      await tokenomics.connect(distributor).distributeEthicalResearcherReward(
        researcher.address,
        rewardAmount,
        "Dataset validated: QmXyz123"
      );

      expect(await tokenomics.balanceOf(researcher.address)).to.equal(rewardAmount);
    });

    it("Should decrease pool balance", async function () {
      const rewardAmount = ethers.parseEther("100");
      const poolBefore = await tokenomics.ethicalResearchersPool();

      await tokenomics.connect(distributor).distributeEthicalResearcherReward(
        researcher.address,
        rewardAmount,
        "Dataset validated"
      );

      const poolAfter = await tokenomics.ethicalResearchersPool();
      expect(poolAfter).to.equal(poolBefore - rewardAmount);
    });

    it("Should emit reward distributed event", async function () {
      const rewardAmount = ethers.parseEther("100");
      await expect(
        tokenomics.connect(distributor).distributeEthicalResearcherReward(
          researcher.address,
          rewardAmount,
          "Dataset validated"
        )
      )
        .to.emit(tokenomics, "RewardDistributed")
        .withArgs(researcher.address, rewardAmount, 0, "Dataset validated"); // 0 = EthicalResearchers
    });

    it("Should reject unauthorized distributor", async function () {
      const rewardAmount = ethers.parseEther("100");
      await expect(
        tokenomics.connect(researcher).distributeEthicalResearcherReward(
          researcher.address,
          rewardAmount,
          "Dataset validated"
        )
      ).to.be.revertedWith("Not authorized");
    });

    it("Should reject zero amount", async function () {
      await expect(
        tokenomics.connect(distributor).distributeEthicalResearcherReward(
          researcher.address,
          0,
          "Dataset validated"
        )
      ).to.be.revertedWith("Amount must be positive");
    });

    it("Should reject insufficient pool balance", async function () {
      const tooMuch = ETHICAL_RESEARCHERS_POOL + ethers.parseEther("1");
      await expect(
        tokenomics.connect(distributor).distributeEthicalResearcherReward(
          researcher.address,
          tooMuch,
          "Dataset validated"
        )
      ).to.be.revertedWith("Insufficient pool balance");
    });
  });

  describe("DAO Validator Rewards", function () {
    beforeEach(async function () {
      await tokenomics.setAuthorizedDistributor(distributor.address, true);
    });

    it("Should distribute rewards to DAO validator", async function () {
      const rewardAmount = ethers.parseEther("50");
      await tokenomics.connect(distributor).distributeDAOValidatorReward(
        validator.address,
        rewardAmount,
        "Quorum participation"
      );

      expect(await tokenomics.balanceOf(validator.address)).to.equal(rewardAmount);
    });

    it("Should decrease validator pool balance", async function () {
      const rewardAmount = ethers.parseEther("50");
      const poolBefore = await tokenomics.daoValidatorsPool();

      await tokenomics.connect(distributor).distributeDAOValidatorReward(
        validator.address,
        rewardAmount,
        "Quorum participation"
      );

      const poolAfter = await tokenomics.daoValidatorsPool();
      expect(poolAfter).to.equal(poolBefore - rewardAmount);
    });
  });

  describe("Trusted Provider Rewards", function () {
    beforeEach(async function () {
      await tokenomics.setAuthorizedDistributor(distributor.address, true);
    });

    it("Should distribute rewards to trusted provider", async function () {
      const rewardAmount = ethers.parseEther("25");
      await tokenomics.connect(distributor).distributeTrustedProviderReward(
        provider.address,
        rewardAmount,
        "10 queries verified"
      );

      expect(await tokenomics.balanceOf(provider.address)).to.equal(rewardAmount);
    });

    it("Should decrease provider pool balance", async function () {
      const rewardAmount = ethers.parseEther("25");
      const poolBefore = await tokenomics.trustedProvidersPool();

      await tokenomics.connect(distributor).distributeTrustedProviderReward(
        provider.address,
        rewardAmount,
        "Queries verified"
      );

      const poolAfter = await tokenomics.trustedProvidersPool();
      expect(poolAfter).to.equal(poolBefore - rewardAmount);
    });
  });

  describe("Operator Rewards", function () {
    beforeEach(async function () {
      await tokenomics.setAuthorizedDistributor(distributor.address, true);
    });

    it("Should distribute rewards to operator", async function () {
      const rewardAmount = ethers.parseEther("75");
      await tokenomics.connect(distributor).distributeOperatorReward(
        operator.address,
        rewardAmount,
        "Retraining executed: QmAbc456"
      );

      expect(await tokenomics.balanceOf(operator.address)).to.equal(rewardAmount);
    });

    it("Should decrease operator pool balance", async function () {
      const rewardAmount = ethers.parseEther("75");
      const poolBefore = await tokenomics.operatorsPool();

      await tokenomics.connect(distributor).distributeOperatorReward(
        operator.address,
        rewardAmount,
        "Retraining executed"
      );

      const poolAfter = await tokenomics.operatorsPool();
      expect(poolAfter).to.equal(poolBefore - rewardAmount);
    });
  });

  describe("Community Reserve", function () {
    it("Should allow owner to withdraw from community reserve", async function () {
      const withdrawAmount = ethers.parseEther("100");
      await tokenomics.withdrawCommunityReserve(researcher.address, withdrawAmount);

      expect(await tokenomics.balanceOf(researcher.address)).to.equal(withdrawAmount);
    });

    it("Should decrease community reserve pool", async function () {
      const withdrawAmount = ethers.parseEther("100");
      const poolBefore = await tokenomics.communityReservePool();

      await tokenomics.withdrawCommunityReserve(researcher.address, withdrawAmount);

      const poolAfter = await tokenomics.communityReservePool();
      expect(poolAfter).to.equal(poolBefore - withdrawAmount);
    });

    it("Should reject non-owner withdrawal", async function () {
      await expect(
        tokenomics.connect(researcher).withdrawCommunityReserve(researcher.address, ethers.parseEther("100"))
      ).to.be.revertedWith("Ownable: caller is not the owner");
    });
  });

  describe("Inflation Control", function () {
    it("Should not allow inflation minting before period elapsed", async function () {
      const inflationAmount = ethers.parseEther("100000");
      await expect(
        tokenomics.mintInflation(inflationAmount)
      ).to.be.revertedWith("Inflation period not elapsed");
    });

    it("Should allow inflation minting after period", async function () {
      // Fast forward time by 1 year
      await ethers.provider.send("evm_increaseTime", [365 * 24 * 60 * 60]);
      await ethers.provider.send("evm_mine");

      const inflationAmount = ethers.parseEther("100000"); // Well under 5% of 10M
      await tokenomics.mintInflation(inflationAmount);

      expect(await tokenomics.communityReservePool()).to.be.gt(COMMUNITY_RESERVE_POOL);
    });

    it("Should reject inflation exceeding max annual rate", async function () {
      // Fast forward time
      await ethers.provider.send("evm_increaseTime", [365 * 24 * 60 * 60]);
      await ethers.provider.send("evm_mine");

      const tooMuch = ethers.parseEther("600000"); // More than 5% of 10M
      await expect(
        tokenomics.mintInflation(tooMuch)
      ).to.be.revertedWith("Exceeds max annual inflation");
    });

    it("Should emit inflation minted event", async function () {
      await ethers.provider.send("evm_increaseTime", [365 * 24 * 60 * 60]);
      await ethers.provider.send("evm_mine");

      const inflationAmount = ethers.parseEther("100000");
      await expect(tokenomics.mintInflation(inflationAmount))
        .to.emit(tokenomics, "InflationMinted");
    });
  });

  describe("Pool Balance Queries", function () {
    it("Should return correct pool balances", async function () {
      expect(await tokenomics.getPoolBalance(0)).to.equal(ETHICAL_RESEARCHERS_POOL);
      expect(await tokenomics.getPoolBalance(1)).to.equal(DAO_VALIDATORS_POOL);
      expect(await tokenomics.getPoolBalance(2)).to.equal(TRUSTED_PROVIDERS_POOL);
      expect(await tokenomics.getPoolBalance(3)).to.equal(OPERATORS_POOL);
      expect(await tokenomics.getPoolBalance(4)).to.equal(COMMUNITY_RESERVE_POOL);
    });
  });
});
