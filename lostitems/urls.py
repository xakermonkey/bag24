from .views import *
from django.urls import path


urlpatterns = [
    path("", loginUserStart, name='login_phone'),
    path("login", loginUser, name='login'),
    path("logout", logoutUser, name='logout'),
    path("registration", registrationUser, name='registration'),
]
