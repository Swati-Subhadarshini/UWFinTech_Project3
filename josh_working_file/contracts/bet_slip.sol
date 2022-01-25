pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract Certificate is ERC721Full {
    constructor() public ERC721Full("BetSlip", "BET") {}

    struct Bet {
        string username;
        string matchup;
        uint256 amountBet;
        uint256 amountPayable;
    }

    mapping(uint256 => Bet) public betHistory;

    event completeBet(uint256 betID, uint256 initalBet, uint256 amountPayable);

    function placeBet(
        address user,
        string memory username,
        string memory matchup,
        uint256 amountBet,
        uint256 amountPayable
        )
        public returns (uint256)
    {
        uint256 betID = totalSupply();
        amountPayable = 0;
        _mint(user, betID);

        betHistory[betID] = Bet(username, matchup, amountBet, amountPayable);

        return betID;
    }
}
