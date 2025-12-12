// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title HelmiGovernance
 * @dev Enhanced governance contract implementing Sensisara Principle
 * Features: Quorum, Cooldown, Rate Limiting, On-Chain Transparency
 */
contract HelmiGovernance is ERC20, Ownable {
    // Governance parameters following Sensisara Principle
    uint256 public constant PROPOSAL_COOLDOWN = 3 days; // Circadian rhythm pattern
    uint256 public constant VOTING_PERIOD = 7 days; // Week-long deliberation
    uint256 public constant QUORUM_PERCENTAGE = 30; // 30% participation required
    uint256 public constant RATE_LIMIT_WINDOW = 1 days; // Proposals per day
    uint256 public constant MAX_PROPOSALS_PER_WINDOW = 3; // Natural constraint
    
    struct Proposal {
        uint256 id;
        address proposer;
        string ipfsCid; // IPFS CID for proposal documentation
        string title;
        uint256 votesFor;
        uint256 votesAgainst;
        uint256 startTime;
        uint256 endTime;
        bool executed;
        bool cancelled;
        mapping(address => bool) hasVoted;
    }
    
    // Contribution scoring for voting power
    mapping(address => uint256) public contributionScore;
    
    // Proposal management
    mapping(uint256 => Proposal) public proposals;
    uint256 public proposalCount;
    uint256 public lastProposalTime;
    
    // Rate limiting tracking
    mapping(uint256 => uint256) public proposalsInWindow; // timestamp => count
    mapping(address => uint256) public userLastProposal; // user => timestamp
    
    // Events for transparency
    event ProposalCreated(
        uint256 indexed proposalId,
        address indexed proposer,
        string ipfsCid,
        string title,
        uint256 startTime,
        uint256 endTime
    );
    
    event VoteCast(
        uint256 indexed proposalId,
        address indexed voter,
        bool support,
        uint256 votingPower
    );
    
    event ProposalExecuted(uint256 indexed proposalId);
    event ProposalCancelled(uint256 indexed proposalId);
    event ContributionScoreUpdated(address indexed user, uint256 newScore);
    
    constructor() ERC20("Helmi Governance Token", "HELMI") Ownable(msg.sender) {}
    
    /**
     * @dev Mint governance tokens (owner only)
     */
    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }
    
    /**
     * @dev Set contribution score for enhanced voting power
     */
    function setContributionScore(address user, uint256 score) external onlyOwner {
        contributionScore[user] = score;
        emit ContributionScoreUpdated(user, score);
    }
    
    /**
     * @dev Calculate voting power based on Sensisara Principle
     * Combines token balance with contribution score
     */
    function votingPower(address user) public view returns (uint256) {
        return balanceOf(user) * (contributionScore[user] + 1);
    }
    
    /**
     * @dev Create a new proposal with rate limiting and cooldown
     * @param ipfsCid IPFS CID containing full proposal documentation
     * @param title Short title for the proposal
     */
    function createProposal(string memory ipfsCid, string memory title) external returns (uint256) {
        require(balanceOf(msg.sender) > 0, "Must hold tokens to propose");
        require(bytes(ipfsCid).length > 0, "IPFS CID required for verifiability");
        require(bytes(title).length > 0, "Title required");
        
        // Check cooldown period (circadian rhythm pattern)
        require(
            block.timestamp >= lastProposalTime + PROPOSAL_COOLDOWN,
            "Cooldown period active - system needs rest"
        );
        
        // Check rate limiting (refractory period)
        // Calculate the start of the current time window using integer division
        // e.g., if current time is 150,000 and window is 86,400 (1 day),
        // windowStart = (150,000 / 86,400) * 86,400 = 1 * 86,400 = 86,400
        uint256 windowStart = (block.timestamp / RATE_LIMIT_WINDOW) * RATE_LIMIT_WINDOW;
        require(
            proposalsInWindow[windowStart] < MAX_PROPOSALS_PER_WINDOW,
            "Rate limit exceeded - too many proposals in this period"
        );
        
        // Check user-specific cooldown
        require(
            block.timestamp >= userLastProposal[msg.sender] + PROPOSAL_COOLDOWN,
            "User cooldown active"
        );
        
        proposalCount++;
        uint256 proposalId = proposalCount;
        
        Proposal storage newProposal = proposals[proposalId];
        newProposal.id = proposalId;
        newProposal.proposer = msg.sender;
        newProposal.ipfsCid = ipfsCid;
        newProposal.title = title;
        newProposal.startTime = block.timestamp;
        newProposal.endTime = block.timestamp + VOTING_PERIOD;
        newProposal.executed = false;
        newProposal.cancelled = false;
        
        lastProposalTime = block.timestamp;
        proposalsInWindow[windowStart]++;
        userLastProposal[msg.sender] = block.timestamp;
        
        emit ProposalCreated(
            proposalId,
            msg.sender,
            ipfsCid,
            title,
            newProposal.startTime,
            newProposal.endTime
        );
        
        return proposalId;
    }
    
    /**
     * @dev Vote on a proposal with transparent tracking
     * @param proposalId ID of the proposal
     * @param support true for yes, false for no
     */
    function vote(uint256 proposalId, bool support) external {
        Proposal storage proposal = proposals[proposalId];
        
        require(proposal.id > 0, "Proposal does not exist");
        require(block.timestamp >= proposal.startTime, "Voting not started");
        require(block.timestamp <= proposal.endTime, "Voting ended");
        require(!proposal.executed, "Proposal already executed");
        require(!proposal.cancelled, "Proposal cancelled");
        require(!proposal.hasVoted[msg.sender], "Already voted");
        require(balanceOf(msg.sender) > 0, "No voting power");
        
        uint256 power = votingPower(msg.sender);
        
        if (support) {
            proposal.votesFor += power;
        } else {
            proposal.votesAgainst += power;
        }
        
        proposal.hasVoted[msg.sender] = true;
        
        emit VoteCast(proposalId, msg.sender, support, power);
    }
    
    /**
     * @dev Check if proposal has reached quorum (Sensisara threshold)
     */
    function hasQuorum(uint256 proposalId) public view returns (bool) {
        Proposal storage proposal = proposals[proposalId];
        uint256 totalVotes = proposal.votesFor + proposal.votesAgainst;
        uint256 totalPower = totalSupply();
        
        return (totalVotes * 100) >= (totalPower * QUORUM_PERCENTAGE);
    }
    
    /**
     * @dev Check if proposal has passed
     */
    function isPassed(uint256 proposalId) public view returns (bool) {
        Proposal storage proposal = proposals[proposalId];
        return proposal.votesFor > proposal.votesAgainst;
    }
    
    /**
     * @dev Execute a passed proposal (simplified - extend for actual execution)
     */
    function executeProposal(uint256 proposalId) external {
        Proposal storage proposal = proposals[proposalId];
        
        require(proposal.id > 0, "Proposal does not exist");
        require(block.timestamp > proposal.endTime, "Voting period not ended");
        require(!proposal.executed, "Already executed");
        require(!proposal.cancelled, "Proposal cancelled");
        require(hasQuorum(proposalId), "Quorum not reached");
        require(isPassed(proposalId), "Proposal not passed");
        
        proposal.executed = true;
        
        emit ProposalExecuted(proposalId);
        
        // Actual execution logic would go here
        // For now, this is a transparent record that proposal passed
    }
    
    /**
     * @dev Cancel a proposal (owner only, for emergencies)
     */
    function cancelProposal(uint256 proposalId) external onlyOwner {
        Proposal storage proposal = proposals[proposalId];
        
        require(proposal.id > 0, "Proposal does not exist");
        require(!proposal.executed, "Already executed");
        require(!proposal.cancelled, "Already cancelled");
        
        proposal.cancelled = true;
        
        emit ProposalCancelled(proposalId);
    }
    
    /**
     * @dev Get proposal details
     */
    function getProposal(uint256 proposalId) external view returns (
        address proposer,
        string memory ipfsCid,
        string memory title,
        uint256 votesFor,
        uint256 votesAgainst,
        uint256 startTime,
        uint256 endTime,
        bool executed,
        bool cancelled
    ) {
        Proposal storage proposal = proposals[proposalId];
        return (
            proposal.proposer,
            proposal.ipfsCid,
            proposal.title,
            proposal.votesFor,
            proposal.votesAgainst,
            proposal.startTime,
            proposal.endTime,
            proposal.executed,
            proposal.cancelled
        );
    }
    
    /**
     * @dev Check if user has voted on a proposal
     */
    function hasVoted(uint256 proposalId, address user) external view returns (bool) {
        return proposals[proposalId].hasVoted[user];
    }
}
