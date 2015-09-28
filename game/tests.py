from django.test import TestCase

from .factories import PlayerFactory
from .exceptions import AttackFailedException
from .models import Player


class GameTest(TestCase):

    def test_attack(self):
        player1 = PlayerFactory()
        player2 = PlayerFactory()
        with self.assertRaises(AttackFailedException):
            player1.attack(player2)

        player1.buy_units(100)
        player1.attack(player2)
        self.assertEqual(
            player1.num_acres,
            int(round(Player.START_ACRES * Player.PERCENT_LAND_TO_TAKE)) + Player.START_ACRES
        )

    def test_reduce_buildings(self):
        player1 = PlayerFactory()
        player1._reduce_buildings(20)
        self.assertEqual(player1.buildings.num_gold_mines, 6)
        self.assertEqual(player1.buildings.num_empty, 12)
        self.assertEqual(player1.num_acres, 30)

    def test_reduce_buildings_unbalanced(self):
        player1 = PlayerFactory()
        player1._reduce_buildings(11)
        self.assertEqual(player1.buildings.num_gold_mines, 8)
        self.assertEqual(player1.buildings.num_empty, 15)
        self.assertEqual(player1.num_acres, 50 - 11)

    def test_reduce_buildings_unbalanced_no_empty(self):
        player1 = PlayerFactory()
        player1.num_acres = 30
        player1.save()
        player1._reduce_buildings(10)
        self.assertEqual(player1.buildings.num_empty, 0)
        self.assertEqual(player1.num_acres, 20)
