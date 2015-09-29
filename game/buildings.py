import re


class Building(object):
    lumber_cost = 0
    gold_cost = 0

    def get_field_name(self):
        return 'num_{}s'.format(self._convert(self.__class__.__name__))

    def _convert(self, name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class LumberYard(Building):
    LUMBER_PER_TURN = 50
    lumber_cost = 20
    gold_cost = 200


class GoldMine(Building):
    GOLD_PER_TURN = 45
    lumber_cost = 20
    gold_cost = 500


class Tower(Building):
    MANA_PER_TURN = 25
    lumber_cost = 20
    gold_cost = 500
