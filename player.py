class Player(object):
    name = ''
    race = None
    num_units = 0
    num_acres = 0
    num_lumber = 0
    num_gold = 0

    START_ACRES = 500
    PERCENT_LAND_TO_TAKE = 0.1
    PERCENT_UNITS_SURVIVE = 0.9
    START_GOLD = 10000
    START_LUMBER = 100

    def __init__(self, name, race, num_units):
        self.name = name
        self.race = race
        self.num_units = num_units
        self.num_acres = self.START_ACRES
        self.num_lumber = self.START_LUMBER
        self.num_gold = self.START_GOLD

    def __str__(self):
        return self.name

    def print_state(self):
        print '{}: {} {} {} acres, {} gold, {} lumber'.format(
            self, self.num_units, self.race.unit.name, 
            self.num_acres, self.num_gold, self.num_lumber)

    def add_units(self, num_units):
        self.num_units += num_units

    def attack(self, other_player):
        if (
            self.num_units * self.race.unit.attack >
            other_player.num_units * other_player.race.unit.defense
        ):
            amount_to_take = other_player.num_acres * self.PERCENT_LAND_TO_TAKE
            other_player.num_acres -= amount_to_take
            self.num_acres += amount_to_take
            print (
                '{} Successfully attacked {} and conquered {} acres'
                ).format(self, other_player, amount_to_take)
        else:
            print '{} Failed to attack {}'.format(self, other_player)

        self.num_units *= self.PERCENT_UNITS_SURVIVE
        other_player.num_units *= self.PERCENT_UNITS_SURVIVE

    def buy_units(self, num_units):
        if self.num_gold < num_units*self.race.unit.cost:
            print ('{} does not have enough gold to make that purchase.'.format(self))
        else:
            self.num_gold -= num_units*self.race.unit.cost
            self.num_units += num_units