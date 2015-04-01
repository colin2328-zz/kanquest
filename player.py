class Player(object):
    name = ''
    race = None
    num_units = 0
    num_acres = 0

    START_ACRES = 500
    PERCENT_LAND_TO_TAKE = 0.1
    PERCENT_UNITS_SURVIVE = 0.9

    def __init__(self, name, race, num_units):
        self.name = name
        self.race = race
        self.num_units = num_units
        self.num_acres = self.START_ACRES

    def __str__(self):
        return self.name

    def print_state(self):
        print '{}: {} {} {} acres'.format(self, self.num_units, self.race.unit.name, self.num_acres)

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
