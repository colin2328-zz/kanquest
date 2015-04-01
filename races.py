# Human, Elf, DarkElf, Dwarf
from units import Knight, Ranger


class Race(object):
    unit = None


class Human(Race):
    unit = Knight


class Elf(Race):
    unit = Ranger


# class DarkElf(Race):
#     units = {'adept'}
