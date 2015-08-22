from django.shortcuts import render
from django.views.generic import ListView

from .models import Player


class PlayerListView(ListView):
    model = Player
