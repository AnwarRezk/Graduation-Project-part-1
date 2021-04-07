from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from .models import *
import json
import random

# Create your views here.

@login_required
def home(request):
    current_user = request.user
    user_ratings = current_user.user_rating_set.all()
    user_rated_movies = [rating.movie for rating in user_ratings]
    
    if request.method == 'POST':
        
        # Check if the user re-rated a movie
        for movie in user_rated_movies:
            if movie.name_eg in request.POST:
                User_Rating.objects.get(user=current_user, movie=movie).delete()
        
        # Save the ratings to the database
        for data in request.POST:
            if data == "csrfmiddlewaretoken":
                continue
            
            if request.POST.get(data) == '0': # An un-rated movie
                continue
            
            movie = Movie.objects.get(name_eg=data)
            rating = User_Rating(user=current_user, movie=movie, rating=float(request.POST.get(data)))
            rating.save()
        
        messages.success(request, 'Your ratings have been saved!')
        return redirect('home')
        
    else:
        movies_info = MovieInfo.objects.all().order_by('-date')[:100]
        l_m = [info.movie for info in movies_info]
        p_m = list(Movie.objects.all().order_by('-final_rating')[:100])
        
        latest_movies = []
        popular_movies = []
        
        # Remove the duplicates between the latest movies and the rated movies
        for movie in l_m:
            if movie not in user_rated_movies:
                latest_movies.insert(len(latest_movies), movie)
            if len(latest_movies) == 20:
                break
        
        # Remove the duplicates between the popular movies and the latest movies, and the rated movies
        for movie in p_m:
            if (movie not in user_rated_movies) and (movie not in latest_movies):
                popular_movies.insert(len(popular_movies), movie)
        
        num_samples = 20
        popular_movies = random.sample(popular_movies, num_samples)
        
        context = {
            'user_ratings': user_ratings,
            'latest_movies': latest_movies,
            'popular_movies': popular_movies
        }
        
        return render(request, 'movies/home.html', context)

class SearchView(LoginRequiredMixin, TemplateView):
    template_name = 'movies/search.html'

class SearchResultsView(LoginRequiredMixin, ListView):
    model = Movie
    template_name = 'movies/search_results.html'
    paginate_by = 12
    
    def post(self, request, *args, **kwargs):
        current_user = request.user
        user_rated_movies = [rating.movie for rating in current_user.user_rating_set.all()]
        
        # Check if the user re-rated a movie
        for movie in user_rated_movies:
            if movie.name_eg in request.POST:
                User_Rating.objects.get(user=current_user, movie=movie).delete()
        
        # Save the ratings to the database
        for data in request.POST:
            
            if data == "csrfmiddlewaretoken":
                continue
            
            if request.POST.get(data) == '0': # An un-rated movie
                continue
            
            movie = Movie.objects.get(name_eg=data)
            rating = User_Rating(user=current_user, movie=movie, rating=float(request.POST.get(data)))
            rating.save()
        
        messages.success(request, 'Your ratings have been saved!')
        return redirect('home')
    
    def get_queryset(self):
        q = Q()
        
        for filtr in self.request.GET:
            if filtr == "movie":
                q &= (Q(name_eg__icontains=self.request.GET.get(filtr)) | Q(name_ar__icontains=self.request.GET.get(filtr)))
                
            elif filtr == "actors":
                if self.request.GET.get(filtr):
                    actors = self.request.GET.get(filtr).split(',')
                        
                    for actor in actors:
                        if actor[0] == ' ':
                            actor = actor[1:]
                        
                        q &= (Q(actors_name_eg__icontains=actor) | Q(actors_name_ar__icontains=actor))
            
            else:
                if filtr == "page":
                    continue
                q &= Q(genres_name_eg__icontains=filtr)
        
        object_list = Movie.objects.filter(q).order_by('-final_rating')
        
        current_user = self.request.user
        user_ratings = current_user.user_rating_set.all()
        rated_movies = [rating.movie for rating in user_ratings]
        movies_ratings = [rating.rating for rating in user_ratings]
        search_results = []
        
        for movie in object_list:
            if movie in rated_movies:
                rating = movies_ratings[rated_movies.index(movie)]

            else:
                rating = 0
                
            search_results.insert(len(search_results), [movie, rating])
            
        return search_results
    
@login_required
def movie_details(request, pk):
    current_user = request.user
    user_ratings = current_user.user_rating_set.all()
    user_rated_movies = [rating.movie for rating in user_ratings]
    movie = get_object_or_404(Movie, pk=pk)
    
    if movie in user_rated_movies:
        movie_is_rated = True
    
    else:
        movie_is_rated = False
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        
        # Check if the user re-rated a movie
        if movie_is_rated:
            User_Rating.objects.get(user=current_user, movie=movie).delete()
        
        # Save the rating to the database
        if json.loads(request.body)['rating'] != '0':
            rating = User_Rating(user=current_user, movie=movie, rating=float(json.loads(request.body)['rating']))
            rating.save()
        
        messages.success(request, 'Your rating has been saved!')
        return JsonResponse({"status": "OK"})
        # return redirect('movie-details', pk=pk)
        
    else:
        if movie_is_rated:
            rating = user_ratings[user_rated_movies.index(movie)].rating
        else:
            rating = 0
            
        context = {
            "movie": movie,
            "rating": rating
        }
        
        return render(request, 'movies/movie_details.html', context)