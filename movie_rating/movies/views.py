from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.

@login_required
def home(request):
    pass

class SearchView(LoginRequiredMixin, TemplateView):
    pass

class SearchResultsView(LoginRequiredMixin, ListView):
    pass