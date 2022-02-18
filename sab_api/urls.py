from .views import *
from django.urls import path


urlpatterns = [
    path('login', apiLogin.as_view()),
    path('new_item', createItem.as_view()),
    path('set_code', verifyCode.as_view()),
    path('get_item', listItem.as_view())
]