from races import Human, Elf
from player import Player

me = Player('Colin', Human, 200)
hakan = Player('Hakan', Elf, 300)

me.print_state()
hakan.attack(me)
me.print_state()

me.buy_units(10)
me.print_state()