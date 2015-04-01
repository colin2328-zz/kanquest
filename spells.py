class Spell(object):
	mana_cost = 0

class Fireball(Spell):
	mana_cost = 50
	@staticmethod
	def cast(target):
		target.num_population = round(target.num_population * 0.9)

