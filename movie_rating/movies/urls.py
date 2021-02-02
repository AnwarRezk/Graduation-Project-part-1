from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('search/results/', views.SearchResultsView.as_view(), name='search_results')
]