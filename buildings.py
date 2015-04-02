class Building(object):
	lumber_cost = 0
	gold_cost = 0
	pass

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
	
class Empty(Building):
	lumber_cost = 0
	gold_cost = 0