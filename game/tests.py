from django.test import TestCase

from .factories import PlayerFactory
from .exceptions import AttackFailedException
from .models import Player, Buildings
from .buildings import GoldMine


class AttackTest(TestCase):

    def setUp(self):
        self.player1 = PlayerFactory()

    def test_attack_failed(self):
        player2 = PlayerFactory()
        with self.assertRaises(AttackFailedException):
            self.player1.attack(player2)

    def test_attack_success(self):
        player2 = PlayerFactory()
        self.player1.buy_units(100)
        self.player1.attack(player2)
        self.assertEqual(
            self.player1.num_acres,
            int(round(Player.START_ACRES * Player.PERCENT_LAND_TO_TAKE)) + Player.START_ACRES
        )
        self.assertEqual(
            player2.num_acres,
            -1 * int(round(Player.START_ACRES * Player.PERCENT_LAND_TO_TAKE)) + Player.START_ACRES
        )
        self.assertEqual(self.player1.num_units, (Player.START_UNITS + 100) * Player.PERCENT_UNITS_SURVIVE)

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


class BuildTest(TestCase):
    def test(self):
        player = PlayerFactory()
        self.assertEqual(player.num_gold, Player.START_GOLD)
        player.build(GoldMine, 5)
        self.assertEqual(player.buildings.num_gold_mines, 5 + Buildings.START_BUILDING_COUNT)
        self.assertEqual(player.num_gold, Player.START_GOLD - 5 * GoldMine.gold_cost)
        self.assertEqual(player.num_lumber, Player.START_LUMBER - 5 * GoldMine.lumber_cost)


class BuyUnitsTest(TestCase):
    def test(self):
        player = PlayerFactory()
        player.buy_units(100)
        self.assertEqual(player.num_units, Player.START_UNITS + 100)
        self.assertEqual(player.num_gold, Player.START_GOLD - 100 * player.race.unit.cost)


class ExploreTest(TestCase):
    def test(self):
        player = PlayerFactory()
        player.explore(10)
        self.assertEqual(player.num_acres, Player.START_ACRES + 10)
        self.assertEqual(player.num_gold, Player.START_GOLD - 10 * Player.EXPLORE_GOLD_COST_PER_ACRE)
