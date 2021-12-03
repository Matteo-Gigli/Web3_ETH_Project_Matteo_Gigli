// SPDX-License-Identifier: MIT
pragma solidity >0.5.0 <0.9.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol";

contract start2TokenCoin is ERC20{

    constructor(uint256 totalSupply)ERC20('start2Token', 'S2T'){
        _mint(msg.sender, totalSupply);
    }
}
