class Game(object):
    players = {}
    turn_count = 0

    def __init__(self, players):
        self.players = players
        self.turn_count = 0

    def take_turn(self):
        self.turn_count += 1
        for player in self.players:
            player.take_turn()
        print '\nOne turn has advanced:'
