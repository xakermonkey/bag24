from .views import *
from django.urls import path


urlpatterns = [
    path("login", AdminLogin, name='login_admin'),
    path("logout", AdminLogout, name='logout_admin'),
    path('panel', AdminPanel, name="panel"),
    path('luggage_storage', AdminLuggageStorage, name='kh'),
    path('worker_<int:pk>', AdminWorkerDetail, name='worker'),
    path('thing_cell', AdminThingCell, name="thing-cell"),
    path('admin_reg', adminRegister, name="admin_reg")
]
