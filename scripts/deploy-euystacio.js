// Deployment script for Euystacio Framework
// This script deploys all three core contracts with proper configuration

const hre = require("hardhat");

async function main() {
  console.log("Starting Euystacio Framework deployment...");
  
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with account:", deployer.address);
  console.log("Account balance:", (await deployer.getBalance()).toString());

  // Configuration - UPDATE THESE VALUES FOR PRODUCTION
  const FOUNDATION_WALLET = process.env.FOUNDATION_WALLET || deployer.address;
  const SEEDBRINGER_ADDRESS = process.env.SEEDBRINGER_ADDRESS || deployer.address;
  
  console.log("\nConfiguration:");
  console.log("Foundation Wallet:", FOUNDATION_WALLET);
  console.log("Seedbringer Address:", SEEDBRINGER_ADDRESS);
  
  // Verify Seedbringer name seal
  const expectedSeal = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("hannesmitterer"));
  console.log("Seedbringer Name Seal:", expectedSeal);

  // Deploy KarmaBond
  console.log("\n1. Deploying KarmaBond...");
  const KarmaBond = await ethers.getContractFactory("KarmaBond");
  const karmaBond = await KarmaBond.deploy(FOUNDATION_WALLET, SEEDBRINGER_ADDRESS);
  await karmaBond.deployed();
  console.log("KarmaBond deployed to:", karmaBond.address);
  console.log("  - Minimum Contribution: 100 ETH");
  console.log("  - Redemption Fee: 5%");
  console.log("  - Flexible Durations: Enabled");

  // Deploy TrustlessFundingProtocol
  console.log("\n2. Deploying TrustlessFundingProtocol...");
  const TrustlessFundingProtocol = await ethers.getContractFactory("TrustlessFundingProtocol");
  const trustlessFunding = await TrustlessFundingProtocol.deploy(FOUNDATION_WALLET, SEEDBRINGER_ADDRESS);
  await trustlessFunding.deployed();
  console.log("TrustlessFundingProtocol deployed to:", trustlessFunding.address);
  console.log("  - Tranche Automation: Enabled");
  console.log("  - Ethical Compliance Verification: Required");
  console.log("  - Seedbringer Veto Power: Enabled");

  // Deploy EUSDaoGovernance
  console.log("\n3. Deploying EUSDaoGovernance...");
  const EUSDaoGovernance = await ethers.getContractFactory("EUSDaoGovernance");
  const governance = await EUSDaoGovernance.deploy(SEEDBRINGER_ADDRESS);
  await governance.deployed();
  console.log("EUSDaoGovernance deployed to:", governance.address);
  console.log("  - Token Name: Euystacio Stewardship");
  console.log("  - Token Symbol: EUS");
  console.log("  - Seedbringer Sustainment: $10,000/month (togglable)");
  console.log("  - Contribution Scoring: Enabled");

  // Verification
  console.log("\n=== Deployment Verification ===");
  console.log("All contracts verify Seedbringer authority:");
  console.log("KarmaBond Seedbringer:", await karmaBond.SEEDBRINGER());
  console.log("TrustlessFunding Seedbringer:", await trustlessFunding.SEEDBRINGER());
  console.log("Governance Seedbringer:", await governance.SEEDBRINGER());
  
  console.log("\nAll contracts use same name seal:");
  console.log("KarmaBond Seal:", await karmaBond.SEEDBRINGER_NAME_SEAL());
  console.log("TrustlessFunding Seal:", await trustlessFunding.SEEDBRINGER_NAME_SEAL());
  console.log("Governance Seal:", await governance.SEEDBRINGER_NAME_SEAL());

  // Save deployment info
  const deploymentInfo = {
    network: hre.network.name,
    deployer: deployer.address,
    timestamp: new Date().toISOString(),
    contracts: {
      KarmaBond: {
        address: karmaBond.address,
        foundationWallet: FOUNDATION_WALLET,
        seedbringer: SEEDBRINGER_ADDRESS,
        minContribution: "100 ETH",
        redemptionFee: "5%"
      },
      TrustlessFundingProtocol: {
        address: trustlessFunding.address,
        foundationWallet: FOUNDATION_WALLET,
        seedbringer: SEEDBRINGER_ADDRESS
      },
      EUSDaoGovernance: {
        address: governance.address,
        seedbringer: SEEDBRINGER_ADDRESS,
        tokenName: "Euystacio Stewardship",
        tokenSymbol: "EUS",
        monthlySustainment: "$10,000"
      }
    }
  };

  console.log("\n=== Deployment Summary ===");
  console.log(JSON.stringify(deploymentInfo, null, 2));
  
  // Save to file
  const fs = require("fs");
  fs.writeFileSync(
    "deployment-info.json",
    JSON.stringify(deploymentInfo, null, 2)
  );
  console.log("\nDeployment info saved to deployment-info.json");

  console.log("\n✅ Euystacio Framework deployment complete!");
  console.log("\nNext steps:");
  console.log("1. Verify contracts on block explorer (if applicable)");
  console.log("2. Configure foundation wallet if needed");
  console.log("3. Test contract interactions");
  console.log("4. Enable sustainment mechanism when ready (via governance.toggleSustainment)");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
