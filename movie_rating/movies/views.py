from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.
from .models import *

def home_view(request):

    print("-"*100)
    print("a\na\na\na\n")

    ### TO SEARCH:
    ### ----------

    input_x = "animation"
    # check if text is arabic or eng {TODO}
    # for eng
    x = Movie.objects.filter(
        actors_name_eg__icontains= input_x
        ) | Movie.objects.filter(
        name_eg__icontains= input_x
        ) |  Movie.objects.filter(
        genres_name_eg__icontains= input_x
        )

    # for arabic 

    # without list(x) the query automatically limit 21 
    # x is a list of dict
    x = list(x.values())
    print(x)
    print("a\na\n")
    ###___________________________________

    ### SELECTING A MOIVE TO SEE ITS INFO:
    ### ----------------------------------

    # to select A movie to get all its info url : moive/{INPUT}
    input_y = 1

    # wanted to use get bec i thought it was faster 
    # but tunrs out get is basicy filter but retuns exactly one record.
    # will use filters as queryset object is easier to deal with 

    y1 = Movie.objects.filter(pk=input_y).values()[:1] 
    y1 = list(y1.values())
    y2 = MovieInfo.objects.filter(pk=input_y).values()[:1] 
    y2 = list(y2.values())

    # (change it if u want)
    #y = MovieInfo.objects.values_list().get(pk=input_y)

    #_____________________________________

    ### SELECT ACTORS:
    ### --------------
    # actors urls
    z = MovieInfo.objects.get(pk=input_y).actors_urls.all()
    z = list(z.values())

    print(z)

    
    return HttpResponse()
  