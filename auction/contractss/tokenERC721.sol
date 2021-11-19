//SPDX-License-Identifier: MIT

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/Counters.sol";

pragma solidity >0.6.0 <0.9.0;

contract MyToken is ERC721{
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    string public _name;
    string public _symbol;
    address public owner;
    mapping (address => uint256) public balances;
    mapping (uint256 => address) public owning;
    mapping (uint256 => string) public uri;
    mapping (string => uint256) public _id;

    string[] public uriDeployed;
    mapping (string => bool) public AlreadyExist;

    constructor()ERC721('ERC721', '721'){}

    function Mintable(address _owner, string memory tokenUri, string memory name_, string memory symbol_)public{
        require(! AlreadyExist[tokenUri], 'Token Already Exist');
        _tokenIds.increment();
        _owner = msg.sender;
        _name = name_;
        _symbol = symbol_;
        uint256 newId = _tokenIds.current();
        tokenUri = tokenUri;
        uriDeployed.push(tokenUri);
        super._mint(_owner, newId);
        AlreadyExist[tokenUri] = true;
        owning[newId] = _owner;
        balances[_owner] += 1;
        uri[newId] = tokenUri;
        _id[tokenUri] = newId;
    }

    function sendToken721(address _from, address _to, uint256 _tokenId)public{
        require(msg.sender == owning[_tokenId], 'You are NOT the Token Owner!');
        require(_to != address(0), 'Cannot send to 0 address');
        require(_from != address(0), 'Cannot send from 0 address');
        _from = _from;
        _to = _to;
        _tokenId = _tokenId;
        balances[_from] -= 1;
        balances[_to] += 1;
        owning[_tokenId] = _to;
        super.transferFrom(_from, _to, _tokenId);
    }
}