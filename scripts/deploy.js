const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying with:", deployer.address);

  // Foundation wallet - replace with Gnosis Safe in real use
  const foundation = "0x5d61a4B25034393A37ef9307C8Ba3aE99e49944b";
  
  // Seedbringer (hannesmitterer) - replace with actual Seedbringer address
  // This should be the address controlled by hannesmitterer
  const seedbringer = deployer.address; // Placeholder - replace with actual Seedbringer address
  
  console.log("Foundation wallet:", foundation);
  console.log("Seedbringer address:", seedbringer);

  // Deploy EUSDaoGovernance with Seedbringer authority
  const Governance = await hre.ethers.getContractFactory("EUSDaoGovernance");
  const governance = await Governance.deploy(seedbringer);
  await governance.deployed();
  console.log("EUSDaoGovernance deployed to:", governance.address);

  // Deploy KarmaBond with Seedbringer authority
  const KarmaBond = await hre.ethers.getContractFactory("KarmaBond");
  const karmabond = await KarmaBond.deploy(foundation, seedbringer);
  await karmabond.deployed();
  console.log("KarmaBond deployed to:", karmabond.address);

  // Deploy TrustlessFundingProtocol with Seedbringer authority
  const Trustless = await hre.ethers.getContractFactory("TrustlessFundingProtocol");
  const trustless = await Trustless.deploy(foundation, seedbringer);
  await trustless.deployed();
  console.log("TrustlessFundingProtocol deployed to:", trustless.address);

  console.log("\n=== Deployment Summary ===");
  console.log("All contracts deployed with Seedbringer authority");
  console.log("Seedbringer (hannesmitterer) has ultimate control over:");
  console.log("  - KarmaBond: Red Code certification, Seedbringer updates");
  console.log("  - TrustlessFundingProtocol: Tranche veto/release, Red Code certification");
  console.log("  - EUSDaoGovernance: Minting, contribution scoring, governance oversight");
  console.log("\nSave these addresses to your front-end config:");
  console.log({
    governance: governance.address,
    karmaBond: karmabond.address,
    trustlessFunding: trustless.address,
    seedbringer: seedbringer,
    foundation: foundation
  });
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});