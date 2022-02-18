from .views import *
from django.urls import path


urlpatterns = [
    path('login', StaffLogin, name='staff_login'),
    path('panel', staffPanel, name='staff_panel'),
    path('panel_refound', staffRefound, name='staff_panel_refound'),
    path('panel_refound_sab', staffRefoundSAB, name='staff_panel_refound_sab'),
    path('add_lostitems/<int:pk>', addLostItems, name="add_lostitems"),
    path('refound_lostitems/<int:pk>', refoundLostItem, name="refound_lostitems"),
    path('refound_lostitems/<int:pk>/save', saveRefundItem, name="refound_save"),
    path('refound_lostitems/<int:pk>/file-upload', refoundUploadFile, name="refound_upload-file"),
    path('add_lostitems/get_kind', get_kind, name="get_kind"),
    path('add_lostitems/<int:pk>/save_lostitem', save_lostitem, name="save_lostitem")
]