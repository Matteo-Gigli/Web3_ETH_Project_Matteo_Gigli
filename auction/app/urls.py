from django.urls import path
from .views import createNft, profile, showItem, conversion, findInSite, tokenOffer

urlpatterns = [
    path('createNft/', createNft, name='createNft'),
    path('profile/', profile, name='profile'),
    path('showItem/<int:pk>', showItem, name='showItem'),
    path('conversion/', conversion, name='conversion'),
    path('findInSite/', findInSite, name='findInSite'),
    path('tokenOffer/<int:pk>', tokenOffer, name='tokenOffer'),

]