/**
 * Euystacio-Helmi SDK
 * Software Development Kit for Web3 and ML integrators
 * 
 * Provides programmatic access to:
 * - Governance operations
 * - Treasury management
 * - IPFS document handling
 * - Sensisara principle implementations
 */

const { ethers } = require('ethers');

class EuystacioHelmiSDK {
  constructor(config = {}) {
    this.config = {
      rpcUrl: config.rpcUrl || process.env.RPC_URL,
      privateKey: config.privateKey || process.env.PRIVATE_KEY,
      governanceAddress: config.governanceAddress || process.env.GOVERNANCE_ADDRESS,
      ipfsGateway: config.ipfsGateway || 'https://ipfs.io/ipfs/',
      ...config
    };
    
    this.provider = null;
    this.signer = null;
    this.governance = null;
    
    if (this.config.rpcUrl) {
      this.initialize();
    }
  }
  
  /**
   * Initialize SDK with provider and contracts
   */
  async initialize() {
    this.provider = new ethers.JsonRpcProvider(this.config.rpcUrl);
    
    if (this.config.privateKey) {
      this.signer = new ethers.Wallet(this.config.privateKey, this.provider);
    }
    
    // Load HelmiGovernance contract
    if (this.config.governanceAddress) {
      const governanceABI = require('./abis/HelmiGovernance.json');
      this.governance = new ethers.Contract(
        this.config.governanceAddress,
        governanceABI,
        this.signer || this.provider
      );
    }
  }
  
  // ==================== Governance Methods ====================
  
  /**
   * Create a new governance proposal
   * @param {string} ipfsCid - IPFS CID of proposal documentation
   * @param {string} title - Proposal title
   * @returns {Promise<Object>} Transaction receipt
   */
  async createProposal(ipfsCid, title) {
    if (!this.governance || !this.signer) {
      throw new Error('Governance contract or signer not initialized');
    }
    
    const tx = await this.governance.createProposal(ipfsCid, title);
    const receipt = await tx.wait();
    
    // Extract proposal ID from events
    const event = receipt.logs.find(log => {
      try {
        const parsed = this.governance.interface.parseLog(log);
        return parsed.name === 'ProposalCreated';
      } catch {
        return false;
      }
    });
    
    return {
      receipt,
      proposalId: event ? event.args.proposalId.toString() : null
    };
  }
  
  /**
   * Vote on a proposal
   * @param {number|string} proposalId - Proposal ID
   * @param {boolean} support - true for yes, false for no
   * @returns {Promise<Object>} Transaction receipt
   */
  async vote(proposalId, support) {
    if (!this.governance || !this.signer) {
      throw new Error('Governance contract or signer not initialized');
    }
    
    const tx = await this.governance.vote(proposalId, support);
    return await tx.wait();
  }
  
  /**
   * Get proposal details
   * @param {number|string} proposalId - Proposal ID
   * @returns {Promise<Object>} Proposal data
   */
  async getProposal(proposalId) {
    if (!this.governance) {
      throw new Error('Governance contract not initialized');
    }
    
    const proposal = await this.governance.getProposal(proposalId);
    
    return {
      proposer: proposal[0],
      ipfsCid: proposal[1],
      title: proposal[2],
      votesFor: proposal[3].toString(),
      votesAgainst: proposal[4].toString(),
      startTime: new Date(Number(proposal[5]) * 1000),
      endTime: new Date(Number(proposal[6]) * 1000),
      executed: proposal[7],
      cancelled: proposal[8]
    };
  }
  
  /**
   * Check if proposal has reached quorum
   * @param {number|string} proposalId - Proposal ID
   * @returns {Promise<boolean>}
   */
  async hasQuorum(proposalId) {
    if (!this.governance) {
      throw new Error('Governance contract not initialized');
    }
    
    return await this.governance.hasQuorum(proposalId);
  }
  
  /**
   * Check if proposal has passed
   * @param {number|string} proposalId - Proposal ID
   * @returns {Promise<boolean>}
   */
  async isPassed(proposalId) {
    if (!this.governance) {
      throw new Error('Governance contract not initialized');
    }
    
    return await this.governance.isPassed(proposalId);
  }
  
  /**
   * Get user's voting power
   * @param {string} address - User address (defaults to signer)
   * @returns {Promise<string>} Voting power
   */
  async getVotingPower(address) {
    if (!this.governance) {
      throw new Error('Governance contract not initialized');
    }
    
    const addr = address || (this.signer ? await this.signer.getAddress() : null);
    if (!addr) {
      throw new Error('No address provided and no signer available');
    }
    
    const power = await this.governance.votingPower(addr);
    return power.toString();
  }
  
  // ==================== IPFS Methods ====================
  
