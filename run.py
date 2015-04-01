from races import Human, Elf
from player import Player
from game import Game
from buildings import GoldMine
from spells import Fireball

colin = Player('Colin', Human, 200)
hakan = Player('Hakan', Elf, 300)
game = Game({colin, hakan})


print ('Starting states:')
colin.print_state()
hakan.print_state()

game.take_turn()
print ('Hakan attacks Colin:')
hakan.attack(colin)
colin.print_state()
hakan.print_state()

print ('Colin buys units:')
colin.buy_units(10)
colin.print_state()
hakan.print_state()

game.take_turn()
print ('Colin attacks Hakan')
colin.attack(hakan)
colin.print_state()
hakan.print_state()

game.take_turn()
print ('Colin buys gold mines')
colin.build(GoldMine, 5)
colin.print_state()

game.take_turn()
print ('Colin fireballs Hakan')
colin.cast(Fireball, hakan)
colin.print_state()
hakan.print_state()