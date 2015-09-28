from django.test import TestCase

from .factories import PlayerFactory
from .exceptions import AttackFailedException
from .models import Player


class AttackTest(TestCase):

    def setUp(self):
        self.player1 = PlayerFactory()

    def test_attack(self):
        player2 = PlayerFactory()
        with self.assertRaises(AttackFailedException):
            self.player1.attack(player2)

        self.player1.buy_units(100)
        self.player1.attack(player2)
        self.assertEqual(
            self.player1.num_acres,
            int(round(Player.START_ACRES * Player.PERCENT_LAND_TO_TAKE)) + Player.START_ACRES
        )

    def test_reduce_buildings(self):
        self.player1._reduce_buildings(20)
        self.assertEqual(self.player1.buildings.num_gold_mines, 6)
        self.assertEqual(self.player1.buildings.num_empty, 12)
        self.assertEqual(self.player1.num_acres, 30)

    def test_reduce_buildings_unbalanced(self):
        self.player1._reduce_buildings(11)
        self.assertEqual(self.player1.buildings.num_gold_mines, 8)
        self.assertEqual(self.player1.buildings.num_empty, 15)
        self.assertEqual(self.player1.num_acres, 50 - 11)

    def test_reduce_buildings_unbalanced_no_empty(self):
        self.player1.num_acres = 30
        self.player1.save()
        self.player1._reduce_buildings(10)
        self.assertEqual(self.player1.buildings.num_empty, 0)
        self.assertEqual(self.player1.num_acres, 20)
