class Spell(object):
    mana_cost = 0


class Fireball(Spell):
    mana_cost = 50

    @staticmethod
    def cast(target):
        # Decimate enemy population
        target.num_population = int(round(target.num_population * 0.9))
