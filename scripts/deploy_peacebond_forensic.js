const hre = require("hardhat");
require("dotenv").config();

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying PeacebondTreasuryForensic with account:", deployer.address);
  console.log("Account balance:", (await deployer.getBalance()).toString());

  // Configuration from environment or defaults
  const RESONANCE_CREDITS_TOKEN = process.env.RESONANCE_CREDITS_TOKEN || process.env.STABLE_TOKEN_ADDRESS || "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174";
  const BLOCK_DETECTION_THRESHOLD = parseInt(process.env.BLOCK_DETECTION_THRESHOLD || "5");
  const REQUIRED_GUARDIAN_APPROVALS = parseInt(process.env.REQUIRED_GUARDIAN_APPROVALS || "2");
  
  // Backup addresses from environment or defaults
  const BACKUP_ADDRESS_1 = process.env.BACKUP_ADDRESS_1 || deployer.address;
  const BACKUP_ADDRESS_2 = process.env.BACKUP_ADDRESS_2 || "0x5d61a4B25034393A37ef9307C8Ba3aE99e49944b";
  const BACKUP_ADDRESS_3 = process.env.BACKUP_ADDRESS_3 || "0x0000000000000000000000000000000000000001";
  
  // Guardian addresses from environment or defaults
  const GUARDIAN_1 = process.env.GUARDIAN_1 || deployer.address;
  const GUARDIAN_2 = process.env.GUARDIAN_2 || "0x5d61a4B25034393A37ef9307C8Ba3aE99e49944b";
  const GUARDIAN_3 = process.env.GUARDIAN_3 || "0x0000000000000000000000000000000000000001";

  console.log("\n=== Deployment Configuration ===");
  console.log("Resonance Credits Token:", RESONANCE_CREDITS_TOKEN);
  console.log("Block Detection Threshold:", BLOCK_DETECTION_THRESHOLD);
  console.log("Required Guardian Approvals:", REQUIRED_GUARDIAN_APPROVALS);
  console.log("\nBackup Addresses:");
  console.log("  1:", BACKUP_ADDRESS_1);
  console.log("  2:", BACKUP_ADDRESS_2);
  console.log("  3:", BACKUP_ADDRESS_3);
  console.log("\nGuardian Addresses:");
  console.log("  1:", GUARDIAN_1);
  console.log("  2:", GUARDIAN_2);
  console.log("  3:", GUARDIAN_3);

  // Deploy PeacebondTreasuryForensic
  console.log("\n=== Deploying PeacebondTreasuryForensic ===");
  const PeacebondTreasuryForensic = await hre.ethers.getContractFactory("PeacebondTreasuryForensic");
  const treasury = await PeacebondTreasuryForensic.deploy(
    RESONANCE_CREDITS_TOKEN,
    BLOCK_DETECTION_THRESHOLD,
    REQUIRED_GUARDIAN_APPROVALS
  );
  await treasury.deployed();
  console.log("✓ PeacebondTreasuryForensic deployed to:", treasury.address);

  // Configure backup addresses
  console.log("\n=== Configuring Backup Addresses ===");
  if (BACKUP_ADDRESS_1 !== deployer.address) {
    const addBackup1 = await treasury.addBackupAddress(BACKUP_ADDRESS_1);
    await addBackup1.wait();
    console.log("✓ Backup address 1 added:", BACKUP_ADDRESS_1);
  }
  
  const addBackup2 = await treasury.addBackupAddress(BACKUP_ADDRESS_2);
  await addBackup2.wait();
  console.log("✓ Backup address 2 added:", BACKUP_ADDRESS_2);
  
  const addBackup3 = await treasury.addBackupAddress(BACKUP_ADDRESS_3);
  await addBackup3.wait();
  console.log("✓ Backup address 3 added:", BACKUP_ADDRESS_3);

  // Configure guardians
  console.log("\n=== Configuring Guardians ===");
  // Deployer is already a guardian from constructor
  console.log("✓ Guardian 1 (deployer) already authorized:", GUARDIAN_1);
  
  if (GUARDIAN_2 !== deployer.address && GUARDIAN_2 !== "0x0000000000000000000000000000000000000001") {
    const addGuardian2 = await treasury.addGuardian(GUARDIAN_2);
    await addGuardian2.wait();
    console.log("✓ Guardian 2 added:", GUARDIAN_2);
  }
  
  if (GUARDIAN_3 !== deployer.address && GUARDIAN_3 !== "0x0000000000000000000000000000000000000001") {
    const addGuardian3 = await treasury.addGuardian(GUARDIAN_3);
    await addGuardian3.wait();
    console.log("✓ Guardian 3 added:", GUARDIAN_3);
  }

  // Get current status
  console.log("\n=== Contract Status ===");
  const status = await treasury.getStatus();
  console.log("Forensic Switch Active:", status.forensicActive);
  console.log("Treasury Balance:", status.balance.toString());
  console.log("Backup Addresses Count:", status.backupCount.toString());
  console.log("Failed Transaction Count:", status.failedTxCount.toString());
  console.log("Guardian Approvals:", status.approvalCount.toString());
  console.log("Can Activate Forensic:", status.canActivate);

  // Print summary
  console.log("\n=== Deployment Summary ===");
  console.log("PeacebondTreasuryForensic:", treasury.address);
  console.log("Resonance Credits Token:", RESONANCE_CREDITS_TOKEN);
  console.log("Block Detection Threshold:", BLOCK_DETECTION_THRESHOLD);
  console.log("Required Guardian Approvals:", REQUIRED_GUARDIAN_APPROVALS);
  console.log("Backup Addresses:", status.backupCount.toString());

  console.log("\n✓ PeacebondTreasuryForensic deployed and configured successfully!");
  console.log("\nSave this address to your frontend config and .env file");

  // Create deployment artifact
  const deployment = {
    network: hre.network.name,
    deployer: deployer.address,
    timestamp: new Date().toISOString(),
    protocol: "EUYSTACIO/NSR - EU 2026 Compliance",
    contracts: {
      PeacebondTreasuryForensic: treasury.address
    },
    config: {
      resonanceCreditsToken: RESONANCE_CREDITS_TOKEN,
      blockDetectionThreshold: BLOCK_DETECTION_THRESHOLD,
      requiredGuardianApprovals: REQUIRED_GUARDIAN_APPROVALS,
      backupAddresses: [BACKUP_ADDRESS_1, BACKUP_ADDRESS_2, BACKUP_ADDRESS_3],
      guardians: [GUARDIAN_1, GUARDIAN_2, GUARDIAN_3]
    },
    status: {
      forensicSwitchActive: status.forensicActive,
      backupAddressesCount: status.backupCount.toString(),
      canActivateForensic: status.canActivate
    }
  };

  console.log("\n=== Deployment JSON ===");
  console.log(JSON.stringify(deployment, null, 2));

  // Save deployment info to file
  const fs = require("fs");
  const deploymentPath = `deployments/peacebond-treasury-forensic-${hre.network.name}-${Date.now()}.json`;
  
  // Create deployments directory if it doesn't exist
  if (!fs.existsSync("deployments")) {
    fs.mkdirSync("deployments");
  }
  
  fs.writeFileSync(deploymentPath, JSON.stringify(deployment, null, 2));
  console.log("\n✓ Deployment info saved to:", deploymentPath);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
