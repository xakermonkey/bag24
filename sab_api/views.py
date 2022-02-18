from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status
from lostitems.models import *
from bag_admin.models import *
from .serializers import *
from datetime import datetime
import random


# Create your views here.


def send_code(number):
    var_code, _ = VerifyCode.objects.get_or_create(phone=number)
    code = random.randint(999, 9999)
    var_code.code = code
    var_code.save()


class apiLogin(APIView):
    def post(self, request):
        if 'number' in request.data:
            user = User.objects.filter(phone=request.data.get('number')).first()
            if not user:
                return Response(status=404, data={"status": False,
                                                  "detail": "Пользователя с таким номером телефона не существует!"})
            if user.status == "us":
                return Response(status=403, data={"status": False, "detail": "Недостаточно прав!"})
            send_code(number=user.phone)
            return Response(status=200, data={"status": True})
        else:
            user = authenticate(username=request.data.get("username"),
                                password=request.data.get('password'))
            if not user:
                return Response(data={'status': False, 'detail': "Неверные данные"})
            if user.status == "us":
                return Response(data={'status': False, "datail": 'Недостаточно прав!'})
            token = Token.objects.get(user=user)

            return Response(data={"status": True, 'token': token.key})


class verifyCode(APIView):
    def post(self, request):
        ver_code = VerifyCode.objects.filter(phone=request.data.get("number")).first()
        if not ver_code:
            return Response(status=404,
                            data={"status": False, "detail": "На этот телефон не было отправлено сообщение"})
        if ver_code.code != request.data.get('code'):
            return Response(data={"status": False, "detail": "Неверный код"})
        else:
            token = Token.objects.get(user=User.objects.get(phone=request.data.get("number")))
            return Response(status=200, data={"status": True, "token": token.key})


class createItem(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        item = SABItem.objects.create(user=request.user,
                                      date=datetime.fromtimestamp(int(request.POST.get('date')) / 1000.0),
                                      place=LuggageStorage.objects.get(id=int(request.POST.get("lg_id"))),
                                      act=True if request.POST.get('act') == 'true' else False,
                                      comment=request.POST.get("comment"))
        for i in request.FILES:
            photo = PhotoSerializer(data={
                'photo': request.FILES.get(i),
                'item': item.id
            })
            if photo.is_valid():
                photo.save()
            else:
                return Response(data={"status": False})
        return Response(data={"status": True})

    def get(self, request):
        lg = LuggageStorage.objects.all()
        serializer = LGSerializer(lg, many=True)
        return Response(serializer.data)


class listItem(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = SABItem.objects.filter(user=request.user)
        photos = Photos.objects.filter(item__user=request.user)
        photo_ser = PhotoSerializer(photos, many=True)
        serializer = SABItemSerializer(items, many=True)
        return Response(data={'item': serializer.data, 'photos': photo_ser.data})
