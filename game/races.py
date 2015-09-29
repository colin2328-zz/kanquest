from units import Knight, Ranger, Adept

RACE_HUMAN = 'HUM'
RACE_ELF = 'ELF'
RACE_DARKELF = 'DEF'
RACE_CHOICES = (
    (RACE_HUMAN, 'Human'),
    (RACE_ELF, 'Elf'),
    (RACE_DARKELF, 'Dark Elf'),
)


class Race(object):
    unit = None


class Human(Race):
    unit = Knight


class Elf(Race):
    unit = Ranger


class DarkElf(Race):
    unit = Adept


RACES = {
    RACE_HUMAN: Human(),
    RACE_ELF: Elf(),
    RACE_DARKELF: DarkElf()
}
