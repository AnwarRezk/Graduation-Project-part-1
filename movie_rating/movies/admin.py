from django.contrib import admin

from .models import Movie,MovieInfo,User_Rating,Actor
# Register your models here.

admin.site.register(Movie)
admin.site.register(Actor)

admin.site.register(MovieInfo)
admin.site.register(User_Rating)


