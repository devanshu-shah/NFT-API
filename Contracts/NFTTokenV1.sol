//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.4;
import "contracts/node_modules/@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "contracts/node_modules/@openzeppelin/contracts/access/ownable.sol";

 contract NFTTokenV1 is ERC721URIStorage, Ownable{
  string public nftName;
  string public nftSymbol;
  uint256 public royalty;
  uint256 public counter=0;

  constructor(string memory _nftName,string memory _nftSymbol) ERC721(_nftName,_nftSymbol)
  {
  }
  
 function mintNFT(address _to, string memory _uri) external onlyOwner {
     counter=counter+1;
    
    super._mint(_to, counter);
    super._setTokenURI(counter,_uri);
  }
 

 }
 
