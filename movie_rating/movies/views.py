from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.

@login_required
def home(request):
    if request.method == 'POST':
        current_user = request.user
        user_ratings_movies = [rating.movie for rating in current_user.user_rating_set.all()]
        
        # Check if the user re-rated a movie
        for movie in user_ratings_movies:
            if movie.name_eg in request.POST:
                User_Rating.objects.get(user=current_user, movie=movie).delete()
        
        # Save the ratings to the database
        for data in request.POST:
            if request.POST.get(data) == 0: # User un-rated a movie
                continue
            
            movie = Movie.objects.get(name_eg=data)
            rating = User_Rating(user=current_user, movie=movie, rating=request.POST.get(data))
            rating.save()
        
        messages.success(request, 'Your ratings have been saved!') 
        return redirect('home')
        
    else:
        movies_info = MovieInfo.objects.all().order_by('-date')[:20]
        latest_movies = [info.movie for info in movies_info]
        popular_movies = Movie.objects.all().order_by('-final_rating')
        
        context = {
            'latest_movies': latest_movies,
            'popular_movies': popular_movies
        }
        
        return render(request, 'movies/home.html', context)

class SearchView(LoginRequiredMixin, TemplateView):
    template_name = 'movies/search.html'

class SearchResultsView(LoginRequiredMixin, ListView):
    def post(self, request, *args, **kwargs):
        pass
    
    def get(self, request, *args, **kwargs):
        pass