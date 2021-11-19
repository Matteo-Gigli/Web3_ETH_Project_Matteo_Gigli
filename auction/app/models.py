from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

class Customer(models.Model):
    user = models.CharField(max_length=50)
    address = models.CharField(max_length=256,
                               blank=False,
                               null=False,
                               unique=True,
                               error_messages={'unique': 'This address is already registered'})
    tokenBalance = models.FloatField(default=0)
    dollarBalance = models.FloatField(default=0)

class Item(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    image = models.ImageField(blank=False, null=False)
    bio = models.TextField()
    itemUrl = models.CharField(max_length=5000)
    itemHash = models.CharField(max_length=256, blank=True, null=False)
    startingPrice = models.FloatField(default=0)
    tokenOffer = models.FloatField(default=0, blank=True, null=True)
    fee = models.FloatField(default=0, blank=True, null=True)
    endingAuction = models.DateTimeField(auto_now_add=False)
    creatorAddress = models.CharField(max_length=256, blank=False, null=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('showItem', kwargs={'pk': self.pk})

    def get_url(self):
        return reverse('tokenOffer', kwargs={'pk': self.pk})