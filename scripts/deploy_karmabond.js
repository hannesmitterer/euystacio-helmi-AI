const hre = require("hardhat");
require("dotenv").config();

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying with account:", deployer.address);
  console.log("Account balance:", (await deployer.getBalance()).toString());

  // Configuration from environment or defaults
  const FOUNDATION_WALLET = process.env.FOUNDATION_WALLET || "0x5d61a4B25034393A37ef9307C8Ba3aE99e49944b";
  const STABLE_TOKEN = process.env.STABLE_TOKEN_ADDRESS || "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"; // USDC on Polygon
  const STABLE_DECIMALS = 6; // USDC has 6 decimals
  const SUSTAINMENT_MIN_USD = parseInt(process.env.SUSTAINMENT_MIN_USD || "10000");
  const SUSTAINMENT_PERCENT_BPS = parseInt(process.env.SUSTAINMENT_PERCENT_BPS || "200");

  console.log("\n=== Deployment Configuration ===");
  console.log("Foundation Wallet:", FOUNDATION_WALLET);
  console.log("Stable Token:", STABLE_TOKEN);
  console.log("Stable Decimals:", STABLE_DECIMALS);
  console.log("Sustainment Minimum (USD):", SUSTAINMENT_MIN_USD);
  console.log("Sustainment Percent (BPS):", SUSTAINMENT_PERCENT_BPS);

  // 1. Deploy Sustainment Contract
  console.log("\n=== Deploying Sustainment ===");
  const Sustainment = await hre.ethers.getContractFactory("Sustainment");
  const sustainment = await Sustainment.deploy(
    STABLE_TOKEN,
    STABLE_DECIMALS,
    SUSTAINMENT_MIN_USD
  );
  await sustainment.deployed();
  console.log("✓ Sustainment deployed to:", sustainment.address);

  // 2. Deploy EUSDaoGovernance
  console.log("\n=== Deploying EUSDaoGovernance ===");
  const Governance = await hre.ethers.getContractFactory("EUSDaoGovernance");
  const governance = await Governance.deploy();
  await governance.deployed();
  console.log("✓ EUSDaoGovernance deployed to:", governance.address);

  // 3. Deploy KarmaBond
  console.log("\n=== Deploying KarmaBond ===");
  const KarmaBond = await hre.ethers.getContractFactory("KarmaBond");
  const karmaBond = await KarmaBond.deploy(
    STABLE_TOKEN,
    sustainment.address,
    FOUNDATION_WALLET,
    SUSTAINMENT_PERCENT_BPS
  );
  await karmaBond.deployed();
  console.log("✓ KarmaBond deployed to:", karmaBond.address);

  // 4. Authorize KarmaBond in Sustainment
  console.log("\n=== Configuring Sustainment ===");
  const authTx = await sustainment.setAuthorizedDepositor(karmaBond.address, true);
  await authTx.wait();
  console.log("✓ KarmaBond authorized as depositor");

  // 5. Deploy TrustlessFundingProtocol
  console.log("\n=== Deploying TrustlessFundingProtocol ===");
  const TFP = await hre.ethers.getContractFactory("TrustlessFundingProtocol");
  const tfp = await TFP.deploy(FOUNDATION_WALLET);
  await tfp.deployed();
  console.log("✓ TrustlessFundingProtocol deployed to:", tfp.address);

  // 6. Configure TFP with Sustainment
  console.log("\n=== Configuring TrustlessFundingProtocol ===");
  const setSustainmentTx = await tfp.setSustainmentContract(sustainment.address);
  await setSustainmentTx.wait();
  console.log("✓ Sustainment contract configured in TFP");

  // Print summary
  console.log("\n=== Deployment Summary ===");
  console.log("Sustainment:", sustainment.address);
  console.log("EUSDaoGovernance:", governance.address);
  console.log("KarmaBond:", karmaBond.address);
  console.log("TrustlessFundingProtocol:", tfp.address);

  console.log("\n=== Configuration ===");
  console.log("Stable Token:", STABLE_TOKEN);
  console.log("Foundation Wallet:", FOUNDATION_WALLET);
  console.log("Sustainment Min:", SUSTAINMENT_MIN_USD, "USD");
  console.log("Sustainment Percent:", SUSTAINMENT_PERCENT_BPS / 100, "%");

  console.log("\n✓ All contracts deployed and configured successfully!");
  console.log("\nSave these addresses to your frontend config and .env file");

  // Create deployment artifact
  const deployment = {
    network: hre.network.name,
    deployer: deployer.address,
    timestamp: new Date().toISOString(),
    contracts: {
      Sustainment: sustainment.address,
      EUSDaoGovernance: governance.address,
      KarmaBond: karmaBond.address,
      TrustlessFundingProtocol: tfp.address
    },
    config: {
      stableToken: STABLE_TOKEN,
      foundationWallet: FOUNDATION_WALLET,
      sustainmentMinUSD: SUSTAINMENT_MIN_USD,
      sustainmentPercentBPS: SUSTAINMENT_PERCENT_BPS
    }
  };

  console.log("\n=== Deployment JSON ===");
  console.log(JSON.stringify(deployment, null, 2));
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
