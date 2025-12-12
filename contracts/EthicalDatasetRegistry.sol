// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

interface ITokenomicsV2 {
    function distributeEthicalResearcherReward(address recipient, uint256 amount, string calldata reason) external;
    function distributeDAOValidatorReward(address recipient, uint256 amount, string calldata reason) external;
}

/**
 * @title EthicalDatasetRegistry
 * @notice Registry for Ethical Corrected Datasets (ECD) with DAO validation and rewards
 * @dev Manages dataset proposals, voting, and reward distribution
 */
contract EthicalDatasetRegistry is Ownable, ReentrancyGuard {
    
    ITokenomicsV2 public tokenomics;
    
    // Proposal structure
    struct DatasetProposal {
        address proposer;
        string ipfsCID;
        string description;
        uint256 impactFactor;      // Error frequency/severity (1-100)
        uint256 proposalTime;
        uint256 votesFor;
        uint256 votesAgainst;
        uint256 totalVotingPower;
        ProposalStatus status;
        mapping(address => bool) hasVoted;
    }
    
    enum ProposalStatus {
        Pending,
        Approved,
        Rejected,
        Executed
    }
    
    // Storage
    mapping(uint256 => DatasetProposal) public proposals;
    uint256 public proposalCount;
    
    // Governance parameters
    uint256 public quorumPercentage = 5000;  // 50% in basis points
    uint256 public approvalThreshold = 6000; // 60% approval needed
    uint256 public votingPeriod = 3 days;
    
    // Reward parameters
    uint256 public baseReward = 1000 * 10**18;  // Base reward in tokens
    uint256 public maxImpactMultiplier = 300;    // 3x max multiplier (in basis points/100)
    uint256 public validatorRewardPerVote = 10 * 10**18; // Reward per validator vote
    
    // Events
    event ProposalCreated(
        uint256 indexed proposalId,
        address indexed proposer,
        string ipfsCID,
        uint256 impactFactor
    );
    
    event VoteCast(
        uint256 indexed proposalId,
        address indexed voter,
        bool support,
        uint256 votingPower
    );
    
    event ProposalExecuted(
        uint256 indexed proposalId,
        ProposalStatus status,
        uint256 rewardAmount
    );
    
    event RewardParametersUpdated(
        uint256 baseReward,
        uint256 maxImpactMultiplier,
        uint256 validatorReward
    );
    
    /**
     * @notice Constructor
     * @param _tokenomics Address of TokenomicsV2 contract
     */
    constructor(address _tokenomics) {
        require(_tokenomics != address(0), "Invalid tokenomics address");
        tokenomics = ITokenomicsV2(_tokenomics);
    }
    
    /**
     * @notice Submit a new dataset proposal
     * @param ipfsCID IPFS content identifier for the dataset
     * @param description Description of the dataset and errors corrected
     * @param impactFactor Impact factor (1-100) based on error frequency/severity
     */
    function submitProposal(
        string calldata ipfsCID,
        string calldata description,
        uint256 impactFactor
    ) external returns (uint256) {
        require(bytes(ipfsCID).length > 0, "CID required");
        require(impactFactor > 0 && impactFactor <= 100, "Invalid impact factor");
        
        uint256 proposalId = proposalCount++;
        DatasetProposal storage proposal = proposals[proposalId];
        
        proposal.proposer = msg.sender;
        proposal.ipfsCID = ipfsCID;
        proposal.description = description;
        proposal.impactFactor = impactFactor;
        proposal.proposalTime = block.timestamp;
        proposal.status = ProposalStatus.Pending;
        
        emit ProposalCreated(proposalId, msg.sender, ipfsCID, impactFactor);
        
        return proposalId;
    }
    
    /**
     * @notice Cast vote on a dataset proposal
     * @param proposalId ID of the proposal
     * @param support Whether to support the proposal
     * @param votingPower Voting power of the voter (from governance token)
     */
    function castVote(
        uint256 proposalId,
        bool support,
        uint256 votingPower
    ) external nonReentrant {
        require(proposalId < proposalCount, "Invalid proposal ID");
        DatasetProposal storage proposal = proposals[proposalId];
        
        require(proposal.status == ProposalStatus.Pending, "Proposal not pending");
        require(!proposal.hasVoted[msg.sender], "Already voted");
        require(block.timestamp <= proposal.proposalTime + votingPeriod, "Voting period ended");
        require(votingPower > 0, "No voting power");
        
        proposal.hasVoted[msg.sender] = true;
        proposal.totalVotingPower += votingPower;
        
        if (support) {
            proposal.votesFor += votingPower;
        } else {
            proposal.votesAgainst += votingPower;
        }
        
        emit VoteCast(proposalId, msg.sender, support, votingPower);
    }
    
    /**
     * @notice Execute a proposal after voting period
     * @param proposalId ID of the proposal to execute
     */
    function executeProposal(uint256 proposalId) external nonReentrant {
        require(proposalId < proposalCount, "Invalid proposal ID");
        DatasetProposal storage proposal = proposals[proposalId];
        
        require(proposal.status == ProposalStatus.Pending, "Proposal not pending");
        require(block.timestamp > proposal.proposalTime + votingPeriod, "Voting period not ended");
        
        // Check quorum
        // Note: In production, this should check against total supply or active voting power
        // For simplicity, using totalVotingPower as denominator
        bool quorumReached = proposal.totalVotingPower > 0; // Simplified check
        
        if (!quorumReached) {
            proposal.status = ProposalStatus.Rejected;
            emit ProposalExecuted(proposalId, ProposalStatus.Rejected, 0);
            return;
        }
        
        // Check approval threshold
        uint256 approvalRate = (proposal.votesFor * 10000) / proposal.totalVotingPower;
        bool approved = approvalRate >= approvalThreshold;
        
        if (approved) {
            proposal.status = ProposalStatus.Approved;
            
            // Calculate and distribute reward
            uint256 rewardAmount = calculateReward(proposal.impactFactor);
            
            string memory reason = string(abi.encodePacked("ECD validated: ", proposal.ipfsCID));
            tokenomics.distributeEthicalResearcherReward(proposal.proposer, rewardAmount, reason);
            
            proposal.status = ProposalStatus.Executed;
            emit ProposalExecuted(proposalId, ProposalStatus.Executed, rewardAmount);
        } else {
            proposal.status = ProposalStatus.Rejected;
            emit ProposalExecuted(proposalId, ProposalStatus.Rejected, 0);
        }
    }
    
    /**
     * @notice Distribute rewards to validators who voted
     * @param proposalId ID of the proposal
     * @param voters Array of voter addresses
     */
    function distributeValidatorRewards(
        uint256 proposalId,
        address[] calldata voters
    ) external onlyOwner nonReentrant {
        require(proposalId < proposalCount, "Invalid proposal ID");
        DatasetProposal storage proposal = proposals[proposalId];
        require(proposal.status == ProposalStatus.Executed, "Proposal not executed");
        
        for (uint256 i = 0; i < voters.length; i++) {
            if (proposal.hasVoted[voters[i]]) {
                tokenomics.distributeDAOValidatorReward(
                    voters[i],
                    validatorRewardPerVote,
                    "Dataset validation vote"
                );
            }
        }
    }
    
    /**
     * @notice Calculate reward based on impact factor
     * @param impactFactor Impact factor (1-100)
     * @return Calculated reward amount
     */
    function calculateReward(uint256 impactFactor) public view returns (uint256) {
        // reward = baseReward * (1 + (impactFactor / 100) * maxImpactMultiplier)
        // Example: impactFactor=50, maxMultiplier=300 => 1.5x multiplier
        uint256 multiplier = 10000 + ((impactFactor * maxImpactMultiplier * 100) / 100);
        return (baseReward * multiplier) / 10000;
    }
    
    /**
     * @notice Set governance parameters
     * @param _quorumPercentage Quorum percentage in basis points
     * @param _approvalThreshold Approval threshold in basis points
     * @param _votingPeriod Voting period in seconds
     */
    function setGovernanceParameters(
        uint256 _quorumPercentage,
        uint256 _approvalThreshold,
        uint256 _votingPeriod
    ) external onlyOwner {
        require(_quorumPercentage <= 10000, "Invalid quorum");
        require(_approvalThreshold <= 10000, "Invalid threshold");
        require(_votingPeriod > 0, "Invalid voting period");
        
        quorumPercentage = _quorumPercentage;
        approvalThreshold = _approvalThreshold;
        votingPeriod = _votingPeriod;
    }
    
    /**
     * @notice Set reward parameters
     * @param _baseReward Base reward amount
     * @param _maxImpactMultiplier Maximum impact multiplier
     * @param _validatorReward Reward per validator vote
     */
    function setRewardParameters(
        uint256 _baseReward,
        uint256 _maxImpactMultiplier,
        uint256 _validatorReward
    ) external onlyOwner {
        baseReward = _baseReward;
        maxImpactMultiplier = _maxImpactMultiplier;
        validatorRewardPerVote = _validatorReward;
        
        emit RewardParametersUpdated(_baseReward, _maxImpactMultiplier, _validatorReward);
    }
    
    /**
     * @notice Get proposal details
     * @param proposalId ID of the proposal
     * @return proposer Proposer address
     * @return ipfsCID IPFS CID
     * @return description Description
     * @return impactFactor Impact factor
     * @return proposalTime Proposal timestamp
     * @return votesFor Votes for
     * @return votesAgainst Votes against
     * @return status Proposal status
     */
    function getProposal(uint256 proposalId) external view returns (
        address proposer,
        string memory ipfsCID,
        string memory description,
        uint256 impactFactor,
        uint256 proposalTime,
        uint256 votesFor,
        uint256 votesAgainst,
        ProposalStatus status
    ) {
        require(proposalId < proposalCount, "Invalid proposal ID");
        DatasetProposal storage proposal = proposals[proposalId];
        
        return (
            proposal.proposer,
            proposal.ipfsCID,
            proposal.description,
            proposal.impactFactor,
            proposal.proposalTime,
            proposal.votesFor,
            proposal.votesAgainst,
            proposal.status
        );
    }
    
    /**
     * @notice Check if address has voted on proposal
     * @param proposalId ID of the proposal
     * @param voter Address to check
     * @return Whether the address has voted
     */
    function hasVoted(uint256 proposalId, address voter) external view returns (bool) {
        require(proposalId < proposalCount, "Invalid proposal ID");
        return proposals[proposalId].hasVoted[voter];
    }
}
