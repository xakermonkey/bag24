from django.shortcuts import render, redirect
import random
from .models import *
from datetime import datetime
from django.http import JsonResponse, Http404
from django.contrib.auth import login, logout, authenticate


def loginUserStart(request):
    return render(request, 'login_start.html')


def loginUser(request):
    username = request.POST.get('login')
    password = request.POST.get('pswd')
    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({'status': False})
    login(request, user)
    if user.first_join:
        url = 'fillprofile'
    else:
        url = 'mainmenu'
    return JsonResponse({'status': True,
                         'path': url})


def logoutUser(request):
    logout(request)
    return redirect('login_phone')


def registrationUser(request):
    username = request.POST.get('login')
    password = request.POST.get('pswd')
    user = User.objects.create_user(username=username, password=password)
    login(request, user)
    return JsonResponse({'status': True})


def fillProfile(request):
    doc, _ = Document.objects.get_or_create(user=request.user)
    list_address, _ = AddressList.objects.get_or_create(user=request.user)
    card = MileOneAir.objects.filter(user=request.user).first()
    return render(request, 'fill_profile.html', {'doc': doc, 'list': list_address, 'card': card})


def mainMenu(request):
    return render(request, 'main_menu.html')


def deliveryInfo(request):
    return render(request, 'delivery_info.html')


def setNumber(request):
    number = str(request.POST.get('number'))
    if number.startswith('8'):
        number = '+7' + number[1:]
    elif number.startswith('7'):
        number = '+' + number
    elif number.startswith('9'):
        number = "+7" + number
    code = random.randint(999, 9999)
    ver, _ = VerifyCode.objects.get_or_create(phone=number)
    ver.code = code
    ver.save()
    return JsonResponse({'status': True, 'number': number})


def setNumberInFill(request):
    number = str(request.POST.get('number'))
    if number.startswith('8'):
        number = '+7' + number[1:]
    elif number.startswith('7'):
        number = '+' + number
    elif number.startswith('9'):
        number = "+7" + number
    if User.objects.filter(phone=number).first():
        return JsonResponse({'status': False,
                             'msg': "Этот номер телефона уже занят!"})
    code = random.randint(999, 9999)
    ver, _ = VerifyCode.objects.get_or_create(phone=number)
    ver.code = code
    ver.save()
    return JsonResponse({'status': True, 'number': number})


def setNumberInCard(request):
    number = str(request.POST.get('number'))
    if number.startswith('8'):
        number = '+7' + number[1:]
    elif number.startswith('7'):
        number = '+' + number
    elif number.startswith('9'):
        number = "+7" + number
    if MileOneAir.objects.filter(phone=number).first():
        return JsonResponse({'status': False,
                             'msg': "Этот номер телефона уже занят!"})
    code = random.randint(999, 9999)
    ver, _ = VerifyCode.objects.get_or_create(phone=number)
    ver.code = code
    ver.save()
    return JsonResponse({'status': True, 'number': number})


def ValidCodeInCard(request):
    number = str(request.POST.get('number'))
    if number.startswith('8'):
        number = '+7' + number[1:]
    elif number.startswith('7'):
        number = '+' + number
    elif number.startswith('9'):
        number = "+7" + number
    code = str(request.POST.get('code'))
    ver = VerifyCode.objects.filter(phone=number).first()
    if not ver:
        return JsonResponse({'status': False,
                             'msg': "Такого телефона не существует!"})
    if code != str(ver.code):
        return JsonResponse({'status': False,
                             'msg': "Неверный код!"})
    if code == str(ver.code):
        MileOneAir.objects.create(user=request.user, phone=number).save()
        return JsonResponse({'status': True})


def ValidCodeInFill(request):
    number = str(request.POST.get('number'))
    if number.startswith('8'):
        number = '+7' + number[1:]
    elif number.startswith('7'):
        number = '+' + number
    elif number.startswith('9'):
        number = "+7" + number
    code = str(request.POST.get('code'))
    ver = VerifyCode.objects.filter(phone=number).first()
    if not ver:
        return JsonResponse({'status': False,
                             'msg': "Такого телефона не существует!"})
    if code != str(ver.code):
        return JsonResponse({'status': False,
                             'msg': "Неверный код!"})
    if code == str(ver.code):
        user = request.user
        user.phone = number
        user.save()
        return JsonResponse({'status': True})


