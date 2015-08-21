from buildings import *
import random


class Player(object):
    # Player attributes
    name = ''
    race = None
    max_population = 0
    num_population = 0
    num_mana = 0
    num_units = 0
    num_acres = 0
    num_lumber = 0
    num_gold = 0

    buildings = {}

    # Constants
    START_ACRES = 50
    PERCENT_LAND_TO_TAKE = 0.1
    PERCENT_UNITS_SURVIVE = 0.9
    START_GOLD = 10000
    START_LUMBER = 100
    DEFAULT_POPULATION = 5 * START_ACRES
    DEFAULT_START_MANA = 100
    DEFAULT_GOLD_PER_TURN = 500
    DEFAULT_LUMBER_PER_TURN = 20
    START_BUILDINGS = {GoldMine: 10, LumberYard: 10, Tower: 10, Empty: 20}

    def __init__(self, name, race, num_units):
        """Starting Values"""
        self.name = name
        self.race = race
        self.num_population = self.DEFAULT_POPULATION
        self.num_mana = self.DEFAULT_START_MANA
        self.num_units = num_units
        self.num_acres = self.START_ACRES
        self.num_lumber = self.START_LUMBER
        self.num_gold = self.START_GOLD
        self.num_gold_per_turn = self.DEFAULT_GOLD_PER_TURN
        self.num_lumber_per_turn = self.DEFAULT_LUMBER_PER_TURN
        self.buildings = self.START_BUILDINGS.copy()

    def __str__(self):
        return self.name

    def print_state(self):
        """ For debugging, print all info about player"""
        print '{}: {} {} {} acres, {} gold, {} lumber, {} buildings, {} mana, {} population'.format(
            self, self.num_units, self.race.unit.name,
            self.num_acres, self.num_gold, self.num_lumber, self.buildings,
            self.num_mana, self.num_population)

    def attack(self, other_player):
        """ Attack player other_player"""
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
            print '{} Failed to attack {}'.format(self, other_player)

        self.num_units *= self.PERCENT_UNITS_SURVIVE
        other_player.num_units *= self.PERCENT_UNITS_SURVIVE

    def buy_units(self, num_units):
        # Check to see if player has gold to purchase units, and complete transaction
        if self.num_gold < num_units*self.race.unit.cost:
            print('{} does not have enough gold to make that purchase.'.format(self))
            return

        self.num_gold -= num_units*self.race.unit.cost
        self.num_units += num_units

    def build(self, building_type, quantity):
        """Build entered quantity of select building type"""

        # check to make sure that we have enough resources
        if self.num_gold < quantity*building_type.gold_cost or self.num_lumber < quantity*building_type.lumber_cost:
            print('{} does not have enough resources to make that purchase.'.format(self))
            return
        if (sum(self.buildings.values()) + quantity) > self.num_acres:
            print('{} does not have enough land to build {} buildings'.format(self, quantity))
            return
        self.buildings[building_type] += quantity

    def cast(self, spell, target):
        """Cast spell on target"""
        if self.num_mana < spell.mana_cost:
            print('{} does not have enough mana to cast {}'.format(self), spell)
            return 
        self.num_mana -= spell.mana_cost
        spell.cast(target)
        print('{} casts {} on {}').format(self, spell, target)

    def take_turn(self):
        """Only called by game.py"""
        max_population = 10 * self.num_acres
        self.num_gold += GoldMine.GOLD_PER_TURN * self.buildings[GoldMine]
        self.num_lumber += LumberYard.LUMBER_PER_TURN * self.buildings[LumberYard]
        self.num_mana += Tower.MANA_PER_TURN * self.buildings[Tower]
        self.num_population = min(max_population, int(round(self.num_population * 1.01)))

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
