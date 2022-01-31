pragma solidity ^0.5.0;

/// Ownable so that we can more easily control ownership in the contract ///
/// Roles may be useful as well, for minting additional coins ///

import "@openzeppelin/contracts/access/Ownable.sol";

/// Reentrancy library purported more secure, prevents a contract from calling itself///

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/// IERC20 library to more easily manage existing tokens ///

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/math/SafeMath.sol";







contract BetsWithFriends is Ownable, ReentrancyGuard {

    

    IERC20 private SBLIV;

    struct Bet {
        address user;  // who placed it
        bytes32 eventId;       // if needed, Id on event or game itself
        uint    amount;        // bet amount
        uint256 chosenWinner;  // Winning team, awarding bet //
    }


    ///uint internal minimumBet = 1.0 SBLIV; // How to convert from ETH? ///
    ///uint internal maximumBet = 10000.0 SBLIV; // How to convert from ETH? ///

    enum Outcome {
        team1,
        team2
    }

    event BettingInfo(
        address _player,
        bytes32 _eventId,
        uint _amount,
        uint256 _chosenWinner
    );

    constructor(address _tokenAddress) {
        SBLIV = IERC20(_tokenAddress); /// is this where main SBLIV address goes? ///
    }


    /// asks for contract address balance of SBLIV ///

    function getContractSBLIVBalance()
        public view returns (uint)
      {
          return SBLIV.balanceOf(address(this));


    ///should move funds from sender to this contract ///

    function deposit(address _sender, uint _amount)
        external


        /// minimum amount for contract ///

        require(_amount >= 1, "Amount deposited must be >= 1");
        SBLIV.transferFrom(_sender, address(this), _amount);

    /// standard for ERC20 token, approves movement of funds from token owner ///

    function approve(address _spender, uint _amount)
         external 
         
    {
        SBLIV.approve(_spender, _amount);
    }


    function placeBet(bytes32 _eventId, uint8 _chosenWinner) 
        public payable
        msg.sender
        nonReentrant /// for simplicity and security ///
    {
        // At least a minimum amout is required to bet
        require(msg.value >= minimumBet, "Bet amount must be >= minimum bet");

        // transfer the player's money into the contract's account 
        payable(address(this)).transfer(msg.value);

        // add the new bet 
        Bet[] storage bets = eventToBets[_eventId]; 
        bets.push( Bet(msg.sender, _eventId, msg.value, _chosenWinner)); 

        // add the mapping
        bytes32[] storage userBets = userToBets[msg.sender]; 
        userBets.push(_eventId);

        emit BettingInfo(
            _eventId,
            msg.sender,      // player
            _chosenWinner, 
            msg.value        // bet amount
        );
    }


    receive() external payable {
    }





}




/// how to link to outside world as well as front-end? ///
