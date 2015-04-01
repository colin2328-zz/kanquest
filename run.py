from races import Human, Elf
from player import Player

me = Player('Colin', Human, 200)
hakan = Player('Hakan', Elf, 300)


print ('Starting states:')
me.print_state()
hakan.print_state()

print ('Hakan attacks Colin:')
hakan.attack(me)
me.print_state()
hakan.print_state()

print ('Colin buys units:')
me.buy_units(10)
me.print_state()
hakan.print_state()

print ('Colin attacks Hakan')
me.attack(hakan)
me.print_state()
hakan.print_state()
