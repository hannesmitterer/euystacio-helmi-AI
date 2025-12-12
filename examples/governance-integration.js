/**
 * Example: Web3 Governance Integration
 * Demonstrates how to use the Euystacio-Helmi SDK for governance operations
 */

const { EuystacioHelmiSDK } = require('../sdk/index.js');
require('dotenv').config();

async function main() {
  console.log('🌿 Euystacio-Helmi SDK - Governance Example\n');
  
  // Initialize SDK
  const sdk = new EuystacioHelmiSDK({
    rpcUrl: process.env.RPC_URL || 'http://localhost:8545',
    privateKey: process.env.PRIVATE_KEY,
    governanceAddress: process.env.GOVERNANCE_ADDRESS
  });
  
  try {
    await sdk.initialize();
    console.log('✅ SDK initialized successfully\n');
    
    // Get governance parameters
    console.log('📋 Governance Parameters:');
    const params = await sdk.getGovernanceParams();
    console.log(`   Cooldown Period: ${params.proposalCooldown} seconds`);
    console.log(`   Voting Period: ${params.votingPeriod} seconds`);
    console.log(`   Quorum Required: ${params.quorumPercentage}%`);
    console.log(`   Rate Limit Window: ${params.rateLimitWindow} seconds`);
    console.log(`   Max Proposals/Window: ${params.maxProposalsPerWindow}\n`);
    
    // Check voting power
    console.log('🗳️  Voting Power:');
    const power = await sdk.getVotingPower();
    console.log(`   Your voting power: ${power}\n`);
    
    // Example 1: Create a proposal
    console.log('📝 Example 1: Creating a Proposal');
    console.log('   (This requires tokens and will consume gas)');
    
    const ipfsCid = 'QmT6S1Z7d3hJ9kL5mN2xV8pQzYvXwA8bC0dE1fG2H3I4J5';
    const title = 'Example Governance Proposal';
    
    console.log(`   IPFS CID: ${ipfsCid}`);
    console.log(`   Title: ${title}`);
    
    // Uncomment to actually create a proposal:
    /*
    const result = await sdk.createProposal(ipfsCid, title);
    console.log(`   ✅ Proposal created! ID: ${result.proposalId}`);
    console.log(`   Transaction: ${result.receipt.hash}\n`);
    */
    console.log('   ⚠️  Skipped (uncomment to execute)\n');
    
    // Example 2: Get proposal details
    console.log('📊 Example 2: Fetching Proposal Details');
    const proposalCount = await sdk.getProposalCount();
    console.log(`   Total proposals: ${proposalCount}`);
    
    if (proposalCount > 0) {
      const proposal = await sdk.getProposal(1);
      console.log(`   Proposal #1:`);
      console.log(`     Title: ${proposal.title}`);
      console.log(`     IPFS CID: ${proposal.ipfsCid}`);
      console.log(`     Proposer: ${proposal.proposer}`);
      console.log(`     Votes For: ${proposal.votesFor}`);
      console.log(`     Votes Against: ${proposal.votesAgainst}`);
      console.log(`     Status: ${proposal.executed ? 'Executed' : 'Active'}`);
      console.log(`     Start: ${proposal.startTime.toISOString()}`);
      console.log(`     End: ${proposal.endTime.toISOString()}\n`);
      
      // Check quorum and pass status
      const hasQuorum = await sdk.hasQuorum(1);
      const isPassed = await sdk.isPassed(1);
      console.log(`   Quorum reached: ${hasQuorum ? '✅' : '❌'}`);
      console.log(`   Proposal passing: ${isPassed ? '✅' : '❌'}\n`);
    } else {
      console.log('   No proposals yet.\n');
    }
    
    // Example 3: Vote on a proposal
    console.log('🗳️  Example 3: Voting on a Proposal');
    if (proposalCount > 0) {
      const hasVoted = await sdk.hasVoted(1);
      console.log(`   Already voted on proposal #1: ${hasVoted ? 'Yes' : 'No'}`);
      
      if (!hasVoted) {
        console.log('   (Uncomment to vote)');
        // Uncomment to vote:
        /*
        const voteReceipt = await sdk.vote(1, true); // true = vote yes
        console.log(`   ✅ Vote cast!`);
        console.log(`   Transaction: ${voteReceipt.hash}\n`);
        */
      }
    }
    console.log('   ⚠️  Skipped (uncomment to execute)\n');
    
    // Example 4: Verify IPFS document
    console.log('📦 Example 4: IPFS Verification');
    const verification = await sdk.verifyIPFSCID(ipfsCid);
    console.log(`   CID: ${verification.cid}`);
    console.log(`   Valid: ${verification.valid ? '✅' : '❌'}`);
    if (verification.valid) {
      console.log(`   Content length: ${verification.contentLength} bytes`);
      console.log(`   Preview: ${verification.content.substring(0, 100)}...`);
    } else {
      console.log(`   Error: ${verification.error}`);
    }
    
    console.log('\n🎉 Examples completed successfully!');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    if (error.code) {
      console.error('   Code:', error.code);
    }
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  main()
    .then(() => process.exit(0))
    .catch((error) => {
      console.error(error);
      process.exit(1);
    });
}

module.exports = { main };
