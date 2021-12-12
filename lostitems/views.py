from django.shortcuts import render

def loginUserStart(request):
    return render(request, 'login_start.html')

def loginUser(request):
    return render(request, 'login.html')

def logoutUser(request):
    pass

def registrationUser(request):
    pass

def fillProfile(request):
    return render(request, 'fill_profile.html')

def mainMenu(request):
    return render(request, 'main_menu.html')

def deliveryInfo(request):
    return render(request, 'delivery_info.html')