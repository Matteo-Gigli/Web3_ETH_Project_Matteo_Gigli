from django.shortcuts import render
import json
from web3 import Web3

ganache_url = 'http://127.0.0.1:7545'
w3 = Web3(Web3.HTTPProvider(ganache_url))

w3.eth.defaultAccount = w3.eth.accounts[0]
Faucet = w3.eth.defaultAccount

#We are setting even this two address now, just to have a look of everything
w3.eth.defaultAccount = w3.eth.accounts[1]
Recipient = w3.eth.defaultAccount

w3.eth.defaultAccount = w3.eth.accounts[2]
addressFee = w3.eth.defaultAccount

#Contract Token ERC20
contractAddress = w3.toChecksumAddress('0x159fbd9F1F686bf29A9fB357A06545Bea99766F3')
abi = json.loads('''[{"inputs":[{"internalType":"uint256","name":"totalSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]''')
contract = w3.eth.contract(address=contractAddress, abi=abi)


#Show the Faucet Status
def faucetStatus(request):
    contractName = contract.functions.name().call()
    contractSymbol = contract.functions.symbol().call()
    faucetBalance = contract.functions.balanceOf(Faucet).call()
    totalSupply = contract.functions.totalSupply().call()
    balanceFee = contract.functions.balanceOf(addressFee).call
    RecipientBalance = contract.functions.balanceOf(Recipient).call

    context ={
        'contractName': contractName,
        'contractSymbol': contractSymbol,
        'faucetBalance': w3.fromWei(faucetBalance, 'ether'),
        'totalSupply': w3.fromWei(totalSupply, 'ether'),
        'faucet': Faucet,
        'contractAddress': contractAddress,
        'balanceFee': balanceFee,
        'RecipientBalance': RecipientBalance
    }
    return render(request, 'getInfo.html', context)