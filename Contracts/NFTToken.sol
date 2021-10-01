//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.4;
import "contracts/node_modules/@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "contracts/node_modules/@openzeppelin/contracts/access/ownable.sol";

 contract NFTToken is ERC721URIStorage, Ownable{
  
  constructor(string memory nftName,string memory nftSymbol)ERC721(nftName,nftSymbol) {
    nftName = "Synth NFT";
    nftSymbol = "SYN";
  }
 function mintNFT(address _to, uint256 _tokenId, string memory _uri) external onlyOwner {
    super._mint(_to, _tokenId);
    super._setTokenURI(_tokenId,_uri);
  }
 
    
 }
 