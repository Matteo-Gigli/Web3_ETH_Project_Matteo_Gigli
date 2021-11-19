def createNft(request):
    customer = Customer.objects.get(user=request.user)
    if request.method == 'POST':
        form = NFT(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            name = form.cleaned_data['name']
            symbol = form.cleaned_data['symbol']
            image = form.cleaned_data['image']
            bio = form.cleaned_data['bio']
            itemUrl = form.cleaned_data['itemUrl']
            creatorAddress = form.cleaned_data['creatorAddress']
            startingPrice = form.cleaned_data['startingPrice']
            endingAuction = form.cleaned_data['endingAuction']

            newItem = Item(
                name=name,
                symbol=symbol,
                image=image,
                bio=bio,
                itemUrl=itemUrl,
                creatorAddress=creatorAddress,
                customer=customer,
                startingPrice=startingPrice,
                endingAuction=endingAuction
            )

#This instruction is made for mint the token to the right address, instead anyone can mint a token for us.

            if newItem.customer.address != creatorAddress:
                messages.error(request, 'You are not the address owner')
                return redirect('/homepage/')

#Minting Our Token ERC721

            txHashForERC721 = contract.functions.Mintable(
                customer.address,
                itemUrl,
                name,
                symbol,
            ).transact({'from': customer.address})
            newItem.itemHash = w3.toHex(txHashForERC721)
            customer.save()
            newItem.save()
            form.save()
            messages.success(request, f'''{request.user}...You Minted A New Nft''')
            return redirect('/homepage/')

    else:
        form = NFT()
        context = {'form': form}
        return render(request, 'createNft.html', context)