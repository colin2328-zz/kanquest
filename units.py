class Unit(object):
    attack = 0
    defense = 0
    name = None

    def __repr__(self):
        return self.name


class Knight(Unit):
    name = 'Knight'
    attack = 5
    defense = 7


class Ranger(Unit):
    name = 'Ranger'
    attack = 5
    defense = 7
