from django.shortcuts import render, redirect
from .forms import UserForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required  #if user not logged in, redirect to login page
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

@login_required
def profile(request):
    current_user = request.user
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=current_user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=current_user.profile)
        
        if u_form.is_valid and p_form.is_valid:
            u_form.save()
            print(request.POST)
            if request.POST.get('password'):
                current_user.set_password(request.POST.get('password'))
                current_user.save()
            p_form.save()
            # messages.success(request, f'Profile updated successfully!') #comment it for now
            return redirect('profile')
        
    else:
        u_form = UserUpdateForm(instance=current_user)
        p_form = ProfileUpdateForm(instance=current_user.profile)
    
        context = {
            'u_form': u_form,
            'p_form': p_form
        }
        
        return render(request, 'users/profile.html', context)