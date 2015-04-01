class Building(object):
	lumber_cost = 0
	gold_cost = 0
	pass

class LumberYard(Building):
	lumber_cost = 20
	gold_cost = 200
	lumber_bonus = 1.05

class GoldMine(Building):
	lumber_cost = 20
	gold_cost = 500
	gold_bonus = 1.05

	