def ValidCode(request):
    number = str(request.POST.get('number'))
    if number.startswith('8'):
        number = '+7' + number[1:]
    elif number.startswith('7'):
        number = '+' + number
    elif number.startswith('9'):
        number = "+7" + number
    code = str(request.POST.get('code'))
    ver = VerifyCode.objects.filter(phone=number).first()
    if not ver:
        return JsonResponse({'status': False,
                             'msg': "Такого телефона не существует!"})
    if code != str(ver.code):
        return JsonResponse({'status': False,
                             'msg': "Неверный код!"})
    if code == str(ver.code):
        user = User.objects.filter(phone=number).first()
        if not user:
            user = User.objects.create_user('User', '1234567890', phone=number)
            user.username = user.username + str(user.id)
            user.save()
            url = 'fillprofile'
        elif user.first_join:
            url = 'fillprofile'
        else:
            url = 'mainmenu'
        login(request, user)
        return JsonResponse({'status': True,
                             'path': url})


def findUser(request):
    username = request.POST.get('login')
    user = User.objects.filter(username=username).first()
    if not user:
        return JsonResponse({'status': False})
    return JsonResponse({'status': True})


def changeLK(request):
    email = request.POST.get('email')
    user = request.user
    user.email = email
    if 'username' in request.POST:
        username = request.POST.get('username')
        user.username = username
    if 'pswd' in request.POST:
        pswd = request.POST.get('pswd')
        user.set_password(pswd)
    user.save()
    login(request, user)
    return JsonResponse({'status': True})


def isPhone(request):
    if request.user.phone:
        return JsonResponse({'status': True})
    return JsonResponse({'status': False})


def changeDoc(request):
    date_get = request.POST.get('date_get').split('-')
    birthday = request.POST.get('birthday').split('-')
    doc = Document.objects.get(user=request.user)
    doc.fio = request.POST.get('fio')
    doc.series_number = request.POST.get('series')
    doc.date_get = datetime(year=int(date_get[0]),
                            month=int(date_get[1]),
                            day=int(date_get[2]))
    doc.how_get = request.POST.get('how_get')
    doc.birthday = datetime(year=int(birthday[0]),
                            month=int(birthday[1]),
                            day=int(birthday[2]))
    doc.save()
    return JsonResponse({'status': True})


def addAddress(request):
    address = Address.objects.create(name=request.POST.get('name'),
                                     address=request.POST.get('address'),
                                     entrance=request.POST.get('entrance'),
                                     floor=request.POST.get('floor'),
                                     code=request.POST.get('code'),
                                     apartment=request.POST.get('apartment'))
    address.save()
    list = AddressList.objects.get(user=request.user)
    list.addresses.add(address)
    list.save()
    return JsonResponse({'status': True,
                         "id": address.id,
                         "name": request.POST.get('name'),
                         "address": request.POST.get('address'),
                         "entrance": request.POST.get('entrance'),
                         "floor": request.POST.get('floor'),
                         "code": request.POST.get('code'),
                         "apartment": request.POST.get('apartment')
                         })


def fileUpload(request):
    doc = Document.objects.get(user=request.user)
    if 'first' in request.FILES:
        doc.first_scan = request.FILES['first']
        doc.save()
    else:
        doc.second_scan = request.FILES['second']
        doc.save()
    return JsonResponse(status=200)


def fileRemove(request):
    doc = Document.objects.get(user=request.user)
    if request.POST.get('scan') == 'first':
        doc.first_scan.delete()
        doc.save()
    else:
        doc.second_scan.delete()
        doc.save()
    return JsonResponse(status=200, data={'status': True})


def removeAddress(request):
    id = request.POST.get('id')
    adrlist = AddressList.objects.get(user=request.user)
    adr = Address.objects.get(pk=id)
    adrlist.addresses.remove(adr)
    adrlist.save()
    count = adrlist.addresses.count()
    adr.delete()
    return JsonResponse({'status': True, 'count': count})
