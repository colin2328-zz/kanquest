# from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Player


class PlayerListView(ListView):
    model = Player


class PlayerDetailView(DetailView):
    model = Player
