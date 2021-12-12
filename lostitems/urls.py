from .views import *
from django.urls import path


urlpatterns = [
    path("", loginUserStart, name='login_phone'),
    path("login", loginUser, name='login'),
    path("logout", logoutUser, name='logout'),
    path("registration", registrationUser, name='registration'),

    path("fillprofile", fillProfile, name='fillprofile'),
    path("mainmenu", mainMenu, name='mainmenu'),
    path("deliveryinfo", deliveryInfo, name='deliveryinfo'),
]
