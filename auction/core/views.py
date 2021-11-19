from django.shortcuts import render
from app.models import Item
from django.views.generic.list import ListView
import json
from web3 import Web3
from django.utils import timezone
import pymongo

# Using MongoDB Database
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["ETH__Project__Web3"]

ganache_url = 'http://127.0.0.1:7545'
w3 = Web3(Web3.HTTPProvider(ganache_url))

#We are setting recipient for sending money at the end, from the recipient address to the creator address
w3.eth.defaultAccount = w3.eth.accounts[1]
Recipient = w3.eth.defaultAccount

#Some fee to pay at the end of the auction.
#We setting an address for the admin in this case the third account on ganache
w3.eth.defaultAccount = w3.eth.accounts[2]
AdminAddressForFee = w3.eth.defaultAccount

#Token ERC721
contractAddress = w3.toChecksumAddress('0xe9642c097B4A681B9A159Ea8270aA1BA6aC15Fee')
abi = json.loads('''[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"string","name":"","type":"string"}],"name":"AlreadyExist","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_owner","type":"address"},{"internalType":"string","name":"tokenUri","type":"string"},{"internalType":"string","name":"name_","type":"string"},{"internalType":"string","name":"symbol_","type":"string"}],"name":"Mintable","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"}],"name":"_id","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balances","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"owning","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_from","type":"address"},{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"sendToken721","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"uri","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"uriDeployed","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]''')
bytecode = '608060405234801561001057600080fd5b50600436106101585760003560e01c806372e77b15116100c3578063b46bbe621161007c578063b46bbe6214610411578063b88d4fde1461042d578063c87b56dd14610449578063ce4636e514610479578063d28d8852146104a9578063e985e9c5146104c757610158565b806372e77b151461033b5780638da5cb5b1461036b57806395d89b41146103895780639f89b563146103a7578063a22cb465146103d7578063b09f1266146103f357610158565b806323b872dd1161011557806323b872dd1461024357806327e235e31461025f57806342842e0e1461028f5780636352211e146102ab57806370a08231146102db578063724868af1461030b57610158565b8063011d02091461015d57806301ffc9a71461017957806306fdde03146101a9578063081812fc146101c7578063095ea7b3146101f75780630e89341c14610213575b600080fd5b61017760048036038101906101729190612354565b6104f7565b005b610193600480360381019061018e919061244f565b610724565b6040516101a09190612907565b60405180910390f35b6101b1610806565b6040516101be9190612922565b60405180910390f35b6101e160048036038101906101dc91906124f2565b610898565b6040516101ee91906128a0565b60405180910390f35b610211600480360381019061020c919061240f565b61091d565b005b61022d600480360381019061022891906124f2565b610a35565b60405161023a9190612922565b60405180910390f35b61025d6004803603810190610258919061223e565b610ad5565b005b610279600480360381019061027491906121d1565b610b35565b6040516102869190612b84565b60405180910390f35b6102a960048036038101906102a4919061223e565b610b4d565b005b6102c560048036038101906102c091906124f2565b610b6d565b6040516102d291906128a0565b60405180910390f35b6102f560048036038101906102f091906121d1565b610c1f565b6040516103029190612b84565b60405180910390f35b610325600480360381019061032091906124a9565b610cd7565b6040516103329190612907565b60405180910390f35b610355600480360381019061035091906124f2565b610d0d565b60405161036291906128a0565b60405180910390f35b610373610d40565b60405161038091906128a0565b60405180910390f35b610391610d66565b60405161039e9190612922565b60405180910390f35b6103c160048036038101906103bc91906124f2565b610df8565b6040516103ce9190612922565b60405180910390f35b6103f160048036038101906103ec9190612314565b610ea4565b005b6103fb610eba565b6040516104089190612922565b60405180910390f35b61042b6004803603810190610426919061223e565b610f48565b005b61044760048036038101906104429190612291565b6111d9565b005b610463600480360381019061045e91906124f2565b61123b565b6040516104709190612922565b60405180910390f35b610493600480360381019061048e91906124a9565b6112e2565b6040516104a09190612b84565b60405180910390f35b6104b1611310565b6040516104be9190612922565b60405180910390f35b6104e160048036038101906104dc91906121fe565b61139e565b6040516104ee9190612907565b60405180910390f35b600f836040516105079190612865565b908152602001604051809103902060009054906101000a900460ff1615610563576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161055a90612a64565b60405180910390fd5b61056d6006611432565b3393508160079080519060200190610586929190611fe5565b50806008908051906020019061059d929190611fe5565b5060006105aa6006611448565b9050600e849080600181540180825580915050600190039060005260206000200160009091909190915090805190602001906105e7929190611fe5565b506105f28582611456565b6001600f856040516106049190612865565b908152602001604051809103902060006101000a81548160ff02191690831515021790555084600b600083815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055506001600a60008773ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282546106cb9190612c69565b9250508190555083600c600083815260200190815260200160002090805190602001906106f9929190611fe5565b5080600d8560405161070b9190612865565b9081526020016040518091039020819055505050505050565b60007f80ac58cd000000000000000000000000000000000000000000000000000000007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916827bffffffffffffffffffffffffffffffffffffffffffffffffffffffff191614806107ef57507f5b5e139f000000000000000000000000000000000000000000000000000000007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916827bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916145b806107ff57506107fe82611624565b5b9050919050565b60606000805461081590612dda565b80601f016020809104026020016040519081016040528092919081815260200182805461084190612dda565b801561088e5780601f106108635761010080835404028352916020019161088e565b820191906000526020600020905b81548152906001019060200180831161087157829003601f168201915b5050505050905090565b60006108a38261168e565b6108e2576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016108d990612aa4565b60405180910390fd5b6004600083815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff169050919050565b600061092882610b6d565b90508073ffffffffffffffffffffffffffffffffffffffff168373ffffffffffffffffffffffffffffffffffffffff161415610999576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161099090612b04565b60405180910390fd5b8073ffffffffffffffffffffffffffffffffffffffff166109b86116fa565b73ffffffffffffffffffffffffffffffffffffffff1614806109e757506109e6816109e16116fa565b61139e565b5b610a26576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610a1d90612a04565b60405180910390fd5b610a308383611702565b505050565b600c6020528060005260406000206000915090508054610a5490612dda565b80601f0160208091040260200160405190810160405280929190818152602001828054610a8090612dda565b8015610acd5780601f10610aa257610100808354040283529160200191610acd565b820191906000526020600020905b815481529060010190602001808311610ab057829003601f168201915b505050505081565b610ae6610ae06116fa565b826117bb565b610b25576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610b1c90612b64565b60405180910390fd5b610b30838383611899565b505050565b600a6020528060005260406000206000915090505481565b610b68838383604051806020016040528060008152506111d9565b505050565b6000806002600084815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff169050600073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff161415610c16576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610c0d90612a44565b60405180910390fd5b80915050919050565b60008073ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff161415610c90576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610c8790612a24565b60405180910390fd5b600360008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020549050919050565b600f818051602081018201805184825260208301602085012081835280955050505050506000915054906101000a900460ff1681565b600b6020528060005260406000206000915054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b600960009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b606060018054610d7590612dda565b80601f0160208091040260200160405190810160405280929190818152602001828054610da190612dda565b8015610dee5780601f10610dc357610100808354040283529160200191610dee565b820191906000526020600020905b815481529060010190602001808311610dd157829003601f168201915b5050505050905090565b600e8181548110610e0857600080fd5b906000526020600020016000915090508054610e2390612dda565b80601f0160208091040260200160405190810160405280929190818152602001828054610e4f90612dda565b8015610e9c5780601f10610e7157610100808354040283529160200191610e9c565b820191906000526020600020905b815481529060010190602001808311610e7f57829003601f168201915b505050505081565b610eb6610eaf6116fa565b8383611af5565b5050565b60088054610ec790612dda565b80601f0160208091040260200160405190810160405280929190818152602001828054610ef390612dda565b8015610f405780601f10610f1557610100808354040283529160200191610f40565b820191906000526020600020905b815481529060010190602001808311610f2357829003601f168201915b505050505081565b600b600082815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614610fe9576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610fe090612b24565b60405180910390fd5b600073ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff161415611059576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161105090612b44565b60405180910390fd5b600073ffffffffffffffffffffffffffffffffffffffff168373ffffffffffffffffffffffffffffffffffffffff1614156110c9576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016110c090612944565b60405180910390fd5b6001600a60008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282546111199190612cf0565b925050819055506001600a60008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282546111709190612c69565b9250508190555081600b600083815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055506111d4838383610ad5565b505050565b6111ea6111e46116fa565b836117bb565b611229576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161122090612b64565b60405180910390fd5b61123584848484611c62565b50505050565b60606112468261168e565b611285576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161127c90612ae4565b60405180910390fd5b600061128f611cbe565b905060008151116112af57604051806020016040528060008152506112da565b806112b984611cd5565b6040516020016112ca92919061287c565b6040516020818303038152906040525b915050919050565b600d818051602081018201805184825260208301602085012081835280955050505050506000915090505481565b6007805461131d90612dda565b80601f016020809104026020016040519081016040528092919081815260200182805461134990612dda565b80156113965780601f1061136b57610100808354040283529160200191611396565b820191906000526020600020905b81548152906001019060200180831161137957829003601f168201915b505050505081565b6000600560008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff16905092915050565b6001816000016000828254019250508190555050565b600081600001549050919050565b600073ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff1614156114c6576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016114bd90612a84565b60405180910390fd5b6114cf8161168e565b1561150f576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161150690612984565b60405180910390fd5b61151b60008383611e36565b6001600360008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600082825461156b9190612c69565b92505081905550816002600083815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550808273ffffffffffffffffffffffffffffffffffffffff16600073ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef60405160405180910390a45050565b60007f01ffc9a7000000000000000000000000000000000000000000000000000000007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916827bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916149050919050565b60008073ffffffffffffffffffffffffffffffffffffffff166002600084815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1614159050919050565b600033905090565b816004600083815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550808273ffffffffffffffffffffffffffffffffffffffff1661177583610b6d565b73ffffffffffffffffffffffffffffffffffffffff167f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b92560405160405180910390a45050565b60006117c68261168e565b611805576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016117fc906129e4565b60405180910390fd5b600061181083610b6d565b90508073ffffffffffffffffffffffffffffffffffffffff168473ffffffffffffffffffffffffffffffffffffffff16148061187f57508373ffffffffffffffffffffffffffffffffffffffff1661186784610898565b73ffffffffffffffffffffffffffffffffffffffff16145b80611890575061188f818561139e565b5b91505092915050565b8273ffffffffffffffffffffffffffffffffffffffff166118b982610b6d565b73ffffffffffffffffffffffffffffffffffffffff161461190f576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161190690612ac4565b60405180910390fd5b600073ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff16141561197f576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401611976906129a4565b60405180910390fd5b61198a838383611e36565b611995600082611702565b6001600360008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282546119e59190612cf0565b925050819055506001600360008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000828254611a3c9190612c69565b92505081905550816002600083815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550808273ffffffffffffffffffffffffffffffffffffffff168473ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef60405160405180910390a4505050565b8173ffffffffffffffffffffffffffffffffffffffff168373ffffffffffffffffffffffffffffffffffffffff161415611b64576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401611b5b906129c4565b60405180910390fd5b80600560008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff0219169083151502179055508173ffffffffffffffffffffffffffffffffffffffff168373ffffffffffffffffffffffffffffffffffffffff167f17307eab39ab6107e8899845ad3d59bd9653f200f220920489ca2b5937696c3183604051611c559190612907565b60405180910390a3505050565b611c6d848484611899565b611c7984848484611e3b565b611cb8576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401611caf90612964565b60405180910390fd5b50505050565b606060405180602001604052806000815250905090565b60606000821415611d1d576040518060400160405280600181526020017f30000000000000000000000000000000000000000000000000000000000000008152509050611e31565b600082905060005b60008214611d4f578080611d3890612e3d565b915050600a82611d489190612cbf565b9150611d25565b60008167ffffffffffffffff811115611d6b57611d6a612f73565b5b6040519080825280601f01601f191660200182016040528015611d9d5781602001600182028036833780820191505090505b5090505b60008514611e2a57600182611db69190612cf0565b9150600a85611dc59190612e86565b6030611dd19190612c69565b60f81b818381518110611de757611de6612f44565b5b60200101907effffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916908160001a905350600a85611e239190612cbf565b9450611da1565b8093505050505b919050565b505050565b6000611e5c8473ffffffffffffffffffffffffffffffffffffffff16611fd2565b15611fc5578373ffffffffffffffffffffffffffffffffffffffff1663150b7a02611e856116fa565b8786866040518563ffffffff1660e01b8152600401611ea794939291906128bb565b602060405180830381600087803b158015611ec157600080fd5b505af1925050508015611ef257506040513d601f19601f82011682018060405250810190611eef919061247c565b60015b611f75573d8060008114611f22576040519150601f19603f3d011682016040523d82523d6000602084013e611f27565b606091505b50600081511415611f6d576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401611f6490612964565b60405180910390fd5b805181602001fd5b63150b7a0260e01b7bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916817bffffffffffffffffffffffffffffffffffffffffffffffffffffffff191614915050611fca565b600190505b949350505050565b600080823b905060008111915050919050565b828054611ff190612dda565b90600052602060002090601f016020900481019282612013576000855561205a565b82601f1061202c57805160ff191683800117855561205a565b8280016001018555821561205a579182015b8281111561205957825182559160200191906001019061203e565b5b509050612067919061206b565b5090565b5b8082111561208457600081600090555060010161206c565b5090565b600061209b61209684612bc4565b612b9f565b9050828152602081018484840111156120b7576120b6612fa7565b5b6120c2848285612d98565b509392505050565b60006120dd6120d884612bf5565b612b9f565b9050828152602081018484840111156120f9576120f8612fa7565b5b612104848285612d98565b509392505050565b60008135905061211b8161344b565b92915050565b60008135905061213081613462565b92915050565b60008135905061214581613479565b92915050565b60008151905061215a81613479565b92915050565b600082601f83011261217557612174612fa2565b5b8135612185848260208601612088565b91505092915050565b600082601f8301126121a3576121a2612fa2565b5b81356121b38482602086016120ca565b91505092915050565b6000813590506121cb81613490565b92915050565b6000602082840312156121e7576121e6612fb1565b5b60006121f58482850161210c565b91505092915050565b6000806040838503121561221557612214612fb1565b5b60006122238582860161210c565b92505060206122348582860161210c565b9150509250929050565b60008060006060848603121561225757612256612fb1565b5b60006122658682870161210c565b93505060206122768682870161210c565b9250506040612287868287016121bc565b9150509250925092565b600080600080608085870312156122ab576122aa612fb1565b5b60006122b98782880161210c565b94505060206122ca8782880161210c565b93505060406122db878288016121bc565b925050606085013567ffffffffffffffff8111156122fc576122fb612fac565b5b61230887828801612160565b91505092959194509250565b6000806040838503121561232b5761232a612fb1565b5b60006123398582860161210c565b925050602061234a85828601612121565b9150509250929050565b6000806000806080858703121561236e5761236d612fb1565b5b600061237c8782880161210c565b945050602085013567ffffffffffffffff81111561239d5761239c612fac565b5b6123a98782880161218e565b935050604085013567ffffffffffffffff8111156123ca576123c9612fac565b5b6123d68782880161218e565b925050606085013567ffffffffffffffff8111156123f7576123f6612fac565b5b6124038782880161218e565b91505092959194509250565b6000806040838503121561242657612425612fb1565b5b60006124348582860161210c565b9250506020612445858286016121bc565b9150509250929050565b60006020828403121561246557612464612fb1565b5b600061247384828501612136565b91505092915050565b60006020828403121561249257612491612fb1565b5b60006124a08482850161214b565b91505092915050565b6000602082840312156124bf576124be612fb1565b5b600082013567ffffffffffffffff8111156124dd576124dc612fac565b5b6124e98482850161218e565b91505092915050565b60006020828403121561250857612507612fb1565b5b6000612516848285016121bc565b91505092915050565b61252881612d24565b82525050565b61253781612d36565b82525050565b600061254882612c26565b6125528185612c3c565b9350612562818560208601612da7565b61256b81612fb6565b840191505092915050565b600061258182612c31565b61258b8185612c4d565b935061259b818560208601612da7565b6125a481612fb6565b840191505092915050565b60006125ba82612c31565b6125c48185612c5e565b93506125d4818560208601612da7565b80840191505092915050565b60006125ed601a83612c4d565b91506125f882612fc7565b602082019050919050565b6000612610603283612c4d565b915061261b82612ff0565b604082019050919050565b6000612633601c83612c4d565b915061263e8261303f565b602082019050919050565b6000612656602483612c4d565b915061266182613068565b604082019050919050565b6000612679601983612c4d565b9150612684826130b7565b602082019050919050565b600061269c602c83612c4d565b91506126a7826130e0565b604082019050919050565b60006126bf603883612c4d565b91506126ca8261312f565b604082019050919050565b60006126e2602a83612c4d565b91506126ed8261317e565b604082019050919050565b6000612705602983612c4d565b9150612710826131cd565b604082019050919050565b6000612728601383612c4d565b91506127338261321c565b602082019050919050565b600061274b602083612c4d565b915061275682613245565b602082019050919050565b600061276e602c83612c4d565b91506127798261326e565b604082019050919050565b6000612791602983612c4d565b915061279c826132bd565b604082019050919050565b60006127b4602f83612c4d565b91506127bf8261330c565b604082019050919050565b60006127d7602183612c4d565b91506127e28261335b565b604082019050919050565b60006127fa601c83612c4d565b9150612805826133aa565b602082019050919050565b600061281d601883612c4d565b9150612828826133d3565b602082019050919050565b6000612840603183612c4d565b915061284b826133fc565b604082019050919050565b61285f81612d8e565b82525050565b600061287182846125af565b915081905092915050565b600061288882856125af565b915061289482846125af565b91508190509392505050565b60006020820190506128b5600083018461251f565b92915050565b60006080820190506128d0600083018761251f565b6128dd602083018661251f565b6128ea6040830185612856565b81810360608301526128fc818461253d565b905095945050505050565b600060208201905061291c600083018461252e565b92915050565b6000602082019050818103600083015261293c8184612576565b905092915050565b6000602082019050818103600083015261295d816125e0565b9050919050565b6000602082019050818103600083015261297d81612603565b9050919050565b6000602082019050818103600083015261299d81612626565b9050919050565b600060208201905081810360008301526129bd81612649565b9050919050565b600060208201905081810360008301526129dd8161266c565b9050919050565b600060208201905081810360008301526129fd8161268f565b9050919050565b60006020820190508181036000830152612a1d816126b2565b9050919050565b60006020820190508181036000830152612a3d816126d5565b9050919050565b60006020820190508181036000830152612a5d816126f8565b9050919050565b60006020820190508181036000830152612a7d8161271b565b9050919050565b60006020820190508181036000830152612a9d8161273e565b9050919050565b60006020820190508181036000830152612abd81612761565b9050919050565b60006020820190508181036000830152612add81612784565b9050919050565b60006020820190508181036000830152612afd816127a7565b9050919050565b60006020820190508181036000830152612b1d816127ca565b9050919050565b60006020820190508181036000830152612b3d816127ed565b9050919050565b60006020820190508181036000830152612b5d81612810565b9050919050565b60006020820190508181036000830152612b7d81612833565b9050919050565b6000602082019050612b996000830184612856565b92915050565b6000612ba9612bba565b9050612bb58282612e0c565b919050565b6000604051905090565b600067ffffffffffffffff821115612bdf57612bde612f73565b5b612be882612fb6565b9050602081019050919050565b600067ffffffffffffffff821115612c1057612c0f612f73565b5b612c1982612fb6565b9050602081019050919050565b600081519050919050565b600081519050919050565b600082825260208201905092915050565b600082825260208201905092915050565b600081905092915050565b6000612c7482612d8e565b9150612c7f83612d8e565b9250827fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff03821115612cb457612cb3612eb7565b5b828201905092915050565b6000612cca82612d8e565b9150612cd583612d8e565b925082612ce557612ce4612ee6565b5b828204905092915050565b6000612cfb82612d8e565b9150612d0683612d8e565b925082821015612d1957612d18612eb7565b5b828203905092915050565b6000612d2f82612d6e565b9050919050565b60008115159050919050565b60007fffffffff0000000000000000000000000000000000000000000000000000000082169050919050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000819050919050565b82818337600083830152505050565b60005b83811015612dc5578082015181840152602081019050612daa565b83811115612dd4576000848401525b50505050565b60006002820490506001821680612df257607f821691505b60208210811415612e0657612e05612f15565b5b50919050565b612e1582612fb6565b810181811067ffffffffffffffff82111715612e3457612e33612f73565b5b80604052505050565b6000612e4882612d8e565b91507fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff821415612e7b57612e7a612eb7565b5b600182019050919050565b6000612e9182612d8e565b9150612e9c83612d8e565b925082612eac57612eab612ee6565b5b828206905092915050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601260045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052603260045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b600080fd5b600080fd5b600080fd5b600080fd5b6000601f19601f8301169050919050565b7f43616e6e6f742073656e642066726f6d20302061646472657373000000000000600082015250565b7f4552433732313a207472616e7366657220746f206e6f6e20455243373231526560008201527f63656976657220696d706c656d656e7465720000000000000000000000000000602082015250565b7f4552433732313a20746f6b656e20616c7265616479206d696e74656400000000600082015250565b7f4552433732313a207472616e7366657220746f20746865207a65726f2061646460008201527f7265737300000000000000000000000000000000000000000000000000000000602082015250565b7f4552433732313a20617070726f766520746f2063616c6c657200000000000000600082015250565b7f4552433732313a206f70657261746f7220717565727920666f72206e6f6e657860008201527f697374656e7420746f6b656e0000000000000000000000000000000000000000602082015250565b7f4552433732313a20617070726f76652063616c6c6572206973206e6f74206f7760008201527f6e6572206e6f7220617070726f76656420666f7220616c6c0000000000000000602082015250565b7f4552433732313a2062616c616e636520717565727920666f7220746865207a6560008201527f726f206164647265737300000000000000000000000000000000000000000000602082015250565b7f4552433732313a206f776e657220717565727920666f72206e6f6e657869737460008201527f656e7420746f6b656e0000000000000000000000000000000000000000000000602082015250565b7f546f6b656e20416c726561647920457869737400000000000000000000000000600082015250565b7f4552433732313a206d696e7420746f20746865207a65726f2061646472657373600082015250565b7f4552433732313a20617070726f76656420717565727920666f72206e6f6e657860008201527f697374656e7420746f6b656e0000000000000000000000000000000000000000602082015250565b7f4552433732313a207472616e73666572206f6620746f6b656e2074686174206960008201527f73206e6f74206f776e0000000000000000000000000000000000000000000000602082015250565b7f4552433732314d657461646174613a2055524920717565727920666f72206e6f60008201527f6e6578697374656e7420746f6b656e0000000000000000000000000000000000602082015250565b7f4552433732313a20617070726f76616c20746f2063757272656e74206f776e6560008201527f7200000000000000000000000000000000000000000000000000000000000000602082015250565b7f596f7520617265204e4f542074686520546f6b656e204f776e65722100000000600082015250565b7f43616e6e6f742073656e6420746f203020616464726573730000000000000000600082015250565b7f4552433732313a207472616e736665722063616c6c6572206973206e6f74206f60008201527f776e6572206e6f7220617070726f766564000000000000000000000000000000602082015250565b61345481612d24565b811461345f57600080fd5b50565b61346b81612d36565b811461347657600080fd5b50565b61348281612d42565b811461348d57600080fd5b50565b61349981612d8e565b81146134a457600080fd5b5056fea2646970667358221220a53440a8d7be752aa517c3357590546b5672b7c5a4a5877f8a5439640a8f773f64736f6c63430008070033'
contract = w3.eth.contract(address=contractAddress, abi=abi, bytecode=bytecode)