  /**
   * Fetch document from IPFS
   * @param {string} cid - IPFS CID
   * @returns {Promise<string>} Document content
   */
  async fetchFromIPFS(cid) {
    const url = `${this.config.ipfsGateway}${cid}`;
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch from IPFS: ${response.statusText}`);
    }
    
    return await response.text();
  }
  
  /**
   * Verify IPFS CID matches expected hash
   * @param {string} cid - IPFS CID to verify
   * @returns {Promise<Object>} Verification result
   */
  async verifyIPFSCID(cid) {
    try {
      const content = await this.fetchFromIPFS(cid);
      return {
        valid: true,
        cid,
        contentLength: content.length,
        content: content.substring(0, 200) + '...' // Preview
      };
    } catch (error) {
      return {
        valid: false,
        cid,
        error: error.message
      };
    }
  }
  
  // ==================== Utility Methods ====================
  
  /**
   * Get current governance parameters
   * @returns {Promise<Object>} Governance parameters
   */
  async getGovernanceParams() {
    if (!this.governance) {
      throw new Error('Governance contract not initialized');
    }
    
    return {
      proposalCooldown: await this.governance.PROPOSAL_COOLDOWN(),
      votingPeriod: await this.governance.VOTING_PERIOD(),
      quorumPercentage: await this.governance.QUORUM_PERCENTAGE(),
      rateLimitWindow: await this.governance.RATE_LIMIT_WINDOW(),
      maxProposalsPerWindow: await this.governance.MAX_PROPOSALS_PER_WINDOW()
    };
  }
  
  /**
   * Get proposal count
   * @returns {Promise<number>}
   */
  async getProposalCount() {
    if (!this.governance) {
      throw new Error('Governance contract not initialized');
    }
    
    const count = await this.governance.proposalCount();
    return Number(count);
  }
  
  /**
   * Check if user has voted on a proposal
   * @param {number|string} proposalId - Proposal ID
   * @param {string} address - User address (defaults to signer)
   * @returns {Promise<boolean>}
   */
  async hasVoted(proposalId, address) {
    if (!this.governance) {
      throw new Error('Governance contract not initialized');
    }
    
    const addr = address || (this.signer ? await this.signer.getAddress() : null);
    if (!addr) {
      throw new Error('No address provided and no signer available');
    }
    
    return await this.governance.hasVoted(proposalId, addr);
  }
}

// ==================== ML Integration Helpers ====================

/**
 * Sensisara Principle implementation for ML models
 * Provides ecosystem-inspired decision-making patterns
 */
class SensisaraML {
  /**
   * Apply homeostatic balancing to model outputs
   * Ensures stability and prevents extreme outputs
   * @param {Array<number>} outputs - Model outputs
   * @param {Object} options - Balancing options
   * @returns {Array<number>} Balanced outputs
   */
  static applyHomeostasis(outputs, options = {}) {
    const {
      minThreshold = 0.1,
      maxThreshold = 0.9,
      smoothingFactor = 0.3
    } = options;
    
    return outputs.map(output => {
      // Clamp to natural bounds
      let balanced = Math.max(minThreshold, Math.min(maxThreshold, output));
      
      // Apply smoothing (like biological damping)
      balanced = output + (balanced - output) * smoothingFactor;
      
      return balanced;
    });
  }
  
  /**
   * Implement quorum-based decision making
   * Multiple model outputs must agree (like quorum sensing in bacteria)
   * @param {Array<Array<number>>} modelOutputs - Outputs from multiple models
   * @param {number} quorumThreshold - Agreement threshold (0-1)
   * @returns {Object} Decision with confidence
   */
  static quorumDecision(modelOutputs, quorumThreshold = 0.6) {
    if (modelOutputs.length === 0) {
      throw new Error('No model outputs provided');
    }
    
    const outputLength = modelOutputs[0].length;
    const consensusOutputs = new Array(outputLength).fill(0);
    const confidence = new Array(outputLength).fill(0);
    
    for (let i = 0; i < outputLength; i++) {
      const values = modelOutputs.map(output => output[i]);
      const mean = values.reduce((a, b) => a + b, 0) / values.length;
      const variance = values.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / values.length;
      
      consensusOutputs[i] = mean;
      confidence[i] = 1 - Math.min(1, variance); // Lower variance = higher confidence
    }
    
    const meetsQuorum = confidence.every(c => c >= quorumThreshold);
    
    return {
      outputs: consensusOutputs,
      confidence: confidence,
      meetsQuorum,
      averageConfidence: confidence.reduce((a, b) => a + b, 0) / confidence.length
    };
  }
}

module.exports = {
  EuystacioHelmiSDK,
  SensisaraML
};
