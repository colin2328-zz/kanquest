<<<<<<< HEAD
from races import Human, Elf
from player import Player
from game import Game
from buildings import GoldMine
from spells import Fireball
=======
from game.races import Human, Elf
from game.models import Game, Player
from game.buildings import GoldMine
from game.spells import Fireball
>>>>>>> 0f14a96058f415ec5497ef427dda7f189735cb98

colin = Player('Colin', Human, 200)
hakan = Player('Hakan', Elf, 300)
game = Game({colin, hakan})


<<<<<<< HEAD
print ('Starting states:')
=======
print('Starting states:')
>>>>>>> 0f14a96058f415ec5497ef427dda7f189735cb98
colin.print_state()
hakan.print_state()

game.take_turn()
<<<<<<< HEAD
print ('Hakan attacks Colin:')
=======
print('Hakan attacks Colin:')
>>>>>>> 0f14a96058f415ec5497ef427dda7f189735cb98
hakan.attack(colin)
colin.print_state()
hakan.print_state()

<<<<<<< HEAD
print ('Colin buys units:')
=======
print('Colin buys units:')
>>>>>>> 0f14a96058f415ec5497ef427dda7f189735cb98
colin.buy_units(10)
colin.print_state()
hakan.print_state()

game.take_turn()
<<<<<<< HEAD
print ('Colin attacks Hakan')
=======
print('Colin attacks Hakan')
>>>>>>> 0f14a96058f415ec5497ef427dda7f189735cb98
colin.attack(hakan)
colin.print_state()
hakan.print_state()

game.take_turn()
<<<<<<< HEAD
print ('Colin buys gold mines')
=======
print('Colin buys gold mines')
>>>>>>> 0f14a96058f415ec5497ef427dda7f189735cb98
colin.build(GoldMine, 5)
colin.print_state()

game.take_turn()
<<<<<<< HEAD
print ('Colin fireballs Hakan')
=======
print('Colin fireballs Hakan')
>>>>>>> 0f14a96058f415ec5497ef427dda7f189735cb98
colin.cast(Fireball, hakan)
colin.print_state()
hakan.print_state()