import math
import pygame

# ------DISPLAY INFO-----#

SURFACE_WIDTH = 700
SURFACE_HEIGHT = 700
SURFACE_CAPTION = "Python game engine"

# --------COLOURS--------#

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 40)
LIGHT_GREY = (05, 05, 05)
TERM_BLUE = (46, 158, 244)
TERM_GRAY = (44, 44, 44)
TERM_LIGHT_GRAY = (102, 102, 102)
DARK_BLUE = (40, 44, 52)

DEFAULT_FONT = 'franklin gothic'


def cos(angle):
    x = math.radians(angle)
    return math.cos(x)


def sin(angle):
    x = math.radians(angle)
    return math.sin(x)


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)

# Numbers = enum('ZERO','ONE','TWO',THREE = 'three')
# print(Numbers.ONE)
# OUTPUT: 1
# print(Numbers.reverse_mapping['three'])
# OUTPUT THREE
