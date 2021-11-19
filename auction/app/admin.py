from django.contrib import admin
from .models import Customer, Item

admin.site.register([Customer, Item])
