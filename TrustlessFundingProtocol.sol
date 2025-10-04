pragma solidity ^0.8.0;

contract TrustlessFundingProtocol {
    address public council;
    uint256 public cap;
    bool public ratified;
    mapping(address => uint256) public balances;

    modifier onlyCouncil() {
        require(msg.sender == council, "Not authorized");
        _;
    }

    constructor(uint256 _cap) {
        council = msg.sender;
        cap = _cap;
        ratified = false;
    }

    function ratify() external onlyCouncil {
        ratified = true;
    }

    function deposit() external payable {
        require(ratified, "Not ratified");
        require(address(this).balance <= cap, "Cap exceeded");
        balances[msg.sender] += msg.value;
    }

    function release(address payable recipient, uint256 amount) external onlyCouncil {
        require(address(this).balance >= amount, "Insufficient funds");
        balances[recipient] -= amount;
        recipient.transfer(amount);
    }
}