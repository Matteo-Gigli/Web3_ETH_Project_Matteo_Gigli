from django.shortcuts import render, redirect
from .forms import Registration
from app.models import Customer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
import json
from web3 import Web3
import random
import pymongo

# Using MongoDB Database
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["ETH__Project__Web3"]


#Connect to Ganache
ganache_url = 'http://127.0.0.1:7545'
w3 = Web3(Web3.HTTPProvider(ganache_url))

#Set first account as Faucet
w3.eth.defaultAccount = w3.eth.accounts[0]
Faucet = w3.eth.defaultAccount



#Contract for Token ERC20 is already deployed from remix
contractAddress = w3.toChecksumAddress('0xC852d33c781cA04dE02b9704cF81a473972022a5')
abi = json.loads('''[{"inputs":[{"internalType":"uint256","name":"totalSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]''')
contract = w3.eth.contract(address=contractAddress, abi=abi)

#We are sending 10 free tokens at the registration
def registration(request):
    if request.method == 'POST':
        form = Registration(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            address = form.cleaned_data['address']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                username=username,
                password=password
            )

            tx = contract.functions.transfer(
                address,
                10000000000000000000
            ).transact({'from': Faucet})
            addressBalance = contract.functions.balanceOf(address).call()
            tBalance = w3.fromWei(addressBalance, 'ether')

            newCustomer = Customer(
                user=user,
                address=address,
                tokenBalance=tBalance,
                dollarBalance=random.randrange(500, 1500)
            )
            user.save()
            newCustomer.save()

            myColl = mydb['Registration Token Gift']
            informationAbout = {
                'From': Faucet,
                'Tx Hash': w3.toHex(tx),
                'To': newCustomer.address,
            }
            populateDatabase = myColl.insert_one(informationAbout)
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'''Welcome in Start2Auction {request.user}, some tokens and some dollar has been accreditate to your account''')
            return redirect('/homepage/')

    else:
        form = Registration()
        context = {'form': form}
        return render(request, 'registrationForm.html', context)
