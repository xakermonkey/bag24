from django.shortcuts import render

def loginUserStart(request):
    return render(request, 'login_start.html')

def loginUser(request):
    return render(request, 'login.html')

def logoutUser(request):
    pass

def registrationUser(request):
    pass