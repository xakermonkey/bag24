from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
import datetime
from lostitems.models import *
from bag_admin.models import *
from .forms import *


# Create your views here.


def StaffLogin(request):
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            return JsonResponse({'status': False})
        if user.status == "us":
            return JsonResponse({'status': False})
        login(request, user)
        return JsonResponse({'status': True})
    else:
        return render(request, 'staff_lostitem/login.html')


def staffPanel(request):
    if not request.user.is_authenticated:
        return HttpResponseNotFound('Необходимо авторзироваться')
    info = WorkerInfo.objects.get(user=request.user)
    lg = U_LS.objects.filter(user=request.user).first()
    dt = TimeForUnclaimed.objects.filter(airport=lg.ls.airport).order_by('delta_time').last()
    lost = LostItem.objects.filter(kh=lg.ls, status=False, demanded=False)
    workers = [[ind, i.user] for ind, i in enumerate(U_LS.objects.filter(ls=lg.ls))]
    aiport = list()
    for ind, i in enumerate(Airport.objects.all()):
        aiport.append([ind, i])
    colors = Color.objects.all()
    return render(request, 'staff_lostitem/panel.html',
                  {'info': info, 'colors': colors, 'airport': aiport, 'workers': workers, 'lost_item': lost,
                   'lg': lg.ls, 'now': datetime.datetime.now()})


def staffRefound(request):
    if not request.user.is_authenticated:
        return HttpResponseNotFound('Необходимо авторзироваться')
    info = WorkerInfo.objects.get(user=request.user)
    lg = U_LS.objects.filter(user=request.user).first()
    refund = RefundItem.objects.filter(lost_item__kh=lg.ls)
    workers = [[ind, i.user] for ind, i in enumerate(U_LS.objects.filter(ls=lg.ls), start=1)]
    airport = [[ind, i] for ind, i in enumerate(Airport.objects.all())]
    colors = Color.objects.all()
    return render(request, 'staff_lostitem/panel_refound.html',
                  {'info': info, 'workers': workers, 'airport': airport, "refund": refund, 'colors': colors})


def staffRefoundSAB(request):
    if not request.user.is_authenticated:
        return HttpResponseNotFound('Необходимо авторзироваться')
    info = WorkerInfo.objects.get(user=request.user)
    colors = Color.objects.all()
    return render(request, 'staff_lostitem/panel_refound_sab.html', {'info': info, 'colors': colors})


def addLostItems(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseNotFound('Необходимо авторзироваться')
    itemSAB = SABItem.objects.get(pk=pk)
    photos = Photos.objects.filter(item=itemSAB)
    workinfo = WorkerInfo.objects.get(user=itemSAB.user)
    staff = WorkerInfo.objects.get(user=request.user)
    lg = [[ind, i.ls] for ind, i in enumerate(U_LS.objects.filter(user=request.user))]
    category = [[ind, i] for ind, i in enumerate(Category.objects.all())]
    colors = Color.objects.all()
    now = datetime.datetime.now()
    return render(request, 'staff_lostitem/add_lostitem.html',
                  {'item': itemSAB, 'photos': photos, 'workerinfo': workinfo, 'colors': colors, 'now': now,
                   'category': category, 'kh': lg, 'staff': staff})


def refoundLostItem(request, pk):
    lostitem = LostItem.objects.get(id=pk)
    info = WorkerInfo.objects.get(user=request.user)
    date = datetime.datetime.today()
    return render(request, 'staff_lostitem/refound_lostitem.html', {'lost': lostitem, 'info': info, 'today': date})


def saveRefundItem(request, pk):
    lost = LostItem.objects.get(id=pk)
    date_get = request.POST.get('date_get').split('-')
    birthday = request.POST.get('birthday').split('-')
    item = RefoundItem(
        data={'lost_item': lost,
              'user': request.user,
              'refund_date': datetime.datetime.now(),
              'fio': request.POST.get('fio'),
              'series_number': request.POST.get('series_number'),
              'date_get': datetime.datetime(year=int(date_get[0]),
                                            month=int(date_get[1]),
                                            day=int(date_get[2])),
              'how_get': request.POST.get('how_get'),
              'birthday': datetime.datetime(year=int(birthday[0]),
                                            month=int(birthday[1]),
                                            day=int(birthday[2]))
              })
    if item.is_valid():
        item.save()
        lost.status = True
        lost.save()
        return JsonResponse(status=200, data={'status': True})


def refoundUploadFile(request, pk):
    item = RefundItem.objects.filter(lost_item=pk).first()
    if item:
        if 'first' in request.FILES:
            item.first_scan = request.FILES['first']
        if 'second' in request.FILES:
            item.second_scan = request.FILES['second']
        if 'firstDoc' in request.FILES:
            item.scan_refund = request.FILES['firstDoc']
        if 'secondDoc' in request.FILES:
            item.scan_receipt = request.FILES['secondDoc']
        item.save()
        return JsonResponse(status=200, data={'status': True})
    return JsonResponse(status=400, data={'status': False})


def get_kind(request):
    cat_id = int(request.POST.get('category'))
    kind = Kind.objects.filter(category=Category.objects.get(id=cat_id))
    kind_json = list()
    for i in kind:
        kind_json.append({
            'id': i.id,
            'name': i.name
        })
    return JsonResponse({'status': True, 'kind': kind_json})


def save_lostitem(request, pk):
    sab_item = SABItem.objects.get(id=pk)
    sab_item.comment = request.POST.get('comment_sab')
    lost_item = LostItemForm(data={'sab_item': sab_item,
                                   'user': request.user,
                                   'date': datetime.datetime.now(),
                                   'comment': request.POST.get('comment'),
                                   'color': int(request.POST.get('color')),
                                   'kh': int(request.POST.get('kh')),
                                   'tag': request.POST.get('tag'),
                                   'category': int(request.POST.get('category')),
                                   'kind': int(request.POST.get('kind'))
                                   })
    if lost_item.is_valid():
        sab_item.status = True
        sab_item.save()
        lost_item.save()
        return JsonResponse(status=200, data={'status': True})
    else:
        return JsonResponse(status=400, data={"status": False})
