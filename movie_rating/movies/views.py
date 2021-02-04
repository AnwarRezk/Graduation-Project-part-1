from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import *

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
            if request.POST.get(data) == 0: # An un-rated movie
                continue
            
            movie = Movie.objects.get(name_eg=data)
            rating = User_Rating(user=current_user, movie=movie, rating=request.POST.get(data))
            rating.save()
        
        messages.success(request, 'Your ratings have been saved!')
        return redirect('home')
        
    else:
        movies_info = MovieInfo.objects.all().order_by('-date')[:20]
        l_m = [info.movie for info in movies_info]
        p_m = list(Movie.objects.all().order_by('-final_rating')[:20])
        
        latest_movies = []
        popular_movies = []
        
        # Remove the duplicates between the latest movies and the rated movies
        for movie in l_m:
            if movie not in user_rated_movies:
                latest_movies.insert(len(latest_movies), movie)
        
        # Remove the duplicates between the popular movies and the latest movies, and the rated movies
        for movie in p_m:
            if (movie not in user_rated_movies) and (movie not in latest_movies):
                popular_movies.insert(len(popular_movies), movie)
        
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
    
    def get_context_data(self,*args, **kwargs):
        current_user = self.request.user
        user_ratings = current_user.user_rating_set.all()
        rated_movies = [rating.movie for rating in user_ratings]
        movies_ratings = [rating.rating for rating in user_ratings]
        context = super(SearchResultsView, self).get_context_data(*args,**kwargs)
        context['rated_movies'] = rated_movies
        context['movies_ratings'] = movies_ratings
        return context
    
    def post(self, request, *args, **kwargs):
        current_user = request.user
        user_rated_movies = [rating.movie for rating in current_user.user_rating_set.all()]
        
        # Check if the user re-rated a movie
        for movie in user_rated_movies:
            if movie.name_eg in request.POST:
                User_Rating.objects.get(user=current_user, movie=movie).delete()
        
        # Save the ratings to the database
        for data in request.POST:
            if request.POST.get(data) == 0: # An un-rated movie
                continue
            
            movie = Movie.objects.get(name_eg=data)
            rating = User_Rating(user=current_user, movie=movie, rating=request.POST.get(data))
            rating.save()
        
        messages.success(request, 'Your ratings have been saved!')
        return redirect('home')
    
    def get_queryset(self):
        q = Q()
        
        for filtr in self.request.GET:
            if filtr == "movie":
                q &= (Q(name_eg__icontains=self.request.GET.get(filtr)) | Q(name_ar__icontains=self.request.GET.get(filtr)))
                
            elif filtr == "actors":
                if ',' in self.request.GET.get(filtr):
                    actors = self.request.GET.get(filtr).split(',')
                    
                else:
                    actors = self.request.GET.get(filtr).split(' ')
                    
                for actor in actors:
                    q &= (Q(actors_name_eg__icontains=actor) | Q(actors_name_ar__icontains=actor))
            
            else:
                if self.request.GET.get(filtr) == "on":
                    q &= Q(genres_name_eg__icontains=filtr)
        
        return Movie.objects.filter(q)