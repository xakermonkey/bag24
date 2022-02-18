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

    path('set_number', setNumber, name='set_number'),
    path('set_number_in_fill', setNumberInFill, name='set_number_in_fill'),
    path('set_number_in_card', setNumberInCard, name='set_number_in_card'),
    path('valid_code', ValidCode, name='valid_code'),
    path('valid_code_in_fill', ValidCodeInFill, name='valid_code_in_fill'),
    path('valid_code_in_card', ValidCodeInCard, name='valid_code_in_card'),
    path('find_user', findUser, name='find_user'),
    path('remove_address', removeAddress, name='remove_address'),
    path('is_phone', isPhone, name='is_phone'),
    path('add_address', addAddress, name='add_address'),
    path('save_change_user', changeLK, name='save_change_user'),
    path('save_change_document', changeDoc, name='save_change_document'),
    path('file-upload', fileUpload, name="file-upload"),
    path('file-remove', fileRemove, name="file-remove"),
]