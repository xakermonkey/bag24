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
from sab_api.serializers import *
from .models import *
from .serializers import *
from datetime import datetime, timezone
import random
from django.core.mail import EmailMessage, send_mail
import requests as r


# Create your views here.


def send_code(number):
    var_code, _ = VerifyCode.objects.get_or_create(phone=number)
    code = random.randint(999, 9999)
    # r.post("https://dev.callback.mileonair.com:8222/api/v1/send/sms",
    #        data={
    #            "phone": number,
    #            "text_sms": f"Ваш код для авторизации в приложении BAG24: {code}. Никому не передавайте его.",
    #            "text_comment": f"BAG24: {number} - {code}"
    #        },
    #        headers={"Authorization": "Bearer k6mCoqbKFDA2mCweY6AaekmwV5tozZdgzqQJZlQGG4TY2YPZtTG0f63jnf3HkfcB"}
    # )
    var_code.code = 2222
    var_code.save()


def create_password():
    import string
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(16))
    return result_str


class ApiLogin(APIView):
    def post(self, request):
        if 'number' in request.data:
            user = User.objects.filter(phone=request.data.get('number')).first()
            if not user:
                user = User.objects.create_user(username=request.data.get("number"), password=create_password(),
                                                phone=request.data.get("number"))
            send_code(number=user.phone)
            return Response(status=200, data={"status": True})


class VerifyCodeView(APIView):
    def post(self, request):
        ver_code = VerifyCode.objects.filter(phone=request.data.get("number")).first()
        if not ver_code:
            return Response(status=404,
                            data={"status": False, "detail": "На этот телефон не было отправлено сообщение"})
        if str(ver_code.code) != request.data.get('code'):
            return Response(data={"status": False, "detail": "Неверный код"})
        else:
            token = Token.objects.get(user=User.objects.get(phone=request.data.get("number")))
            doc, _ = Document.objects.get_or_create(user=User.objects.get(phone=request.data.get("number")))
            docSer = DocumentSerializers(doc).data
            qr, _ = MileOneAir.objects.get_or_create(user=User.objects.get(phone=request.data.get("number")))
            qrCode = QRSerializers(qr).data
            return Response(status=200, data={"status": True, "token": token.key, "doc": docSer, "qr": qrCode})


class GetCodeCity(APIView):

    def get(self, request):
        # import json
        # import requests as r
        # import pycountry
        # import gettext
        # import io
        # from django.core.files.images import ImageFile
        # ru = gettext.translation('iso3166', pycountry.LOCALES_DIR,
        #                          languages=['ru'])
        # ru.install()
        # code = list()
        # with open("countries.json") as f:
        #     data = json.load(f)
        # for county in data["data"]["countries"]:
        #     response = r.get(county["flag_url"], stream=True)
        #     c = pycountry.countries.get(alpha_3=county["iso3"])
        #     if not c is None and not county["phone_mask"].replace("-", "") in code:
        #         code.append(county["phone_mask"].replace("-", ""))
        #         image = ImageFile(io.BytesIO(response.content), name=f'{ru.gettext(c.name)}.jpg')
        #         CodeCity.objects.create(city=ru.gettext(c.name), code=county["phone_mask"].replace("-", ""), flag=image)
        # print("End!!!")
        code = CityCodeSerializers(CodeCity.objects.all(), many=True)
        return Response(status=200, data=code.data)


