from .views import *
from django.urls import path

urlpatterns = [
    path('login', ApiLogin.as_view()),
    path('set_code', VerifyCodeView.as_view()),
    path("get_code_city", GetCodeCity.as_view()),
    path("set_document", CreateDocument.as_view()),
    path("get_airport", GetAirport.as_view()),
    path("get_terminals", GetTerminals.as_view()),
    path("get_closed_termianls", GetClosedTerminals.as_view()),
    path("get_terminal/<int:pk>", GetTerminal.as_view()),
    path("add_luggage", AddLuggage.as_view()),
    path("get_luggage", GetLuggage.as_view()),
    path("change_luggage", ChangeStatusLuggage.as_view()),
    path("get_orders/<int:pk>", GetOrders.as_view()),
    path("get_close_orders/<int:pk>", GetCloseOrders.as_view()),
    path("send_luggage/<int:pk>", SendLuggage.as_view()),
    path("take_luggage/<int:pk>", TakeLuggage.as_view()),
    path("send_email", SendEmail.as_view()),
    path("verify_email/<str:hash>", VerifyEmail.as_view()),
    path("get_profile", GetProfile.as_view()),
    path("cards", Card.as_view()),
    path("add_mile_on_air", AddMileOnAir.as_view()),
    path("remove_mile_on_air", RemoveMileOnAir.as_view()),

]