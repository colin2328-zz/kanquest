from django.forms import ModelForm

from game.models import Player


class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = ['username', 'password', 'email', 'race_choice']
