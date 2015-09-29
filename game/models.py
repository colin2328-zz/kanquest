import random
from django.db import models
from django.contrib.auth.models import User
from annoying.fields import AutoOneToOneField

from .buildings import GoldMine, LumberYard, Tower
from .races import RACE_CHOICES, RACE_HUMAN, RACES
from .exceptions import (
    NotEnoughGoldException, AttackFailedException, NotEnoughLumberException,
    NotEnoughManaException, NotEnoughLandException
)


class Player(User):

    # Constants
    START_ACRES = 50
    PERCENT_LAND_TO_TAKE = 0.1
    PERCENT_UNITS_SURVIVE = 0.9
    START_GOLD = 10000
    START_LUMBER = 100
    START_POPULATION = 5 * START_ACRES
    START_MANA = 100
    START_UNITS = 200
    DEFAULT_GOLD_PER_TURN = 500
    DEFAULT_LUMBER_PER_TURN = 20
    EXPLORE_GOLD_COST_PER_ACRE = 100

    race_choice = models.CharField(choices=RACE_CHOICES, max_length=3, default=RACE_HUMAN)
    num_population = models.PositiveIntegerField(default=START_POPULATION)
    num_mana = models.PositiveIntegerField(default=START_MANA)
    num_units = models.PositiveIntegerField(default=START_UNITS)
    num_acres = models.PositiveIntegerField(default=START_ACRES)
    num_lumber = models.PositiveIntegerField(default=START_LUMBER)
    num_gold = models.PositiveIntegerField(default=START_GOLD)

    def __unicode__(self):
        return self.username

    @property
    def race(self):
        return RACES[self.race_choice]

    def state(self):
        """ For debugging, return all info about player"""
        return '{}: {} {} {} acres, {} gold, {} lumber, {} buildings, {} mana, {} population'.format(
            self, self.num_units, self.race.unit.name,
            self.num_acres, self.num_gold, self.num_lumber, self.buildings,
            self.num_mana, self.num_population)

    def attack(self, other_player):
        """Attack player other_player"""
        # Compare your offense to enemy defense
        failed = (
            self.num_units * self.race.unit.attack <=
            other_player.num_units * other_player.race.unit.defense
        )
        self.num_units *= self.PERCENT_UNITS_SURVIVE
        other_player.num_units *= self.PERCENT_UNITS_SURVIVE
        self.save()
        other_player.save()
        if failed:
            raise AttackFailedException()
        # Calculate amount of land to be taken, reduce enemy's buildings, reduce enemy's land, then add the same # of acres to your kingdom
        amount_to_take = int(round(other_player.num_acres * self.PERCENT_LAND_TO_TAKE))
        other_player._reduce_buildings(amount_to_take)
        self.num_acres += amount_to_take
        self.save()
        return (
            '{} Successfully attacked {} and conquered {} acres'
            ).format(self, other_player, amount_to_take)

    def buy_units(self, num_units):
        if self.num_gold < num_units*self.race.unit.cost:
            raise NotEnoughGoldException()

        self.num_gold -= num_units*self.race.unit.cost
        self.num_units += num_units
        self.save()

    def explore(self, quantity):
        if self.num_gold < quantity * self.EXPLORE_GOLD_COST_PER_ACRE:
            raise NotEnoughGoldException()

        self.num_gold -= quantity * self.EXPLORE_GOLD_COST_PER_ACRE
        self.num_acres += quantity
        self.save()

    def build(self, building_type, quantity):
        """Build entered quantity of select building type"""

        # check to make sure that we have enough resources
        if self.num_gold < quantity*building_type.gold_cost:
            raise NotEnoughGoldException()

        if self.num_lumber < quantity*building_type.lumber_cost:
            raise NotEnoughLumberException()
        if self.buildings.num_empty < quantity:
            raise NotEnoughLandException

        field = building_type().get_field_name()
        setattr(self.buildings, field, getattr(self.buildings, field) + quantity)
        self.num_gold -= quantity*building_type.gold_cost
        self.num_lumber -= quantity*building_type.lumber_cost
        self.save()

    def cast(self, spell, target):
        """Cast spell on target"""
        if self.num_mana < spell.mana_cost:
            raise NotEnoughManaException()
        self.num_mana -= spell.mana_cost
        spell.cast(target)
        print('{} casts {} on {}').format(self, spell, target)
        self.save()

    def take_turn(self):
        """Only called by game.py"""
        max_population = 10 * self.num_acres
        self.num_gold += GoldMine.GOLD_PER_TURN * self.buildings.num_gold_mines
        self.num_lumber += LumberYard.LUMBER_PER_TURN * self.buildings.num_lumber_yards
        self.num_mana += Tower.MANA_PER_TURN * self.buildings.num_towers
        self.num_population = min(max_population, int(round(self.num_population * 1.01)))
        self.save()

    def _reduce_buildings(self, quantity):
        """Called during a successful attack by player, makes sure that a player can't have more buildings than land"""
        total_loss = 0
        percent_to_take = quantity / float(self.num_acres)
        empty_reduction = int(round(self.buildings.num_empty * percent_to_take))
        total_loss += empty_reduction
        self.num_acres -= quantity
        # Calculate the %age of land made up by each building type, then divy up the lost land according to those %s
        for field in self.buildings.get_building_fields():
            count = getattr(self.buildings, field)
            reduction = int(round(count * percent_to_take))
            total_loss += reduction
            setattr(self.buildings, field, count - reduction)

        # difference between the land lost and number of buildings lost due to rounding errors?
        difference = quantity - total_loss

        # If there is, remove buildings at random until the discrepancy no longer exists.
        # take from empty
        difference -= max(0, self.buildings.num_empty)
        for x in range(0, difference):
            field = random.choice(self.buildings.get_building_fields())
            count = getattr(self.buildings, field)
            setattr(self.buildings, field, count - 1)
        self.save()


class Buildings(models.Model):
    START_BUILDING_COUNT = 10
    player = AutoOneToOneField(Player, primary_key=True)

    num_gold_mines = models.PositiveIntegerField(default=START_BUILDING_COUNT)
    num_lumber_yards = models.PositiveIntegerField(default=START_BUILDING_COUNT)
    num_towers = models.PositiveIntegerField(default=START_BUILDING_COUNT)

    @property
    def num_empty(self):
        fields = self.get_building_fields()
        return self.player.num_acres - sum([getattr(self, field) for field in fields])

    def get_building_fields(self):
        fields = self._meta.get_all_field_names()
        return [field for field in fields if 'num_' in field]
