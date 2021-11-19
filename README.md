# Web3_ETH_Project_Matteo_Gigli

<h3>💡</h3>
<h3>The Idea</h3>

I am creating an auction site, which is interact with a smart contract deployed on Ganache and built, compile with Remix Ide.<br>
I deployed an <strong>ERC20 token</strong> to create a value spendible in my auction site and an <strong>ERC721 token</strong> to create NFT. <br>
When a user will register, a contract function is automatically call, and the new user will recive an amount of 10 tokens, and even an amount in range 500, 1500 of dollars.<br>
Used database is MongoDB which will save the address who recived the registration token accreditation. the conversion from dollar to tokens and the auction result.<br>
When an auction will finish database will recive the information from the auction like: winner, price, tokenPrice...and will save everything,<br>
obviously depending from the esit of the auction. In fact we have different collections in our database depending by auction result.<br>
If we will use an address different from Ganache addresses, we will have an error. Conversion is 1:1, so 1 Token is 1 dollar

<h3>❗️</h3>
<h3>Important to Know !</h3>
First 3 accounts on Ganache are setted for:

Faucet: Index 0

Recipient: Index 1

Address for fee: Index 2

Start to register from the fourth address on your Ganache

Recipient is made to manage auctions token offer.
Address for fee is for recive fee from auction operations

<h3>🔨</h3>
<h3>Site Fundamentals</h3><br>
<strong>Creating with:</strong><br>
<br>

djongo

web3

Ganache

Remix

Ipfs for the NFT URL
