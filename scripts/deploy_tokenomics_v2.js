// Deployment script for Tokenomics V2.0 system
// Run with: npx hardhat run scripts/deploy_tokenomics_v2.js --network <network>

const hre = require("hardhat");

async function main() {
  console.log("Deploying Tokenomics V2.0 System...");
  
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying contracts with account:", deployer.address);
  
  // Configuration
  const INITIAL_SUPPLY = hre.ethers.parseEther("10000000"); // 10M tokens
  
  // 1. Deploy TokenomicsV2
  console.log("\n1. Deploying TokenomicsV2...");
  const TokenomicsV2 = await hre.ethers.getContractFactory("TokenomicsV2");
  const tokenomics = await TokenomicsV2.deploy(INITIAL_SUPPLY);
  await tokenomics.waitForDeployment();
  const tokenomicsAddress = await tokenomics.getAddress();
  console.log("TokenomicsV2 deployed to:", tokenomicsAddress);
  
  // 2. Deploy EthicalDatasetRegistry
  console.log("\n2. Deploying EthicalDatasetRegistry...");
  const EthicalDatasetRegistry = await hre.ethers.getContractFactory("EthicalDatasetRegistry");
  const datasetRegistry = await EthicalDatasetRegistry.deploy(tokenomicsAddress);
  await datasetRegistry.waitForDeployment();
  const datasetRegistryAddress = await datasetRegistry.getAddress();
  console.log("EthicalDatasetRegistry deployed to:", datasetRegistryAddress);
  
  // 3. Deploy ModelRetrainingEscrow
  console.log("\n3. Deploying ModelRetrainingEscrow...");
  const ModelRetrainingEscrow = await hre.ethers.getContractFactory("ModelRetrainingEscrow");
  const retrainingEscrow = await ModelRetrainingEscrow.deploy(
    tokenomicsAddress, // Using same token for staking
    tokenomicsAddress
  );
  await retrainingEscrow.waitForDeployment();
  const retrainingEscrowAddress = await retrainingEscrow.getAddress();
  console.log("ModelRetrainingEscrow deployed to:", retrainingEscrowAddress);
  
  // 4. Deploy EcosystemInteractionModule
  console.log("\n4. Deploying EcosystemInteractionModule...");
  const EcosystemInteractionModule = await hre.ethers.getContractFactory("EcosystemInteractionModule");
  const eim = await EcosystemInteractionModule.deploy(tokenomicsAddress);
  await eim.waitForDeployment();
  const eimAddress = await eim.getAddress();
  console.log("EcosystemInteractionModule deployed to:", eimAddress);
  
  // 5. Deploy KSyncOracle
  console.log("\n5. Deploying KSyncOracle...");
  const KSyncOracle = await hre.ethers.getContractFactory("KSyncOracle");
  const ksyncOracle = await KSyncOracle.deploy(
    tokenomicsAddress, // Using same token for staking
    tokenomicsAddress
  );
  await ksyncOracle.waitForDeployment();
  const ksyncOracleAddress = await ksyncOracle.getAddress();
  console.log("KSyncOracle deployed to:", ksyncOracleAddress);
  
  // 6. Authorize all distributor contracts
  console.log("\n6. Authorizing distributor contracts...");
  
  console.log("Authorizing EthicalDatasetRegistry...");
  await tokenomics.setAuthorizedDistributor(datasetRegistryAddress, true);
  
  console.log("Authorizing ModelRetrainingEscrow...");
  await tokenomics.setAuthorizedDistributor(retrainingEscrowAddress, true);
  
  console.log("Authorizing EcosystemInteractionModule...");
  await tokenomics.setAuthorizedDistributor(eimAddress, true);
  
  console.log("Authorizing KSyncOracle...");
  await tokenomics.setAuthorizedDistributor(ksyncOracleAddress, true);
  
  console.log("\n✅ All contracts authorized!");
  
  // 7. Display deployment summary
  console.log("\n=== Tokenomics V2.0 Deployment Summary ===");
  console.log("Network:", hre.network.name);
  console.log("Deployer:", deployer.address);
  console.log("\nContract Addresses:");
  console.log("- TokenomicsV2:              ", tokenomicsAddress);
  console.log("- EthicalDatasetRegistry:    ", datasetRegistryAddress);
  console.log("- ModelRetrainingEscrow:     ", retrainingEscrowAddress);
  console.log("- EcosystemInteractionModule:", eimAddress);
  console.log("- KSyncOracle:               ", ksyncOracleAddress);
  
  console.log("\nToken Allocation:");
  console.log("- Ethical Researchers Pool:  ", hre.ethers.formatEther(await tokenomics.ethicalResearchersPool()), "SENS (35%)");
  console.log("- DAO Validators Pool:       ", hre.ethers.formatEther(await tokenomics.daoValidatorsPool()), "SENS (20%)");
  console.log("- Trusted Providers Pool:    ", hre.ethers.formatEther(await tokenomics.trustedProvidersPool()), "SENS (15%)");
  console.log("- Operators Pool:            ", hre.ethers.formatEther(await tokenomics.operatorsPool()), "SENS (20%)");
  console.log("- Community Reserve Pool:    ", hre.ethers.formatEther(await tokenomics.communityReservePool()), "SENS (10%)");
  console.log("- Total Supply:              ", hre.ethers.formatEther(await tokenomics.totalSupply()), "SENS");
  
  console.log("\n✅ Tokenomics V2.0 deployment completed successfully!");
  
  // Save deployment info
  const deploymentInfo = {
    network: hre.network.name,
    deployer: deployer.address,
    timestamp: new Date().toISOString(),
    contracts: {
      TokenomicsV2: tokenomicsAddress,
      EthicalDatasetRegistry: datasetRegistryAddress,
      ModelRetrainingEscrow: retrainingEscrowAddress,
      EcosystemInteractionModule: eimAddress,
      KSyncOracle: ksyncOracleAddress
    },
    config: {
      initialSupply: hre.ethers.formatEther(INITIAL_SUPPLY),
      allocations: {
        ethicalResearchers: "35%",
        daoValidators: "20%",
        trustedProviders: "15%",
        operators: "20%",
        communityReserve: "10%"
      }
    }
  };
  
  const fs = require("fs");
  const path = require("path");
  const deploymentsDir = path.join(__dirname, "..", "deployments");
  
  if (!fs.existsSync(deploymentsDir)) {
    fs.mkdirSync(deploymentsDir);
  }
  
  const deploymentFile = path.join(deploymentsDir, `tokenomics-v2-${hre.network.name}.json`);
  fs.writeFileSync(deploymentFile, JSON.stringify(deploymentInfo, null, 2));
  console.log("\nDeployment info saved to:", deploymentFile);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
