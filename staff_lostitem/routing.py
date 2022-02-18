from django.urls import path

from .consumer import *



ws_urlpatterns = [
    path('ws/send_item/<int:pk>', sendItemConsumer.as_asgi()),
    path('ws/accept_item/<int:user>', acceptItemConsumer.as_asgi()),
]