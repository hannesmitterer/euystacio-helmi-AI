// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

interface ITokenomicsV2Operator {
    function distributeOperatorReward(address recipient, uint256 amount, string calldata reason) external;
}

/**
 * @title KSyncOracle
 * @notice Oracle and automation contract for K-Sync daemon operators
 * @dev Manages operator registration, staking, and rewards for model retraining execution
 */
contract KSyncOracle is Ownable, ReentrancyGuard {
    using SafeERC20 for IERC20;
    
    IERC20 public immutable stakingToken;
    ITokenomicsV2Operator public tokenomics;
    
    // Operator structure
    struct Operator {
        bool isActive;
        uint256 stakedAmount;
        uint256 registrationTime;
        uint256 totalExecutions;
        uint256 successfulExecutions;
        uint256 totalRewardsEarned;
        string endpoint;            // API endpoint for K-Sync daemon
    }
    
    // Retraining execution structure
    struct RetrainingExecution {
        address operator;
        string datasetCID;          // IPFS CID of dataset
        string oldModelCID;         // Previous model CID
        string newModelCID;         // Updated model CID after retraining
        uint256 executionTime;
        uint256 gasUsed;
        ExecutionStatus status;
        uint256 rewardAmount;
    }
    
    enum ExecutionStatus {
        Pending,
        InProgress,
        Completed,
        Failed
    }
    
    // Storage
    mapping(address => Operator) public operators;
    mapping(uint256 => RetrainingExecution) public executions;
    address[] public operatorList;
    uint256 public executionCount;
    
    // Staking and reward parameters
    uint256 public minimumStake = 500 * 10**18;              // Minimum stake to become operator
    uint256 public baseExecutionReward = 100 * 10**18;       // Base reward per execution
    uint256 public gasReimbursementRate = 150;               // 150% of gas cost (in basis points/100)
    uint256 public successBonusMultiplier = 200;             // 2x bonus for successful execution
    
    // Slashing parameters
    uint256 public failurePenalty = 10 * 10**18;             // Penalty for failed execution
    uint256 public maxConsecutiveFailures = 3;               // Max failures before deactivation
    
    // Events
    event OperatorRegistered(
        address indexed operator,
        uint256 stakedAmount,
        string endpoint
    );
    
    event OperatorStakeUpdated(
        address indexed operator,
        uint256 oldStake,
        uint256 newStake
    );
    
    event OperatorStatusChanged(
        address indexed operator,
        bool isActive
    );
    
    event ExecutionStarted(
        uint256 indexed executionId,
        address indexed operator,
        string datasetCID,
        string oldModelCID
    );
    
    event ExecutionCompleted(
        uint256 indexed executionId,
        address indexed operator,
        string newModelCID,
        uint256 rewardAmount
    );
    
    event ExecutionFailed(
        uint256 indexed executionId,
        address indexed operator,
        uint256 penaltyAmount
    );
    
    event OperatorSlashed(
        address indexed operator,
        uint256 amount,
        string reason
    );
    
    /**
     * @notice Constructor
     * @param _stakingToken Address of token used for staking
     * @param _tokenomics Address of TokenomicsV2 contract
     */
    constructor(address _stakingToken, address _tokenomics) {
        require(_stakingToken != address(0), "Invalid staking token");
        require(_tokenomics != address(0), "Invalid tokenomics");
        
        stakingToken = IERC20(_stakingToken);
        tokenomics = ITokenomicsV2Operator(_tokenomics);
    }
    
    /**
     * @notice Register as an operator with stake
     * @param stakeAmount Amount of tokens to stake
     * @param endpoint API endpoint for K-Sync daemon
     */
    function registerOperator(
        uint256 stakeAmount,
        string calldata endpoint
    ) external nonReentrant {
        require(operators[msg.sender].registrationTime == 0, "Already registered");
        require(stakeAmount >= minimumStake, "Insufficient stake");
        require(bytes(endpoint).length > 0, "Endpoint required");
        
        // Transfer stake
        stakingToken.safeTransferFrom(msg.sender, address(this), stakeAmount);
        
        operators[msg.sender] = Operator({
            isActive: true,
            stakedAmount: stakeAmount,
            registrationTime: block.timestamp,
            totalExecutions: 0,
            successfulExecutions: 0,
            totalRewardsEarned: 0,
            endpoint: endpoint
        });
        
        operatorList.push(msg.sender);
        
        emit OperatorRegistered(msg.sender, stakeAmount, endpoint);
    }
    
    /**
     * @notice Add more stake to operator account
     * @param additionalStake Amount of additional tokens to stake
     */
    function addStake(uint256 additionalStake) external nonReentrant {
        require(operators[msg.sender].registrationTime > 0, "Not registered");
        require(additionalStake > 0, "Invalid amount");
        
        stakingToken.safeTransferFrom(msg.sender, address(this), additionalStake);
        
        uint256 oldStake = operators[msg.sender].stakedAmount;
        operators[msg.sender].stakedAmount += additionalStake;
        
        emit OperatorStakeUpdated(msg.sender, oldStake, operators[msg.sender].stakedAmount);
    }
    
    /**
     * @notice Withdraw stake (only if not active)
     * @param amount Amount to withdraw
     */
    function withdrawStake(uint256 amount) external nonReentrant {
        require(operators[msg.sender].registrationTime > 0, "Not registered");
        require(!operators[msg.sender].isActive, "Must deactivate first");
        require(amount <= operators[msg.sender].stakedAmount, "Insufficient stake");
        
        uint256 oldStake = operators[msg.sender].stakedAmount;
        operators[msg.sender].stakedAmount -= amount;
        
        stakingToken.safeTransfer(msg.sender, amount);
        
        emit OperatorStakeUpdated(msg.sender, oldStake, operators[msg.sender].stakedAmount);
    }
    
    /**
     * @notice Start a retraining execution
     * @param operator Address of the operator executing
     * @param datasetCID IPFS CID of the dataset
     * @param oldModelCID Current model CID before retraining
     */
    function startExecution(
        address operator,
        string calldata datasetCID,
        string calldata oldModelCID
    ) external onlyOwner returns (uint256) {
        require(operators[operator].isActive, "Operator not active");
        require(bytes(datasetCID).length > 0, "Dataset CID required");
        require(bytes(oldModelCID).length > 0, "Model CID required");
        
        uint256 executionId = executionCount++;
        
        executions[executionId] = RetrainingExecution({
            operator: operator,
            datasetCID: datasetCID,
            oldModelCID: oldModelCID,
            newModelCID: "",
            executionTime: block.timestamp,
            gasUsed: 0,
            status: ExecutionStatus.InProgress,
            rewardAmount: 0
        });
        
        operators[operator].totalExecutions++;
        
        emit ExecutionStarted(executionId, operator, datasetCID, oldModelCID);
        
        return executionId;
    }
    
    /**
     * @notice Complete a retraining execution successfully
     * @param executionId ID of the execution
     * @param newModelCID IPFS CID of the retrained model
     * @param gasUsed Estimated gas used
     */
    function completeExecution(
        uint256 executionId,
        string calldata newModelCID,
        uint256 gasUsed
    ) external onlyOwner nonReentrant {
        require(executionId < executionCount, "Invalid execution ID");
        require(bytes(newModelCID).length > 0, "Model CID required");
        
        RetrainingExecution storage execution = executions[executionId];
        require(execution.status == ExecutionStatus.InProgress, "Not in progress");
        
        address operator = execution.operator;
        
        // Update execution
        execution.newModelCID = newModelCID;
        execution.gasUsed = gasUsed;
        execution.status = ExecutionStatus.Completed;
        
        // Calculate reward
        uint256 rewardAmount = calculateExecutionReward(gasUsed, true);
        execution.rewardAmount = rewardAmount;
        
        // Update operator stats
        operators[operator].successfulExecutions++;
        operators[operator].totalRewardsEarned += rewardAmount;
        
        // Distribute reward
        string memory reason = string(abi.encodePacked(
            "Retraining execution completed: ",
            newModelCID
        ));
        tokenomics.distributeOperatorReward(operator, rewardAmount, reason);
        
        emit ExecutionCompleted(executionId, operator, newModelCID, rewardAmount);
    }
    
    /**
     * @notice Mark execution as failed and apply penalty
     * @param executionId ID of the execution
     */
    function failExecution(uint256 executionId) external onlyOwner nonReentrant {
        require(executionId < executionCount, "Invalid execution ID");
        
        RetrainingExecution storage execution = executions[executionId];
        require(execution.status == ExecutionStatus.InProgress, "Not in progress");
        
        address operator = execution.operator;
        execution.status = ExecutionStatus.Failed;
        
        // Apply penalty
        uint256 penaltyAmount = failurePenalty;
        if (operators[operator].stakedAmount >= penaltyAmount) {
            operators[operator].stakedAmount -= penaltyAmount;
            emit OperatorSlashed(operator, penaltyAmount, "Execution failed");
        }
        
        // Check for consecutive failures
        uint256 recentFailures = countRecentFailures(operator);
        if (recentFailures >= maxConsecutiveFailures) {
            operators[operator].isActive = false;
            emit OperatorStatusChanged(operator, false);
        }
        
        emit ExecutionFailed(executionId, operator, penaltyAmount);
    }
    
    /**
     * @notice Calculate execution reward
     * @param gasUsed Gas used in execution
     * @param successful Whether execution was successful
     * @return Reward amount
     */
    function calculateExecutionReward(
        uint256 gasUsed,
        bool successful
    ) public view returns (uint256) {
        // Base reward + gas reimbursement
        uint256 gasReimbursement = (gasUsed * gasReimbursementRate) / 100;
        uint256 reward = baseExecutionReward + gasReimbursement;
        
        // Apply success bonus
        if (successful) {
            reward = (reward * successBonusMultiplier) / 100;
        }
        
        return reward;
    }
    
    /**
     * @notice Count recent failures for an operator (simplified - last 10 executions)
     */
    function countRecentFailures(address operator) internal view returns (uint256) {
        uint256 failures = 0;
        uint256 checked = 0;
        
        // Check last 10 executions
        for (uint256 i = executionCount; i > 0 && checked < 10; i--) {
            if (executions[i - 1].operator == operator) {
                if (executions[i - 1].status == ExecutionStatus.Failed) {
                    failures++;
                }
                checked++;
            }
        }
        
        return failures;
    }
    
    /**
     * @notice Update operator status
     */
    function setOperatorStatus(address operator, bool isActive) external onlyOwner {
        require(operators[operator].registrationTime > 0, "Not registered");
        operators[operator].isActive = isActive;
        emit OperatorStatusChanged(operator, isActive);
    }
    
    /**
     * @notice Set staking parameters
     */
    function setStakingParameters(
        uint256 _minimumStake,
        uint256 _failurePenalty,
        uint256 _maxConsecutiveFailures
    ) external onlyOwner {
        minimumStake = _minimumStake;
        failurePenalty = _failurePenalty;
        maxConsecutiveFailures = _maxConsecutiveFailures;
    }
    
    /**
     * @notice Set reward parameters
     */
    function setRewardParameters(
        uint256 _baseReward,
        uint256 _gasReimbursementRate,
        uint256 _successBonusMultiplier
    ) external onlyOwner {
        baseExecutionReward = _baseReward;
        gasReimbursementRate = _gasReimbursementRate;
        successBonusMultiplier = _successBonusMultiplier;
    }
    
    /**
     * @notice Get operator details
     */
    function getOperator(address operator) external view returns (
        bool isActive,
        uint256 stakedAmount,
        uint256 registrationTime,
        uint256 totalExecutions,
        uint256 successfulExecutions,
        uint256 totalRewardsEarned,
        string memory endpoint
    ) {
        Operator memory op = operators[operator];
        return (
            op.isActive,
            op.stakedAmount,
            op.registrationTime,
            op.totalExecutions,
            op.successfulExecutions,
            op.totalRewardsEarned,
            op.endpoint
        );
    }
    
    /**
     * @notice Get total number of registered operators
     */
    function getOperatorCount() external view returns (uint256) {
        return operatorList.length;
    }
    
    /**
     * @notice Get execution details
     */
    function getExecution(uint256 executionId) external view returns (
        address operator,
        string memory datasetCID,
        string memory oldModelCID,
        string memory newModelCID,
        uint256 executionTime,
        uint256 gasUsed,
        ExecutionStatus status,
        uint256 rewardAmount
    ) {
        require(executionId < executionCount, "Invalid execution ID");
        RetrainingExecution memory exec = executions[executionId];
        
        return (
            exec.operator,
            exec.datasetCID,
            exec.oldModelCID,
            exec.newModelCID,
            exec.executionTime,
            exec.gasUsed,
            exec.status,
            exec.rewardAmount
        );
    }
}
