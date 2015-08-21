from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory

from .models import Game, Player


class GameFactory(DjangoModelFactory):
    class Meta:
        model = Game


class PlayerFactory(DjangoModelFactory):
    class Meta:
        model = Player

    username = Sequence(lambda n: "Agent %03d" % n)
    game = SubFactory(GameFactory)
