// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title EUSDaoGovernance
 * @notice Euystacio DAO Governance with Red Code Veto and Quorum Rules
 * @dev Implements H-Var aligned governance with immutable quorum requirements
 */
contract EUSDaoGovernance is ERC20, Ownable {
    // Contribution scores for weighted voting
    mapping(address => uint256) public contributionScore;
    
    // Governance parameters (immutable after initialization)
    uint256 public quorumPercentage = 51; // 51% quorum required (H-Var aligned)
    uint256 public proposalThreshold = 1000 * 10**18; // Minimum tokens to create proposal
    uint256 public votingPeriod = 7 days; // Standard voting period
    
    // Proposal tracking
    struct Proposal {
        uint256 id;
        address proposer;
        string description;
        uint256 forVotes;
        uint256 againstVotes;
        uint256 startTime;
        uint256 endTime;
        bool executed;
        bool vetoed;
        mapping(address => bool) hasVoted;
    }
    
    mapping(uint256 => Proposal) public proposals;
    uint256 public proposalCount;
    
    // Red Code Veto authority
    address public vetoAuthority;
    
    // Events
    event ProposalCreated(uint256 indexed proposalId, address indexed proposer, string description);
    event VoteCast(uint256 indexed proposalId, address indexed voter, bool support, uint256 weight);
    event ProposalExecuted(uint256 indexed proposalId);
    event ProposalVetoed(uint256 indexed proposalId, address indexed vetoAuthority);
    event QuorumUpdated(uint256 newQuorumPercentage);
    event VetoAuthorityUpdated(address indexed newAuthority);

    constructor() ERC20("Euystacio Stewardship", "EUS") {
        vetoAuthority = msg.sender; // Initial veto authority is deployer
    }

    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }

    function setContributionScore(address user, uint256 score) external onlyOwner {
        contributionScore[user] = score;
    }

    function votingPower(address user) public view returns (uint256) {
        // voting power = balance * (1 + contributionScore)
        return balanceOf(user) * (contributionScore[user] + 1);
    }
    
    /**
     * @notice Create a new governance proposal
     * @param description Description of the proposal
     */
    function createProposal(string memory description) external returns (uint256) {
        require(balanceOf(msg.sender) >= proposalThreshold, "Insufficient tokens for proposal");
        
        uint256 proposalId = proposalCount++;
        Proposal storage proposal = proposals[proposalId];
        proposal.id = proposalId;
        proposal.proposer = msg.sender;
        proposal.description = description;
        proposal.startTime = block.timestamp;
        proposal.endTime = block.timestamp + votingPeriod;
        proposal.executed = false;
        proposal.vetoed = false;
        
        emit ProposalCreated(proposalId, msg.sender, description);
        return proposalId;
    }
    
    /**
     * @notice Vote on a proposal
     * @param proposalId The ID of the proposal
     * @param support True for yes, false for no
     */
    function vote(uint256 proposalId, bool support) external {
        Proposal storage proposal = proposals[proposalId];
        require(block.timestamp >= proposal.startTime, "Voting not started");
        require(block.timestamp <= proposal.endTime, "Voting ended");
        require(!proposal.hasVoted[msg.sender], "Already voted");
        require(!proposal.vetoed, "Proposal vetoed");
        
        uint256 weight = votingPower(msg.sender);
        require(weight > 0, "No voting power");
        
        proposal.hasVoted[msg.sender] = true;
        
        if (support) {
            proposal.forVotes += weight;
        } else {
            proposal.againstVotes += weight;
        }
        
        emit VoteCast(proposalId, msg.sender, support, weight);
    }
    
    /**
     * @notice Check if quorum is reached for a proposal
     * @param proposalId The ID of the proposal
     */
    function quorumReached(uint256 proposalId) public view returns (bool) {
        Proposal storage proposal = proposals[proposalId];
        uint256 totalVotes = proposal.forVotes + proposal.againstVotes;
        uint256 totalSupply = totalSupply();
        
        if (totalSupply == 0) return false;
        
        // Quorum calculation: (totalVotes * 100) / totalSupply >= quorumPercentage
        return (totalVotes * 100) >= (totalSupply * quorumPercentage);
    }
    
    /**
     * @notice Check if a proposal passed
     * @param proposalId The ID of the proposal
     */
    function proposalPassed(uint256 proposalId) public view returns (bool) {
        Proposal storage proposal = proposals[proposalId];
        return quorumReached(proposalId) && proposal.forVotes > proposal.againstVotes;
    }
    
    /**
     * @notice Execute a passed proposal
     * @param proposalId The ID of the proposal
     */
    function executeProposal(uint256 proposalId) external {
        Proposal storage proposal = proposals[proposalId];
        require(block.timestamp > proposal.endTime, "Voting period not ended");
        require(!proposal.executed, "Already executed");
        require(!proposal.vetoed, "Proposal vetoed");
        require(proposalPassed(proposalId), "Proposal did not pass");
        
        proposal.executed = true;
        emit ProposalExecuted(proposalId);
    }
    
    /**
     * @notice Red Code Veto - Authority can veto any proposal
     * @param proposalId The ID of the proposal to veto
     */
    function vetoProposal(uint256 proposalId) external {
        require(msg.sender == vetoAuthority, "Only veto authority can veto");
        Proposal storage proposal = proposals[proposalId];
        require(!proposal.executed, "Already executed");
        
        proposal.vetoed = true;
        emit ProposalVetoed(proposalId, msg.sender);
    }
    
    /**
     * @notice Update quorum percentage (owner only, for governance evolution)
     * @param newQuorumPercentage New quorum percentage (1-100)
     */
    function updateQuorumPercentage(uint256 newQuorumPercentage) external onlyOwner {
        require(newQuorumPercentage > 0 && newQuorumPercentage <= 100, "Invalid quorum percentage");
        quorumPercentage = newQuorumPercentage;
        emit QuorumUpdated(newQuorumPercentage);
    }
    
    /**
     * @notice Update veto authority (owner only, for Red Code compliance)
     * @param newAuthority New veto authority address
     */
    function updateVetoAuthority(address newAuthority) external onlyOwner {
        require(newAuthority != address(0), "Invalid authority address");
        vetoAuthority = newAuthority;
        emit VetoAuthorityUpdated(newAuthority);
    }
    
    /**
     * @notice Get proposal details
     * @param proposalId The ID of the proposal
     */
    function getProposal(uint256 proposalId) external view returns (
        uint256 id,
        address proposer,
        string memory description,
        uint256 forVotes,
        uint256 againstVotes,
        uint256 startTime,
        uint256 endTime,
        bool executed,
        bool vetoed
    ) {
        Proposal storage proposal = proposals[proposalId];
        return (
            proposal.id,
            proposal.proposer,
            proposal.description,
            proposal.forVotes,
            proposal.againstVotes,
            proposal.startTime,
            proposal.endTime,
            proposal.executed,
            proposal.vetoed
        );
    }
}