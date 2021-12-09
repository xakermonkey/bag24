from .views import *
from django.urls import path


urlpatterns = [
    path("login", AdminLogin, name='login'),
    path('panel', AdminPanel, name="panel"),
    path('luggage_storage', AdminLuggageStorage, name='kh'),
    path('worker_<int:pk>', AdminWorkerDetail, name='worker'),
    path('thing_cell', AdminThingCell, name="thing-cell")
]
