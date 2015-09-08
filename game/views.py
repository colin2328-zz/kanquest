from django.shortcuts import render
from django.views.generic import ListView

from .models import Player


class PlayerListView(ListView):
    model = Player

    def get(self, request):
        return super(PlayerListView, self).get(request)
