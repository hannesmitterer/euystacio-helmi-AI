const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying with:", deployer.address);

  // Configuration
  const foundation = "0x5d61a4B25034393A37ef9307C8Ba3aE99e49944b"; // replace with Gnosis Safe in real use
  const seedbringer = deployer.address; // In production, set to actual Seedbringer address
  const initialEthPriceUSD = 200000; // 2000 USD per ETH in cents

  // Deploy EUSDaoGovernance with Seedbringer control
  const Governance = await hre.ethers.getContractFactory("EUSDaoGovernance");
  const governance = await Governance.deploy(seedbringer);
  await governance.deployed();
  console.log("EUSDaoGovernance:", governance.address);
  console.log("  - Seedbringer:", seedbringer);

  // Deploy KarmaBond with minimum investment and redemption fee
  const KarmaBond = await hre.ethers.getContractFactory("KarmaBond");
  const karmabond = await KarmaBond.deploy(foundation, initialEthPriceUSD);
  await karmabond.deployed();
  console.log("KarmaBond:", karmabond.address);
  console.log("  - Foundation Wallet:", foundation);
  console.log("  - Min Investment: 100 USD");
  console.log("  - Redemption Fee: 5%");

  // Deploy TrustlessFundingProtocol_Covenant with oracle and Seedbringer control
  const oracle = deployer.address; // In production, set to actual oracle address
  const TrustlessCovenant = await hre.ethers.getContractFactory("TrustlessFundingProtocol_Covenant");
  const trustlessCovenant = await TrustlessCovenant.deploy(oracle, foundation, seedbringer);
  await trustlessCovenant.deployed();
  console.log("TrustlessFundingProtocol_Covenant:", trustlessCovenant.address);
  console.log("  - Oracle:", oracle);
  console.log("  - Foundation:", foundation);
  console.log("  - Seedbringer:", seedbringer);

  // Also deploy the simple TrustlessFundingProtocol for compatibility
  const Trustless = await hre.ethers.getContractFactory("TrustlessFundingProtocol");
  const trustless = await Trustless.deploy(foundation);
  await trustless.deployed();
  console.log("TrustlessFundingProtocol:", trustless.address);

  // Print deployment summary
  console.log("\n=== Deployment Summary ===");
  console.log("All contracts deployed successfully!");
  console.log("\nContract Addresses:");
  console.log("  EUSDaoGovernance:", governance.address);
  console.log("  KarmaBond:", karmabond.address);
  console.log("  TrustlessFundingProtocol_Covenant:", trustlessCovenant.address);
  console.log("  TrustlessFundingProtocol:", trustless.address);
  console.log("\nKey Features:");
  console.log("  - KarmaBond: 100 USD minimum, 5% redemption fee, flexible duration");
  console.log("  - TrustlessFundingProtocol_Covenant: Automated tranches, Red Code compliance");
  console.log("  - EUSDaoGovernance: Seedbringer control, contribution scoring");
  console.log("\nSave these addresses to your front-end config.");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});