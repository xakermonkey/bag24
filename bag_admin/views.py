from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse, HttpResponseForbidden
from lostitems.models import *
from bag_admin.models import *


# Create your views here.


def AdminLogin(request):
    return render(request, 'bag_admin/login.html')

def AdminLogout(request):
    logout(request)
    return render(request, 'bag_admin/login.html')


def AdminPanel(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    if request.user.status != 'adm':
        return HttpResponseForbidden('<h1>Недостаточно прав</h1>')
    info = WorkerInfo.objects.all()
    air = Airport.objects.all()
    return render(request, 'bag_admin/admin_panel.html', {'workerinfo': info, 'airport': air})


def AdminLuggageStorage(request):
    return render(request, 'bag_admin/admin_kh.html')


def AdminWorkerDetail(request, pk):
    return render(request, 'bag_admin/admin_worker_detail.html')


def AdminThingCell(request):
    return render(request, 'bag_admin/admin_thing.html')


def adminRegister(request):
    username = request.POST.get('login')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if not user:
        return JsonResponse({'status': False})
    if user.status != 'adm':
        return JsonResponse({'status': False})
    login(request, user)
    return JsonResponse({'status': True})
