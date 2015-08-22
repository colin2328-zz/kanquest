from factory import Sequence
from factory.django import DjangoModelFactory

from .models import Player


class PlayerFactory(DjangoModelFactory):
    class Meta:
        model = Player

    username = Sequence(lambda n: "Agent %03d" % n)
