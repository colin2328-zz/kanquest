class GameException(Exception):
    message = 'In Game Exception'


class NotEnoughGoldException(GameException):
    message = 'Not enough gold'


class NotEnoughLumberException(GameException):
    message = 'Not enough lumber'


class NotEnoughLandException(GameException):
    message = 'Not enough land'


class NotEnoughManaException(GameException):
    message = 'Not enough mana'


class AttackFailedException(GameException):
    message = 'Attack failed'
