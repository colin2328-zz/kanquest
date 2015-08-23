from django.shortcuts import render
from django.views.generic import ListView

from .models import Player


class PlayerListView(ListView):
    model = Player

    def get(self, request):
        print request.user.is_authenticated()
        return super(PlayerListView, self).get(request)
