const hre = require("hardhat");
require("dotenv").config();

/**
 * Legacy deployment script - redirects to deploy_karmabond.js
 * For new deployments, use: npx hardhat run scripts/deploy_karmabond.js
 */

console.log("⚠️  This is the legacy deployment script.");
console.log("Please use scripts/deploy_karmabond.js for the new Sustainment-integrated deployment:");
console.log("  npx hardhat run scripts/deploy_karmabond.js --network <network>\n");

// Run the new deployment script
const deploy = require("./deploy_karmabond.js");
