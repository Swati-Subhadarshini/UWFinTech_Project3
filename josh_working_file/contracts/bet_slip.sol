pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract betWithFriends is ERC721Full {

    address payable owner = msg.sender;
    uint public accountBalance;
    address payable authorizedRecipient;

    constructor() public ERC721Full("BetSlip", "BET") {}

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

        bool sent = receiver.send(msg.value);
        require(sent, "Failed to send Ether");
        accountBalance = address(this).balance;
    }

    function updateBet(
        uint256 betID,
        uint256 newEarnedPayout
    ) public returns (uint256) {
        betHistory[betID].earnedPayout = newEarnedPayout;

        emit completeBet(betID, newEarnedPayout);

        return betHistory[betID].earnedPayout;
    }

    function deposit() public payable {
        accountBalance = address(this).balance;
    }

    function() external payable {}
}
