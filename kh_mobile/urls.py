from .views import *
from django.urls import path

urlpatterns = [
    path('login', apiLogin.as_view()),
    path('set_code', verifyCode.as_view()),
    path("get_code_city", getCodeCity.as_view()),
    path("set_document", createDocument.as_view()),
    path("get_airport", getAirport.as_view()),
    path("get_terminals", getTerminals.as_view()),
    path("get_terminal/<int:pk>", getTerminal.as_view()),
    path("add_luggage", addLuggage.as_view()),
    path("get_orders/<int:pk>", getOrders.as_view()),
    path("send_luggage/<int:pk>", sendLuggage.as_view()),
    path("send_email", sendEmail.as_view()),
    path("verify_email/<str:hash>", verifyEmail.as_view()),
    path("get_profile", getProfile.as_view()),

]