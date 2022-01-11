from .views import *
from django.urls import path


urlpatterns = [
    path('login', StaffLogin, name='staff_login'),
    path('panel', staffPanel, name='staff_panel'),
    path('panel_refound', staffRefound, name='staff_panel_refound'),
    path('panel_refound_sab', staffRefoundSAB, name='staff_panel_refound_sab'),
    path('add_lostitems/<int:pk>', addLostItems, name="add_lostitems"),
    path('refound_lostitems/<int:pk>', refoundLostItem, name="refound_lostitems"),
]