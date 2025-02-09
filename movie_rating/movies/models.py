from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

# Create your models here.

class Movie(models.Model):

	name_eg = models.CharField(max_length=200,blank=True,null=True)
	name_ar = models.CharField(max_length=200,blank=True,null=True)

	actors_name_eg = models.CharField(max_length=200,blank=True,null=True)
	actors_name_ar = models.CharField(max_length=200,blank=True,null=True)

	genres_name_eg = models.CharField(max_length=200,blank=True,null=True)
	genres_name_ar = models.CharField(max_length=200,blank=True,null=True)

	poster_url = models.URLField(blank=True, null=True)

	date = models.IntegerField(default=1900, validators=[MinValueValidator(1900), MaxValueValidator(3000)])
	
	is_english = models.BooleanField(default=True)

	# rating calculated using imdb formula
	final_rating = models.FloatField(default=0,validators=[MinValueValidator(0), MaxValueValidator(5)])

	def __str__(self):
		return f"{self.name_eg} | {self.name_ar}"

class MovieInfo(models.Model):

	movie = models.OneToOneField(Movie, primary_key=True, on_delete=models.CASCADE)

	
	country = models.CharField(max_length=40,blank=True,null=True)

	# gatherd from egybest
	rating = models.FloatField(default=0,validators=[MinValueValidator(0), MaxValueValidator(5)])
	rating_count = models.IntegerField(default=0)

	plot = models.TextField(blank=True,null=True)

	actors_urls = models.TextField(blank=True, null=True)

	def __str__(self):
		return f"Info of: {self.movie.name_eg} | {self.movie.name_ar}"

class User_Rating(models.Model):
    #user.user_rating_set
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    
    # rating out of 5
    rating = models.FloatField(default=0,validators=[MinValueValidator(0), MaxValueValidator(5)])
    
    def __str__(self):
        return f"{self.user.username} | {self.movie.name_eg} | {self.rating}"
    
    class Meta():
        unique_together = ("user", "movie")
