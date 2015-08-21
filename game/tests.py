from django.test import TestCase

from .factories import GameFactory, PlayerFactory


class GameTest(TestCase):

    def test(self):
        game = GameFactory()
        self.assertEqual(game.turn_count, 0)

        player1 = PlayerFactory()
        player2 = PlayerFactory()
