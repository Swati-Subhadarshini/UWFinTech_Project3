pragma solidity ^0.5.0;


import "github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/math/SafeMath.sol";

contract SportsBetting {

    using SafeMath for uint;

    address User1Address = 0xc3879B456DAA348a16B6524CBC558d2CC984722c;
    string team1;
    string team2;
    uint Team1Odds;
    uint Team2Odds;
    uint accountBalance;

    mapping(address => uint) balances;
    
  
    function getInfo() view public returns(string memory, string memory, uint, uint) {
      return (team1, team2, Team1Odds, Team2Odds);
    }

    function setInfo(string memory NewTeam1, string memory NewTeam2, uint NewTeam1Odds, uint NewTeam2Odds) public {
      team1 = NewTeam1;
      team2 = NewTeam2;
      Team1Odds = NewTeam1Odds;
      Team2Odds = NewTeam2Odds;
      
    }
    // uint holds poitive number and int holds negative or positive number
    function calculatePayout (uint BetAmount, int odds, address payable recipient) public view returns (uint payout, uint profit) {
      
      uint value = 100;
      uint odds1;
      odds1 = uint(odds);

        if(odds < 0){
            profit = (value.div(odds1)).mul(BetAmount);
            payout = BetAmount.add(profit);
            return (profit, payout);
        }

        else{
            profit = (odds1.div(value)).mul(BetAmount);
            payout = BetAmount.add(profit);
            return (profit, payout);
        }
        //recipient.transfer(payout);
        //accountBalance = address(this).balance;
        //return (payout, profit);
        //return profit;
    }

    function deposit() public payable {}

    function() external payable{}
}