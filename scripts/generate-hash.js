#!/usr/bin/env node

/**
 * Generate Hash for Executive Master Document
 * 
 * This script generates the SHA-256 hash of the executive master document
 * for use in blockchain anchoring.
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

function generateHash() {
  try {
    // Read document content
    console.log('Reading document from:', DOCUMENT_PATH);
    const content = fs.readFileSync(DOCUMENT_PATH, 'utf8');
    
    // Generate SHA-256 hash
    const hash = crypto.createHash('sha256').update(content).digest('hex');
    
    // Display results
    console.log('\n=== Document Hash Generated ===\n');
    console.log('File:', DOCUMENT_PATH);
    console.log('Size:', content.length, 'bytes');
    console.log('\nSHA-256 Hash (hex):');
    console.log(hash);
    console.log('\nSHA-256 Hash (with 0x prefix for Ethereum):');
    console.log('0x' + hash);
    
    // Save to file
    const hashFile = path.join(__dirname, '..', 'DOCUMENT_HASH.txt');
    fs.writeFileSync(hashFile, `SHA-256: ${hash}\nWith 0x: 0x${hash}\nGenerated: ${new Date().toISOString()}\n`);
    console.log('\nHash saved to:', hashFile);
    
    return hash;
  } catch (error) {
    console.error('Error generating hash:', error.message);
    process.exit(1);
  }
}

// Run if executed directly
if (require.main === module) {
  generateHash();
}

module.exports = { generateHash };
