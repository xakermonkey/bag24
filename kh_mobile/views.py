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


# Create your views here.


def send_code(number):
    var_code, _ = VerifyCode.objects.get_or_create(phone=number)
    code = random.randint(999, 9999)
    var_code.code = code
    var_code.save()


def create_password():
    import string
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(16))
    return result_str


class apiLogin(APIView):
    def post(self, request):
        if 'number' in request.data:
            user = User.objects.filter(phone=request.data.get('number')).first()
            if not user:
                user = User.objects.create_user(username=request.data.get("number"), password=create_password(),
                                                phone=request.data.get("number"))
            send_code(number=user.phone)
            return Response(status=200, data={"status": True})


class verifyCode(APIView):
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
            return Response(status=200, data={"status": True, "token": token.key, "doc": docSer})


class getCodeCity(APIView):

    def get(self, request):
        code = CityCodeSerializers(CodeCity.objects.all(), many=True)
        return Response(status=200, data=code.data)


class createDocument(APIView):
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


class getAirport(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        air = AirportSerializers(Airport.objects.all(), many=True)
        return Response(status=200, data=air.data)


class getTerminals(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ls = LuggageStorage.objects.filter(airport__iata=request.GET.get("iata"))
        term = LGSerializer(ls, many=True).data
        for i in term:
            i.update(LSInfoSerializers(LuggageStorageInfo.objects.get(ls_id=i.get("id"))).data)
            i.update([("luggage",
                       Luggage.objects.filter(user=request.user, date_send__isnull=False, date_take__isnull=True,
                                              ls_id=i.get("id")).count())])
        return Response(status=200, data=term)


class getTerminal(APIView):

    def get(self, request, pk):
        ls = LGSerializer(LuggageStorage.objects.get(id=pk), many=False).data
        ls.update(PriceLSSerializers(LSPrice.objects.filter(ls_id=pk).order_by("date").last()).data)
        return Response(status=200, data=ls)


class addLuggage(APIView):
    permission_classes = [IsAuthenticated]

    parser_classes = (FormParser, MultiPartParser)

    def get(self, request):
        airport = Airport.objects.get(iata=request.GET.get("iata"))
        term = LGSerializer(LuggageStorage.objects.filter(airport=airport), many=True).data
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
        return Response(status=200, data={"status": True, "id": luggage.id})


class getOrders(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        luggage = Luggage.objects.filter(ls_id=pk, user=request.user, date_send__isnull=False, date_take__isnull=True)
        orders = LuggageSerializers(luggage, many=True).data
        return Response(status=200, data=orders)


class sendLuggage(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        luggage = Luggage.objects.get(id=pk)
        luggage.date_send = datetime.now()
        luggage.save()
        return Response(status=200, data={"status": True})


class takeLuggage(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        for i in request.GET.get("luggage[]"):
            luggage = Luggage.objects.get(id=int(i))
            luggage.date_take = datetime.now()
            luggage.save()
        return Response(status=200, data={"status": True})



class sendEmail(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        hash = request.user.password.replace(r"[^A-Za-z]", "").split('$')[2]
        mail = EmailMessage("Подтверждение почты", f"Для подтверждения почты в приложении Bag24 перейдите по ссылке ниже:\nhttp://{request.get_host()}/mobile/verify_email/{request.user.id}_{hash}",
                            settings.EMAIL_HOST_USER, [request.data.get("email")])
        mail.send()
        request.user.email = request.data.get("email")
        request.user.save()
        return Response(status=200, data={"status": True})


class verifyEmail(APIView):



    def get(self, request, hash):
        id = hash.split("_")[0]
        user = User.objects.get(id=id)
        user.verify_email = True
        user.save()
        return Response(status=200)

class getProfile(APIView):

    permission_classes = [IsAuthenticated]


    def get(self, request):
        userSer = UserSerializers(request.user).data
        return Response(status=200, data=userSer)
