// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

interface IEuystacioSTAnchor {
    function redCodeVetoAuthority() external view returns (address);
    function deploymentSealed() external view returns (bool);
    function governanceStateLocked() external view returns (bool);
    function invokeRedCodeVeto(string calldata reason) external;
}

contract EUSDaoGovernance is ERC20, Ownable {
    mapping(address => uint256) public contributionScore;
    
    /// @notice EuystacioSTAnchor contract for Red Code Veto H-Var integration
    IEuystacioSTAnchor public stAnchor;
    
    /// @notice Whether Red Code Veto integration is enabled
    bool public redCodeVetoEnabled;
    
    event STAnchorSet(address indexed stAnchor);
    event RedCodeVetoEnabled(bool enabled);
    event RedCodeVetoInvokedInGovernance(address indexed invoker, string reason);

    constructor() ERC20("Euystacio Stewardship", "EUS") {}

    /**
     * @notice Set the EuystacioSTAnchor contract address for Red Code Veto integration
     * @param _stAnchor Address of the EuystacioSTAnchor contract
     */
    function setSTAnchor(address _stAnchor) external onlyOwner {
        require(_stAnchor != address(0), "Invalid STAnchor address");
        stAnchor = IEuystacioSTAnchor(_stAnchor);
        emit STAnchorSet(_stAnchor);
    }
    
    /**
     * @notice Enable Red Code Veto integration
     * @param enabled Whether to enable Red Code Veto integration
     */
    function setRedCodeVetoEnabled(bool enabled) external onlyOwner {
        require(address(stAnchor) != address(0), "STAnchor not set");
        redCodeVetoEnabled = enabled;
        emit RedCodeVetoEnabled(enabled);
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
     * @notice Invoke Red Code Veto through governance (requires veto authority)
     * @param reason The ethical reason for invoking the veto
     */
    function invokeRedCodeVetoFromGovernance(string calldata reason) external {
        require(redCodeVetoEnabled, "Red Code Veto not enabled");
        require(address(stAnchor) != address(0), "STAnchor not set");
        require(msg.sender == stAnchor.redCodeVetoAuthority(), "Not veto authority");
        
        stAnchor.invokeRedCodeVeto(reason);
        emit RedCodeVetoInvokedInGovernance(msg.sender, reason);
    }
    
    /**
     * @notice Check if governance is operating under sealed deployment
     */
    function isGovernanceSealed() external view returns (bool) {
        if (address(stAnchor) == address(0)) return false;
        return stAnchor.deploymentSealed() && stAnchor.governanceStateLocked();
    }
}