class CreateDocument(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        document, _ = Document.objects.get_or_create(user=request.user)
        ser = DocumentSerializers(document).data
        return Response(status=200, data=ser)

    def post(self, request):
        document, _ = Document.objects.get_or_create(user=request.user)
        if "patronymic" in request.POST.keys():
            document.patronymic = request.POST.get('patronymic')
        if "first_name" in request.POST.keys():
            document.first_name = request.POST.get('first_name')
        if "last_name" in request.POST.keys():
            document.last_name = request.POST.get('last_name')
        if "series_number" in request.POST.keys():
            document.series_number = request.POST.get("series_number")
        if "birthday" in request.POST.keys():
            document.birthday = datetime.fromtimestamp(int(request.POST.get("birthday")) / 1000.0)
        if "type_doc" in request.POST.keys():
            document.type_doc = request.POST.get("type_doc")
        if "how_get" in request.POST.keys():
            document.how_get = request.POST.get("how_get")
        if "date_get" in request.POST.keys():
            document.date_get = datetime.fromtimestamp(int(request.POST.get("date_get")) / 1000.0)
        if "photo" in request.FILES:
            document.first_scan = request.FILES.get("photo")
        document.save()
        return Response(status=200, data={"ok": "ok"})


class GetAirport(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # import json
        # import pandas as pd
        # import numpy as np
        # import io
        # import requests as r
        # from django.core.files.images import ImageFile
        # df = pd.read_excel("аэропорты.xls")
        # with open("airports.json") as f:
        #     data = json.load(f)
        # freq = dict()
        # for i in data["data"]["airports"]:
        #     arr = np.array(df[df["Код"] == i["code_iata"]])
        #     if arr.shape == (1, 3) and not Airport.objects.filter(iata=i["code_iata"]):
        #         response = r.get(i["photo_path"])
        #         city = City.objects.filter(name=arr[0][2]).first()
        #         image = ImageFile(io.BytesIO(response.content), name=f'{arr[0][0]}.jpg')
        #         Airport.objects.create(iata=arr[0][1],
        #                                name=arr[0][0],
        #                                image=image,
        #                                city=city,
        #                                lat=i["latitude"],
        #                                lon=i["longitude"]
        #                                )
        # print("End!!!")
        air = AirportSerializers(Airport.objects.all().order_by("name"), many=True)
        return Response(status=200, data=air.data)


class GetTerminals(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ls = LuggageStorage.objects.filter(airport__iata=request.GET.get("iata"), active=True)
        term = LGSerializer(ls, many=True).data
        for i in term:
            i.update(LSInfoSerializers(LuggageStorageInfo.objects.get(ls_id=i.get("id"))).data)
            i.update([("luggage",
                       Luggage.objects.filter(user=request.user, date_send__isnull=False, date_take__isnull=True,
                                              ls_id=i.get("id")).count())])
        return Response(status=200, data=term)


class GetClosedTerminals(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ls = LuggageStorage.objects.filter(airport__iata=request.GET.get("iata"), active=True)
        term = LGSerializer(ls, many=True).data
        for i in term:
            i.update(LSInfoSerializers(LuggageStorageInfo.objects.get(ls_id=i.get("id"))).data)
            i.update([("luggage",
                       Luggage.objects.filter(user=request.user, date_send__isnull=False, date_take__isnull=False,
                                              ls_id=i.get("id")).count())])
        return Response(status=200, data=term)


class GetTerminal(APIView):

    def get(self, request, pk):
        ls = LGSerializer(LuggageStorage.objects.get(id=pk), many=False).data
        ls.update(PriceLSSerializers(LSPrice.objects.filter(ls_id=pk).order_by("date").last()).data)
        return Response(status=200, data=ls)


class AddLuggage(APIView):
    permission_classes = [IsAuthenticated]

    parser_classes = (FormParser, MultiPartParser)

    def get(self, request):
        if "iata" in request.GET.keys():
            airport = Airport.objects.get(iata=request.GET.get("iata"))
        else:
            airport = Airport.objects.get(name=request.GET.get("airport"))
        term = LGSerializer(LuggageStorage.objects.filter(airport=airport, active=True), many=True).data
        kind = KindLuggageSerializers(KindLuggage.objects.all(), many=True).data
        for i in term:
            i.update(LSInfoSerializers(LuggageStorageInfo.objects.get(ls_id=i.get("id"))).data)
            i.update(PriceLSSerializers(LSPrice.objects.filter(ls_id=i.get("id")).order_by("date").last()).data)
        return Response(status=200, data={"kind": kind, "ls": term})

    def post(self, request):
        price_list = LSPrice.objects.filter(ls_id=request.POST.get("ls")).order_by("date").last()
        luggage = Luggage.objects.create(user=request.user,
                                         ls_id=request.POST.get("ls"),
                                         kind_luggage_id=request.POST.get("kind"),
                                         price_storage=price_list.price_storage,
                                         price_per_day=price_list.extension_storage,
                                         sale_storage=int(request.POST.get("sale")),
                                         date_create=datetime.now(),
                                         total_price=price_list.price_storage - int(request.POST.get("sale")))
        for i in request.FILES:
            PhotoLuggage.objects.create(luggage=luggage, photo=request.FILES[i])
        partner = ParthnerSerializers(
            LSSettings.objects.filter(ls_id=request.POST.get("ls")).order_by("date").last().partner).data
        luggage = LuggageSerializers(luggage).data
        ls = LGSerializer(LuggageStorage.objects.get(id=request.POST.get("ls"))).data
        return Response(status=200, data={"status": True, "lg": luggage, "partner": partner, "ls": ls})


class GetOrders(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        luggage = Luggage.objects.filter(ls_id=pk, user=request.user, date_send__isnull=False, date_take__isnull=True)
        orders = LuggageSerializers(luggage, many=True).data
        return Response(status=200, data=orders)


class GetCloseOrders(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        luggage = Luggage.objects.filter(ls_id=pk, user=request.user, date_send__isnull=False, date_take__isnull=False)
        orders = LuggageSerializers(luggage, many=True).data
        return Response(status=200, data=orders)


class SendLuggage(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        luggage = Luggage.objects.get(id=pk)
        luggage.date_send = datetime.now()
        luggage.save()
        return Response(status=200, data={"status": True})


class Card(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pass

    def post(self, request):
        pass


class TakeLuggage(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        luggage = Luggage.objects.get(id=pk)
        luggage.date_take = datetime.now()
        luggage.save()
        return Response(status=200, data={"status": True})

    def post(self, request, pk):
        print(request.data)
        luggage = Luggage.objects.get(id=pk)
        luggage.day_storage = int(request.data.get("day_len"))
        luggage.price_day_storage = int(request.data.get("price_for_storage"))
        if not request.data.get("sale_day_storage") is None:
            luggage.sale_day_storage = int(request.data.get("sale_day_storage"))
            luggage.total_price += int(request.data.get("price_for_storage")) - int(
                request.data.get("sale_day_storage"))
        else:
            luggage.sale_day_storage = 0
            luggage.total_price += int(request.data.get("price_for_storage"))
        luggage.save()
        return Response(status=200, data={"ok": "ok"})


class SendEmail(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        hash = request.user.password.replace(r"[^A-Za-z]", "").split('$')[2]
        mail = EmailMessage("Подтверждение почты",
                            f"Для подтверждения почты в приложении Bag24 перейдите по ссылке ниже:\nhttp://{request.get_host()}/mobile/verify_email/{request.user.id}_{hash}",
                            settings.EMAIL_HOST_USER, [request.data.get("email")])
        mail.send()
        request.user.email = request.data.get("email")
        request.user.save()
        return Response(status=200, data={"status": True})


class VerifyEmail(APIView):

    def get(self, request, hash):
        id = hash.split("_")[0]
        user = User.objects.get(id=id)
        user.verify_email = True
        user.save()
        return Response(status=200)


class GetProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        userSer = UserSerializers(request.user).data
        return Response(status=200, data=userSer)


class AddMileOnAir(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        qr, _ = MileOneAir.objects.get_or_create(user=request.user)
        qr.qr = request.data.get("qr")
        qr.save()
        return Response(status=200, data={"ok": "ok"})


class RemoveMileOnAir(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qr, _ = MileOneAir.objects.get_or_create(user=request.user)
        qr.qr = None
        qr.save()
        return Response(status=200, data={"ok": "ok"})
