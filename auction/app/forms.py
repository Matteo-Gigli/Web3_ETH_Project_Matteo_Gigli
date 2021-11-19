from django import forms
from .models import Item, Customer

class NFT(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'symbol', 'image', 'bio', 'itemUrl', 'creatorAddress', 'startingPrice', 'endingAuction']
        labels = {'name': 'Name', 'symbol': 'Set a 10 Letter Max Symbol', 'bio': 'Bio',
                 'itemUrl': 'Item Url', 'creatorAddress': 'Your Address',
                 'startingPrice': 'Set Initial Price', 'endingAuction': 'Auction Ending On'}


class Conversion(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['dollarBalance']


class TokenOffer(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['tokenOffer']