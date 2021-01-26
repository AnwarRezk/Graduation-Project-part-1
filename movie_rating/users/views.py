from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')  #if user not logged in, redirect to login page
def home(request):
    return render(request, 'users/home.html')

def LoginPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        context = {}
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else: #something went wrong
                context = {'username': username}
                messages.warning(request,'Username/Password is incorrect')

        return render(request, 'users/login.html', context)

def RegisterPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = UserForm()
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account created for ' + user)
                return redirect("login")
        context = {'form': form}
        return render(request, 'users/register.html', context)

def LogoutUser(request):
    logout(request)
    return redirect('login')