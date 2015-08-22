import random
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

from .buildings import *
from .races import RACE_CHOICES, RACE_HUMAN, RACES
from .exceptions import NotEnoughGoldException


class Player(User):
    buildings = {}  # TODO make into model

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
    START_BUILDINGS = {GoldMine: 10, LumberYard: 10, Tower: 10, Empty: 20}

    race_choice = models.SmallIntegerField(choices=RACE_CHOICES, default=RACE_HUMAN)
    num_population = models.IntegerField(default=START_POPULATION, validators=[MinValueValidator(0)])
    num_mana = models.IntegerField(default=START_MANA, validators=[MinValueValidator(0)])
    num_units = models.IntegerField(default=START_UNITS, validators=[MinValueValidator(0)])
    num_acres = models.IntegerField(default=START_ACRES, validators=[MinValueValidator(0)])
    num_lumber = models.IntegerField(default=START_LUMBER, validators=[MinValueValidator(0)])
    num_gold = models.IntegerField(default=START_GOLD, validators=[MinValueValidator(0)])

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
        if (
            self.num_units * self.race.unit.attack >
            other_player.num_units * other_player.race.unit.defense
        ):
            # Calculate amount of land to be taken, reduce enemy's buildings, reduce enemy's land, then add the same # of acres to your kingdom
            amount_to_take = int(round(other_player.num_acres * self.PERCENT_LAND_TO_TAKE))
            other_player._reduce_buildings(amount_to_take)
            other_player.num_acres -= amount_to_take
            self.num_acres += amount_to_take
            self.buildings[Empty] += amount_to_take
            print(
                '{} Successfully attacked {} and conquered {} acres'
                ).format(self, other_player, amount_to_take)
        else:
            print('{} Failed to attack {}'.format(self, other_player))

        self.num_units *= self.PERCENT_UNITS_SURVIVE
        other_player.num_units *= self.PERCENT_UNITS_SURVIVE
        self.save()
        other_player.save()

    def buy_units(self, num_units):
        if self.num_gold < num_units*self.race.unit.cost:
            raise NotEnoughGoldException()

        self.num_gold -= num_units*self.race.unit.cost
        self.num_units += num_units
        self.save()

    def build(self, building_type, quantity):
        """Build entered quantity of select building type"""

        # check to make sure that we have enough resources
        if self.num_gold < quantity*building_type.gold_cost:
            raise NotEnoughGoldException()

        if self.num_lumber < quantity*building_type.lumber_cost:
            raise NotEnoughLumberException()
        if (sum(self.buildings.values()) + quantity) > self.num_acres:
            raise NotEnoughLandException

        self.buildings[building_type] += quantity
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
        self.num_gold += GoldMine.GOLD_PER_TURN * self.buildings[GoldMine]
        self.num_lumber += LumberYard.LUMBER_PER_TURN * self.buildings[LumberYard]
        self.num_mana += Tower.MANA_PER_TURN * self.buildings[Tower]
        self.num_population = min(max_population, int(round(self.num_population * 1.01)))
        self.save()

    def _reduce_buildings(self, quantity):
        """Called during a successful attack by player, makes sure that a player can't have more buildings than land"""
        total_loss = 0
        # Calculate the %age of land made up by each building type, then divy up the lost land according to those %s
        for building, count in self.buildings.iteritems():
            reduction = int(round(count / float(self.num_acres) * quantity))
            total_loss += reduction
            self.buildings[building] -= reduction

        # Is there a difference between the land lost and number of buildings lost due to rounding errors?
        difference = quantity - total_loss
        if difference == 0:
            return

        # If there is, remove buildings at random until the discrepancy no longer exists.
        for x in range(0, difference):
            self.buildings[random.choice(self.buildings.keys())] -= 1
