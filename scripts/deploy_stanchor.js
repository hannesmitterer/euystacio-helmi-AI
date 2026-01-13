const hre = require("hardhat");
require("dotenv").config();

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying EuystacioSTAnchor with account:", deployer.address);
  console.log("Account balance:", (await deployer.getBalance()).toString());

  // Configuration from environment or defaults
  const RED_CODE_VETO_AUTHORITY = process.env.RED_CODE_VETO_AUTHORITY || deployer.address;

  console.log("\n=== Deployment Configuration ===");
  console.log("Red Code Veto Authority:", RED_CODE_VETO_AUTHORITY);

  // Deploy EuystacioSTAnchor
  console.log("\n=== Deploying EuystacioSTAnchor ===");
  const EuystacioSTAnchor = await hre.ethers.getContractFactory("EuystacioSTAnchor");
  const anchor = await EuystacioSTAnchor.deploy(RED_CODE_VETO_AUTHORITY);
  await anchor.waitForDeployment();
  const anchorAddress = await anchor.getAddress();
  console.log("✓ EuystacioSTAnchor deployed to:", anchorAddress);

  // Initialize with Red Code IPFS CID if provided
  const RED_CODE_IPFS_CID = process.env.RED_CODE_IPFS_CID;
  if (RED_CODE_IPFS_CID) {
    console.log("\n=== Initializing Red Code IPFS ===");
    const vetoSigner = deployer; // In production, this would be the veto authority signer
    const tx = await anchor.connect(vetoSigner).setRedCodeIPFS(RED_CODE_IPFS_CID);
    await tx.wait();
    console.log("✓ Red Code IPFS CID set:", RED_CODE_IPFS_CID);
  }

  // Register deployment keys if provided
  const DEPLOYMENT_KEY_NAME = process.env.DEPLOYMENT_KEY_NAME;
  const DEPLOYMENT_KEY_HASH = process.env.DEPLOYMENT_KEY_HASH;
  const DEPLOYMENT_KEY_IPFS = process.env.DEPLOYMENT_KEY_IPFS;
  
  if (DEPLOYMENT_KEY_NAME && DEPLOYMENT_KEY_HASH && DEPLOYMENT_KEY_IPFS) {
    console.log("\n=== Registering Deployment Key ===");
    const keyId = hre.ethers.id(DEPLOYMENT_KEY_NAME);
    const tx = await anchor.registerDeploymentKey(
      keyId,
      DEPLOYMENT_KEY_NAME,
      DEPLOYMENT_KEY_HASH,
      DEPLOYMENT_KEY_IPFS
    );
    await tx.wait();
    console.log("✓ Deployment key registered:", DEPLOYMENT_KEY_NAME);
    console.log("  Key ID:", keyId);
  }

  // Set runtime parameters if provided
  const RUNTIME_PARAM_NAME = process.env.RUNTIME_PARAM_NAME;
  const RUNTIME_PARAM_VALUE_HASH = process.env.RUNTIME_PARAM_VALUE_HASH;
  const RUNTIME_PARAM_DESCRIPTION = process.env.RUNTIME_PARAM_DESCRIPTION;
  
  if (RUNTIME_PARAM_NAME && RUNTIME_PARAM_VALUE_HASH) {
    console.log("\n=== Setting Runtime Parameter ===");
    const paramId = hre.ethers.id(RUNTIME_PARAM_NAME);
    const tx = await anchor.setRuntimeParameter(
      paramId,
      RUNTIME_PARAM_NAME,
      RUNTIME_PARAM_VALUE_HASH,
      RUNTIME_PARAM_DESCRIPTION || ""
    );
    await tx.wait();
    console.log("✓ Runtime parameter set:", RUNTIME_PARAM_NAME);
    console.log("  Param ID:", paramId);
  }

  // Anchor governance documents if provided
  const GOV_DOC_NAME = process.env.GOV_DOC_NAME;
  const GOV_DOC_IPFS_CID = process.env.GOV_DOC_IPFS_CID;
  const GOV_DOC_CONTENT_HASH = process.env.GOV_DOC_CONTENT_HASH;
  
  if (GOV_DOC_NAME && GOV_DOC_IPFS_CID && GOV_DOC_CONTENT_HASH) {
    console.log("\n=== Anchoring Governance Document ===");
    const docId = hre.ethers.id(GOV_DOC_NAME);
    const tx = await anchor.anchorGovernanceDocument(
      docId,
      GOV_DOC_NAME,
      GOV_DOC_IPFS_CID,
      GOV_DOC_CONTENT_HASH
    );
    await tx.wait();
    console.log("✓ Governance document anchored:", GOV_DOC_NAME);
    console.log("  Doc ID:", docId);
    console.log("  IPFS CID:", GOV_DOC_IPFS_CID);
  }

  // Update G-CSI anchoring graph if provided
  const GCSI_GRAPH_CID = process.env.GCSI_GRAPH_CID;
  if (GCSI_GRAPH_CID) {
    console.log("\n=== Updating G-CSI Anchoring Graph ===");
    const tx = await anchor.updateGCSIAnchoringGraph(GCSI_GRAPH_CID);
    await tx.wait();
    console.log("✓ G-CSI anchoring graph updated:", GCSI_GRAPH_CID);
  }

  // Optional: Seal deployment if AUTO_SEAL is set
  if (process.env.AUTO_SEAL === "true") {
    console.log("\n=== WARNING: Auto-sealing deployment ===");
    console.log("This action is IRREVERSIBLE!");
    
    // Lock governance state
    const lockTx = await anchor.lockGovernanceState();
    await lockTx.wait();
    console.log("✓ Governance state locked");
    
    // Seal deployment
    const sealTx = await anchor.sealDeployment();
    await sealTx.wait();
    console.log("✓ Deployment sealed");
  }

  // Print summary
  console.log("\n=== Deployment Summary ===");
  console.log("EuystacioSTAnchor:", anchorAddress);
  console.log("Red Code Veto Authority:", RED_CODE_VETO_AUTHORITY);
  console.log("Deployment Sealed:", await anchor.deploymentSealed());
  console.log("Governance Locked:", await anchor.governanceStateLocked());

  // Create deployment artifact
  const deployment = {
    network: hre.network.name,
    deployer: deployer.address,
    timestamp: new Date().toISOString(),
    contracts: {
      EuystacioSTAnchor: anchorAddress
    },
    config: {
      redCodeVetoAuthority: RED_CODE_VETO_AUTHORITY,
      redCodeIPFSCID: RED_CODE_IPFS_CID || "",
      gcsiAnchoringGraphCID: GCSI_GRAPH_CID || ""
    },
    status: {
      deploymentSealed: await anchor.deploymentSealed(),
      governanceStateLocked: await anchor.governanceStateLocked()
    }
  };

  console.log("\n=== Deployment JSON ===");
  console.log(JSON.stringify(deployment, null, 2));
  
  console.log("\n✓ EuystacioSTAnchor deployment complete!");
  console.log("\nSave the contract address and configuration to your .env file");
  console.log("\nNext steps:");
  console.log("1. Verify contract on block explorer");
  console.log("2. Configure deployment keys and runtime parameters");
  console.log("3. Anchor governance documents with IPFS");
  console.log("4. Update G-CSI anchoring graph");
  console.log("5. Lock critical parameters");
  console.log("6. Seal deployment when ready (IRREVERSIBLE)");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
