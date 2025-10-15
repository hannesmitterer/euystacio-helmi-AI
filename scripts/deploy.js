const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying with:", deployer.address);

  const foundation = "0x5d61a4B25034393A37ef9307C8Ba3aE99e49944b"; // replace with Gnosis Safe in real use

  const Governance = await hre.ethers.getContractFactory("EUSDaoGovernance");
  const governance = await Governance.deploy();
  await governance.deployed();
  console.log("EUSDaoGovernance:", governance.address);

  const KarmaBond = await hre.ethers.getContractFactory("KarmaBond");
  const karmabond = await KarmaBond.deploy(foundation);
  await karmabond.deployed();
  console.log("KarmaBond:", karmabond.address);

  const Trustless = await hre.ethers.getContractFactory("TrustlessFundingProtocol");
  const trustless = await Trustless.deploy(foundation);
  await trustless.deployed();
  console.log("TrustlessFundingProtocol:", trustless.address);

  // Print artifacts for front-end
  console.log("Save these addresses to your front-end config.");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});