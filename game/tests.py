from django.test import TestCase

from .factories import PlayerFactory


class GameTest(TestCase):

    def test(self):
        player1 = PlayerFactory()
        player2 = PlayerFactory()
        player1.attack(player2)
