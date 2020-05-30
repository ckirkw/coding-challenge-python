from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def login0(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if (user is not None):
            login(request, user)
            return redirect('list')
        
        else:
            return redirect('login')

def logout0(request):
    logout(request)
    return redirect('login')