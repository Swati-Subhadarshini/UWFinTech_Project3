pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract betWithFriends is ERC721Full {

    address payable owner;
    uint public accountBalance;
    address payable authorizedRecipient;

    constructor() public ERC721Full("BetSlip", "BET") {
        owner = msg.sender;
    }

    modifier onlyOwner() {
    require(msg.sender == owner, "Only admin can update.");
    _;
    }

    struct Bet {
        string username;
        string betSelection;
        uint256 amountOfWager;
        uint256 earnedPayout; 
    }

    mapping(uint256 => Bet) public betHistory;

    event completeBet(uint256 betID, uint256 earnedPayout);

    function placeBet (
        address payable user,
        string memory username,
        string memory betSelection
        )
        public payable {
        uint256 amountOfWager = msg.value;
        uint256 betID = totalSupply();
        uint256 earnedPayout = 0;
        address payable receiver = address(this);

        _mint(user, betID);

        betHistory[betID] = Bet(username, betSelection, amountOfWager, earnedPayout);

        bool sent = receiver.send(amountOfWager);
        require(sent, "Failed to send Ether");
        accountBalance = address(this).balance;
    }

    function reviewBet(uint256 betID) public view returns (string memory, string memory, uint256, uint256) {
        
        string memory _username = betHistory[betID].username;
        string memory _betSelection = betHistory[betID].betSelection;
        uint256 _amountOfWager = betHistory[betID].amountOfWager;
        uint256 _earnedPayout = betHistory[betID].earnedPayout;
        
        return (_username, _betSelection, _amountOfWager, _earnedPayout);
    }

    function updateBet(uint256 betID, uint256 newEarnedPayout) public onlyOwner returns (uint256) {

        betHistory[betID].earnedPayout = newEarnedPayout;

        emit completeBet(betID, newEarnedPayout);

        return betHistory[betID].earnedPayout;
    }

    function transferProfits(uint amount, address payable recipient) public {
        require(recipient == owner || recipient == authorizedRecipient, "The recipient address is not authorized!");
        recipient.transfer(amount);
        accountBalance = address(this).balance;
    }

    function deposit() public payable {
        accountBalance = address(this).balance;
    }

    function() external payable {}
}
