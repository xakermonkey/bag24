from django.shortcuts import render

# Create your views here.


def AdminLogin(request):
    return render(request, 'bag_admin/login.html')


def AdminPanel(request):
    return render(request, 'bag_admin/admin_panel.html')

def AdminLuggageStorage(request):
    return render(request, 'bag_admin/admin_kh.html')


def AdminWorkerDetail(request, pk):
    return render(request, 'bag_admin/admin_worker_detail.html')


def AdminThingCell(request):
    return render(request, 'bag_admin/admin_thing.html')