#Token ERC20
contractAddress20 = w3.toChecksumAddress('0x159fbd9F1F686bf29A9fB357A06545Bea99766F3')
abi20 = json.loads('''[{"inputs":[{"internalType":"uint256","name":"totalSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]''')
contract20 = w3.eth.contract(address=contractAddress20, abi=abi20)



class Homeview(ListView):
    queryset = Item.objects.filter().order_by('endingAuction')
    template_name = 'homepage.html'

    for item in queryset:

        feeTransactionCost = item.startingPrice / 100 * 2
        tokenId = contract.functions._id(item.itemUrl).call()

        if item.endingAuction >= timezone.now() and item.tokenOffer == 0:
            noWinnerAuction = {
                'Item Name': item.name,
                'Item Url' : item.itemUrl,
                'Item TX Hash': item.itemHash,
                'Creator': item.creatorAddress
            }
            myColl = mydb['No Winner Auction']
            informationAbout = noWinnerAuction
            populateDatabase = myColl.insert_one(informationAbout)

            item.delete()

        else:
            sendingLastOfferToCreator = contract20.functions.transfer(
                item.creatorAddress,
                w3.toWei(item.tokenOffer, 'ether')
            ).transact({'from': Recipient})

            sendingFeeToAdminAddress = contract20.functions.transfer(
                AdminAddressForFee,
                w3.toWei(feeTransactionCost, 'ether')
            ).transact({'from': item.customer.address})

            sendingTokenFromCreatorToWinner = contract.functions.sendToken721(
                item.creatorAddress,
                item.customer.address,
                tokenId
            ).transact({'from': item.creatorAddress})

            winnerAuction = {
                'Item Name': item.name,
                'Item Url': item.itemUrl,
                'Item Hash': item.itemHash,
                'Creator': item.creatorAddress,
                'Winner': item.customer.address,
                'Price': item.tokenOffer,
                'Transaction For Fee From Creator To Admin Address': w3.toHex(sendingFeeToAdminAddress),
                'Transaction For ERC721 From Creator To Winner': w3.toHex(sendingTokenFromCreatorToWinner),
                'Transaction From Winner To Creator': w3.toHex(sendingLastOfferToCreator),
            }

            myNewColl = mydb ['Winner Auction And Data About It']
            informationAboutIt = winnerAuction
            populateDatabase = myNewColl.insert_one(informationAboutIt)
            item.delete()

