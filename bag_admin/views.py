from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse


# Create your views here.


def AdminLogin(request):
    return render(request, 'bag_admin/login.html')

def AdminLogout(request):
    logout(request)
    return render(request, 'bag_admin/login.html')


def AdminPanel(request):
    return render(request, 'bag_admin/admin_panel.html')


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
    if int(user.status) != 2:
        return JsonResponse({'status': False})
    login(request, user)
    return JsonResponse({'status': True})
