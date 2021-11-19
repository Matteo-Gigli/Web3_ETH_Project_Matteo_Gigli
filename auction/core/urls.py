from django.urls import path
from .views import Homeview

urlpatterns = [
    path('homepage/', Homeview.as_view(), name='homepage'),

]