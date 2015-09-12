from units import Knight, Ranger

RACE_HUMAN = 'HUM'
RACE_ELF = 'ELF'
# RACE_DARKELF = 3
# RACE_DWARF = 4
RACE_CHOICES = (
    (RACE_HUMAN, 'Human'),
    (RACE_ELF, 'Elf'),
    # (RACE_DARKELF, 'Dark Elf'),
    # (RACE_DWARF, 'Dwarf'),
)


class Race(object):
    unit = None


class Human(Race):
    unit = Knight


class Elf(Race):
    unit = Ranger

# class DarkElf(Race):
#     unit = Adept

RACES = {
    RACE_HUMAN: Human(),
    RACE_ELF: Elf(),
}
