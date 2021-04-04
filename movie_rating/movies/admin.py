from django.contrib import admin

from .models import Movie,MovieInfo,User_Rating
# Register your models here.

admin.site.register(Movie)

admin.site.register(MovieInfo)
admin.site.register(User_Rating)


