from races import Human, Elf
from player import Player
from game import Game
from buildings import GoldMine

me = Player('Colin', Human, 200)
hakan = Player('Hakan', Elf, 300)
game = Game({me, hakan})


print ('Starting states:')
me.print_state()
hakan.print_state()

game.take_turn()
print ('Hakan attacks Colin:')
hakan.attack(me)
me.print_state()
hakan.print_state()

print ('Colin buys units:')
me.buy_units(10)
me.print_state()
hakan.print_state()

game.take_turn()
print ('Colin attacks Hakan')
me.attack(hakan)
me.print_state()
hakan.print_state()

game.take_turn()
print ('Colin buys gold mines')
me.build(GoldMine, 5)
me.print_state()
