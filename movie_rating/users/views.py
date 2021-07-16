from django.shortcuts import render, redirect
from .forms import UserForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from movie_rating.models import Recommendation_Fun
from movie_rating.models import ArabicRecommendation_Fun
from movies.models import Movie

# Create your views here.


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
                return redirect('notepage')
            else:  # something went wrong
                context = {'username': username}
                messages.warning(request, 'Username/Password is incorrect')

        return render(request, 'users/login.html', context)


@login_required
def notepage(request):
    return render(request, 'users/notepage.html')


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
    backup_user = {
        "username": current_user.username,
        "email": current_user.email
    }

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=current_user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=current_user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            if request.POST.get('password'):
                current_user.set_password(request.POST.get('password'))
                current_user.save()
            p_form.save()
            # comment it for now
            messages.success(request, f'Profile updated successfully!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=current_user)
        p_form = ProfileUpdateForm(instance=current_user.profile)

    user_ratings = current_user.user_rating_set.all()
    user_rated_movies = [rating.movie for rating in user_ratings]
    collaborative_movies = {}

    for movie in user_rated_movies:
        if movie.is_english:
            collab_movies = Recommendation_Fun.recommend_fun(movie.id)["id"][1:]
            for mov in collab_movies:
                if mov not in collaborative_movies:
                    collaborative_movies[mov] = 1
                else:
                    collaborative_movies[mov] += 1
        else:
            collab_movies = ArabicRecommendation_Fun.get_movie_recommendation(movie.name_eg)[
                "Title"]
            for mov in collab_movies:
                if mov not in collaborative_movies:
                    collaborative_movies[mov] = 1
                else:
                    collaborative_movies[mov] += 1

    total_collaborative_movies = {}

    for i, v in collaborative_movies.items():
        if type(i) is str:
            try:
                mv = Movie.objects.get(name_eg=i)
                if mv not in user_rated_movies:
                    total_collaborative_movies[mv] = v
            except Movie.DoesNotExist:
                pass
        else:
            try:
                mv = Movie.objects.get(id=i)
                if mv not in user_rated_movies:
                    total_collaborative_movies[mv] = v
            except Movie.DoesNotExist:
                pass

    total_collaborative_movies = sorted(total_collaborative_movies.items(), key = lambda kv: (kv[1], kv[0].final_rating))[::-1][:20]
    total_collaborative_movies = [tup[0] for tup in total_collaborative_movies]
    
    context = {
        'USER': backup_user,
        'u_form': u_form,
        'p_form': p_form,
        'user_ratings': user_ratings,
        'collaborative_movies': total_collaborative_movies
    }

    return render(request, 'users/profile.html', context)
