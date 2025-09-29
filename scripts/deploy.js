const { ethers } = require("hardhat");

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying with:", deployer.address);

  const foundation = "0x5d61a4B25034393A37ef9307C8Ba3aE99e49944b";

  const Governance = await ethers.getContractFactory("EUSDaoGovernance");
  const governance = await Governance.deploy();
  await governance.deployed();
  console.log("EUSDaoGovernance at:", governance.address);

  const Bond = await ethers.getContractFactory("KarmaBond");
  const bond = await Bond.deploy(foundation, governance.address);
  await bond.deployed();
  console.log("KarmaBond at:", bond.address);

  const Trustless = await ethers.getContractFactory("TrustlessFundingProtocol");
  const trustless = await Trustless.deploy(foundation);
  await trustless.deployed();
  console.log("TrustlessFundingProtocol at:", trustless.address);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});