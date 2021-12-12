from django.urls import path
from .views import *

urlpatterns = [
    path('panel', AdminPanel, name='keepit-panel'),
    path('keepit_detail_<int:pk>', AdminPostDetail, name='keepit-detail'),
    path('keepit_history_<int:pk>', AdminPostHistory, name='keepit-history'),
    path('keepit_history_clear_<int:pk>', AdminPostClearHistory, name='keepit-history-clear'),
]