import os
import pygame

# ------DISPLAY INFO-----#

SURFACE_WIDTH = 800
SURFACE_HEIGHT = SURFACE_WIDTH / 16 * 9
SURFACE_CAPTION = "Python game engine"

PATH = os.getcwd()
ICON = pygame.image.load(os.path.join("vesta", "resources", "images" ,"terminal.png"))

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

# ------    DEBUG   ------#

DEBUG_MODE = False

DEBUG_CONSOLE_WIDTH = (SURFACE_WIDTH * 0.9)
DEBUG_CONSOLE_HEIGHT = 32
DEBUG_CONSOLE_BACKGROUND_COLOR = TERM_GRAY
DEBUG_CONSOLE_X = 0
DEBUG_CONSOLE_Y = (SURFACE_HEIGHT - DEBUG_CONSOLE_HEIGHT)
