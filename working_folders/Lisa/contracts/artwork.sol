pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract ArtToken is ERC721Full {
    constructor() public ERC721Full("ArtToken", "ART") { }

    function registerArtwork(address owner, string memory tokenURI)
    public
    returns (uint256)
    {
    // TODO: add code to mint new tokens
    uint256 tokenId = totalSupply();
    _mint(owner, tokenId);
    _setTokenURI(tokenId, tokenURI);

    return tokenId;
    }
}