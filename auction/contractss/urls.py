from django.urls import path
from .views import faucetStatus

urlpatterns = [
    path('faucetStatus/', faucetStatus, name='faucetStatus'),

]