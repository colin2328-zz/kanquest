from django.shortcuts import get_object_or_404

from game.models import Player


class Action(object):
    """Transforms requests extra data into an actual event"""
    player = None
    data = {}

    def __init__(self, player, data):
        self.player = player
        self.data = data

    def attack(self):
        target_id = self.data.get('target')
        target = get_object_or_404(Player, id=target_id)
        return self.player.attack(target)

    def explore(self):
        return self.player.explore()

    def build(self):
        building_type = self.data.get('building_type')
        quantity = self.data.get('quantity')
        return self.player.build(building_type, quantity)

    def cast(self):
        spell = self.data.get('spell')
        target_id = self.data.get('target_id')
        target = get_object_or_404(Player, id=target_id)
        return self.player.cast(spell, target)
