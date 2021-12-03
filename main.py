#connettere infura

#block.js =

var Web3;

async function Connect(){
    await window.web3.currentProvider.enable();

await window.ethereum.request({method: 'eth_requestAccounts'})

    web3 = new web3(window.web3.currentProvider);
   }

-------------------------------------------------------------------------
#metamask.html

<!DOCTYPE html>
<html lang='en'>
  <head>
    <meta charset='UTF-8' />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Floats</title>
    <link rel='stylesheet' href='styles.css'/>

    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="http://cdn.jsdelivr.net/npm/web3@latest/dist/web3.min.js"></script>

    <script src="./block.js"></script>
  </head>

  <body>
        <input id="connect" type="button" value="Connect" onclick="Connect()">
