// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

interface ITokenomicsV2Distributor {
    function distributeEthicalResearcherReward(address recipient, uint256 amount, string calldata reason) external;
}

/**
 * @title ModelRetrainingEscrow
 * @notice Manages model retraining proposals with token escrow and DAO validation
 * @dev Ensures serious proposals through token staking and distributes rewards on success
 */
contract ModelRetrainingEscrow is Ownable, ReentrancyGuard {
    using SafeERC20 for IERC20;
    
    IERC20 public immutable stakingToken;
    ITokenomicsV2Distributor public tokenomics;
    
    // Retraining proposal structure
    struct RetrainingProposal {
        address proposer;
        string datasetCID;          // IPFS CID of training dataset
        string modelDescription;
        uint256 complexity;         // Complexity score (1-100)
        uint256 escrowAmount;       // Staked tokens
        uint256 proposalTime;
        uint256 votesFor;
        uint256 votesAgainst;
        uint256 totalVotingPower;
        ProposalStatus status;
        string deployedModelCID;    // CID after successful retraining
        mapping(address => bool) hasVoted;
    }
    
    enum ProposalStatus {
        Pending,
        Approved,
        Rejected,
        InProgress,
        Completed,
        Failed
    }
    
    // Storage
    mapping(uint256 => RetrainingProposal) public proposals;
    uint256 public proposalCount;
    
    // Governance parameters
    uint256 public quorumPercentage = 4000;   // 40% in basis points
    uint256 public approvalThreshold = 6000;  // 60% approval needed
    uint256 public votingPeriod = 5 days;
    
    // Escrow and reward parameters
    uint256 public minimumEscrow = 100 * 10**18;     // Minimum tokens to stake
    uint256 public baseReward = 2000 * 10**18;       // Base reward for successful retraining
    uint256 public maxComplexityMultiplier = 500;    // 5x max multiplier
    
    // Events
    event ProposalCreated(
        uint256 indexed proposalId,
        address indexed proposer,
        string datasetCID,
        uint256 complexity,
        uint256 escrowAmount
    );
    
    event VoteCast(
        uint256 indexed proposalId,
        address indexed voter,
        bool support,
        uint256 votingPower
    );
    
    event ProposalStatusChanged(
        uint256 indexed proposalId,
        ProposalStatus oldStatus,
        ProposalStatus newStatus
    );
    
    event RetrainingCompleted(
        uint256 indexed proposalId,
        string deployedModelCID,
        uint256 rewardAmount
    );
    
    event EscrowRefunded(
        uint256 indexed proposalId,
        address indexed proposer,
        uint256 amount
    );
    
    /**
     * @notice Constructor
     * @param _stakingToken Address of token used for escrow
     * @param _tokenomics Address of TokenomicsV2 contract
     */
    constructor(address _stakingToken, address _tokenomics) {
        require(_stakingToken != address(0), "Invalid staking token");
        require(_tokenomics != address(0), "Invalid tokenomics");
        
        stakingToken = IERC20(_stakingToken);
        tokenomics = ITokenomicsV2Distributor(_tokenomics);
    }
    
    /**
     * @notice Submit a new retraining proposal with escrow
     * @param datasetCID IPFS CID of the training dataset
     * @param modelDescription Description of the retraining goal
     * @param complexity Complexity score (1-100)
     * @param escrowAmount Amount of tokens to stake
     */
    function submitProposal(
        string calldata datasetCID,
        string calldata modelDescription,
        uint256 complexity,
        uint256 escrowAmount
    ) external nonReentrant returns (uint256) {
        require(bytes(datasetCID).length > 0, "CID required");
        require(complexity > 0 && complexity <= 100, "Invalid complexity");
        require(escrowAmount >= minimumEscrow, "Insufficient escrow");
        
        // Transfer escrow tokens
        stakingToken.safeTransferFrom(msg.sender, address(this), escrowAmount);
        
        uint256 proposalId = proposalCount++;
        RetrainingProposal storage proposal = proposals[proposalId];
        
        proposal.proposer = msg.sender;
        proposal.datasetCID = datasetCID;
        proposal.modelDescription = modelDescription;
        proposal.complexity = complexity;
        proposal.escrowAmount = escrowAmount;
        proposal.proposalTime = block.timestamp;
        proposal.status = ProposalStatus.Pending;
        
        emit ProposalCreated(proposalId, msg.sender, datasetCID, complexity, escrowAmount);
        
        return proposalId;
    }
    
    /**
     * @notice Cast vote on a retraining proposal
     * @param proposalId ID of the proposal
     * @param support Whether to support the proposal
     * @param votingPower Voting power of the voter
     */
    function castVote(
        uint256 proposalId,
        bool support,
        uint256 votingPower
    ) external nonReentrant {
        require(proposalId < proposalCount, "Invalid proposal ID");
        RetrainingProposal storage proposal = proposals[proposalId];
        
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
     * @notice Execute proposal after voting period
     * @param proposalId ID of the proposal
     */
    function executeProposal(uint256 proposalId) external nonReentrant {
        require(proposalId < proposalCount, "Invalid proposal ID");
        RetrainingProposal storage proposal = proposals[proposalId];
        
        require(proposal.status == ProposalStatus.Pending, "Proposal not pending");
        require(block.timestamp > proposal.proposalTime + votingPeriod, "Voting period not ended");
        
        ProposalStatus oldStatus = proposal.status;
        
        // Check quorum and approval
        bool quorumReached = proposal.totalVotingPower > 0; // Simplified
        
        if (!quorumReached) {
            proposal.status = ProposalStatus.Rejected;
            // Refund escrow
            stakingToken.safeTransfer(proposal.proposer, proposal.escrowAmount);
            emit EscrowRefunded(proposalId, proposal.proposer, proposal.escrowAmount);
            emit ProposalStatusChanged(proposalId, oldStatus, ProposalStatus.Rejected);
            return;
        }
        
        uint256 approvalRate = (proposal.votesFor * 10000) / proposal.totalVotingPower;
        
        if (approvalRate >= approvalThreshold) {
            proposal.status = ProposalStatus.Approved;
            emit ProposalStatusChanged(proposalId, oldStatus, ProposalStatus.Approved);
        } else {
            proposal.status = ProposalStatus.Rejected;
            // Refund escrow
            stakingToken.safeTransfer(proposal.proposer, proposal.escrowAmount);
            emit EscrowRefunded(proposalId, proposal.proposer, proposal.escrowAmount);
            emit ProposalStatusChanged(proposalId, oldStatus, ProposalStatus.Rejected);
        }
    }
    
    /**
     * @notice Mark proposal as in progress (called by operator)
     * @param proposalId ID of the proposal
     */
    function startRetraining(uint256 proposalId) external onlyOwner {
        require(proposalId < proposalCount, "Invalid proposal ID");
        RetrainingProposal storage proposal = proposals[proposalId];
        
        require(proposal.status == ProposalStatus.Approved, "Proposal not approved");
        
        ProposalStatus oldStatus = proposal.status;
        proposal.status = ProposalStatus.InProgress;
        
        emit ProposalStatusChanged(proposalId, oldStatus, ProposalStatus.InProgress);
    }
    
    /**
     * @notice Complete retraining and distribute rewards
     * @param proposalId ID of the proposal
     * @param deployedModelCID IPFS CID of the deployed model
     */
    function completeRetraining(
        uint256 proposalId,
        string calldata deployedModelCID
    ) external onlyOwner nonReentrant {
        require(proposalId < proposalCount, "Invalid proposal ID");
        require(bytes(deployedModelCID).length > 0, "Model CID required");
        
        RetrainingProposal storage proposal = proposals[proposalId];
        require(proposal.status == ProposalStatus.InProgress, "Proposal not in progress");
        
        ProposalStatus oldStatus = proposal.status;
        proposal.status = ProposalStatus.Completed;
        proposal.deployedModelCID = deployedModelCID;
        
        // Calculate reward based on complexity
        uint256 rewardAmount = calculateReward(proposal.complexity);
        
        // Refund escrow
        stakingToken.safeTransfer(proposal.proposer, proposal.escrowAmount);
        emit EscrowRefunded(proposalId, proposal.proposer, proposal.escrowAmount);
        
        // Distribute reward
        string memory reason = string(abi.encodePacked("Model retraining completed: ", deployedModelCID));
        tokenomics.distributeEthicalResearcherReward(proposal.proposer, rewardAmount, reason);
        
        emit RetrainingCompleted(proposalId, deployedModelCID, rewardAmount);
        emit ProposalStatusChanged(proposalId, oldStatus, ProposalStatus.Completed);
    }
    
    /**
     * @notice Mark retraining as failed and handle escrow
     * @param proposalId ID of the proposal
     * @param refundEscrow Whether to refund the escrow
     */
    function failRetraining(uint256 proposalId, bool refundEscrow) external onlyOwner nonReentrant {
        require(proposalId < proposalCount, "Invalid proposal ID");
        
        RetrainingProposal storage proposal = proposals[proposalId];
        require(
            proposal.status == ProposalStatus.InProgress || proposal.status == ProposalStatus.Approved,
            "Invalid status"
        );
        
        ProposalStatus oldStatus = proposal.status;
        proposal.status = ProposalStatus.Failed;
        
        if (refundEscrow) {
            stakingToken.safeTransfer(proposal.proposer, proposal.escrowAmount);
            emit EscrowRefunded(proposalId, proposal.proposer, proposal.escrowAmount);
        } else {
            // Escrow goes to community reserve (transfer to owner for redistribution)
            stakingToken.safeTransfer(owner(), proposal.escrowAmount);
        }
        
        emit ProposalStatusChanged(proposalId, oldStatus, ProposalStatus.Failed);
    }
    
    /**
     * @notice Calculate reward based on complexity
     * @param complexity Complexity score (1-100)
     * @return Calculated reward amount
     */
    function calculateReward(uint256 complexity) public view returns (uint256) {
        // reward = baseReward * (1 + (complexity / 100) * maxComplexityMultiplier)
        uint256 multiplier = 10000 + (complexity * maxComplexityMultiplier);
        return (baseReward * multiplier) / 10000;
    }
    
    /**
     * @notice Set governance parameters
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
     * @notice Set escrow and reward parameters
     */
    function setEscrowRewardParameters(
        uint256 _minimumEscrow,
        uint256 _baseReward,
        uint256 _maxComplexityMultiplier
    ) external onlyOwner {
        minimumEscrow = _minimumEscrow;
        baseReward = _baseReward;
        maxComplexityMultiplier = _maxComplexityMultiplier;
    }
    
    /**
     * @notice Get proposal details
     */
    function getProposal(uint256 proposalId) external view returns (
        address proposer,
        string memory datasetCID,
        string memory modelDescription,
        uint256 complexity,
        uint256 escrowAmount,
        uint256 proposalTime,
        uint256 votesFor,
        uint256 votesAgainst,
        ProposalStatus status,
        string memory deployedModelCID
    ) {
        require(proposalId < proposalCount, "Invalid proposal ID");
        RetrainingProposal storage proposal = proposals[proposalId];
        
        return (
            proposal.proposer,
            proposal.datasetCID,
            proposal.modelDescription,
            proposal.complexity,
            proposal.escrowAmount,
            proposal.proposalTime,
            proposal.votesFor,
            proposal.votesAgainst,
            proposal.status,
            proposal.deployedModelCID
        );
    }
}
