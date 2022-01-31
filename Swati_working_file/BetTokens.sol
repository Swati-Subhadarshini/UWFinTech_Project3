pragma solidity ^0.5.0;

contract BetToken{
    address payable owner = msg.sender;
    string public symbol = 'SBLIV';
    uint public exchange_rate = 100;

    mapping(address => uint) balances;

    function TokenBalance () public view returns (uint) {
        return balances[msg.sender];
    }

    function tokenTransfer(address BetUser, uint value) public {
        balances[msg.sender] -= value;
        balances[BetUser] += value;
    }

    function buyTokens() public payable{
        uint amount = msg.value * exchange_rate;
        balances[msg.sender] += amount;
        owner.transfer(msg.value);
    }

    function mintToken(address BetUser, uint value) public {
        require(msg.sender == owner, "You do not have permission to mint tokens");
        balances[BetUser] += value;
    }

}