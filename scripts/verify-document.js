#!/usr/bin/env node

/**
 * Verify Document Integrity
 * 
 * This script verifies the integrity of the executive master document
 * against a provided hash or on-chain anchor.
 */

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

// Path to the master document
const DOCUMENT_PATH = path.join(
  __dirname,
  '..',
  'docs',
  'governance',
  'EXECUTIVE_MASTER_DOCUMENT.md'
);

function computeDocumentHash() {
  const content = fs.readFileSync(DOCUMENT_PATH, 'utf8');
  return crypto.createHash('sha256').update(content).digest('hex');
}

function verifyHash(expectedHash) {
  // Remove 0x prefix if present
  expectedHash = expectedHash.replace(/^0x/, '');
  
  console.log('Verifying document integrity...\n');
  console.log('Document:', DOCUMENT_PATH);
  
  // Compute current hash
  const actualHash = computeDocumentHash();
  
  console.log('\nExpected Hash:', expectedHash);
  console.log('Actual Hash:  ', actualHash);
  
  // Compare hashes
  const isValid = actualHash === expectedHash;
  
  console.log('\nVerification Result:', isValid ? '✅ VALID' : '❌ INVALID');
  
  if (!isValid) {
    console.log('\n⚠️  WARNING: Document has been modified since the hash was generated!');
    console.log('The content does not match the expected hash.');
  } else {
    console.log('\n✅ Document integrity verified!');
    console.log('The content matches the expected hash exactly.');
  }
  
  return isValid;
}

async function verifyOnChain(contractAddress, anchorId) {
  console.log('Verifying against blockchain anchor...\n');
  
  try {
    // This would require ethers.js and network connection
    // For now, provide instructions
    console.log('To verify on-chain:');
    console.log('1. Visit https://sepolia.etherscan.io/address/' + contractAddress);
    console.log('2. Navigate to "Read Contract"');
    console.log('3. Call getAnchor(' + anchorId + ')');
    console.log('4. Compare documentHash with computed hash');
    
    const actualHash = computeDocumentHash();
    console.log('\nComputed Hash: 0x' + actualHash);
    console.log('\nCompare this with the on-chain hash value.');
    
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// Command line interface
const args = process.argv.slice(2);

if (args.length === 0) {
  console.log('Usage:');
  console.log('  node verify-document.js <hash>           - Verify against provided hash');
  console.log('  node verify-document.js <contract> <id>  - Verify against blockchain anchor');
  console.log('  node verify-document.js --current        - Show current hash');
  process.exit(0);
}

if (args[0] === '--current') {
  const hash = computeDocumentHash();
  console.log('Current Document Hash:');
  console.log(hash);
  console.log('\nWith 0x prefix:');
  console.log('0x' + hash);
} else if (args.length === 1) {
  // Hash verification
  verifyHash(args[0]);
} else if (args.length === 2) {
  // On-chain verification
  verifyOnChain(args[0], args[1]);
} else {
  console.error('Invalid arguments. Use --help for usage information.');
  process.exit(1);
}

module.exports = { verifyHash, computeDocumentHash };
