#!/usr/bin/python
import sys
import getopt
import pygame

import world
import settings
from utilites import util

class Surface():
    def __init__(self):
        pygame.init()

        self.SURFACE = pygame.display.set_mode(
                [util.SURFACE_WIDTH, util.SURFACE_HEIGHT], pygame.HWSURFACE |
                pygame.DOUBLEBUF)

        self.WIDTH = self.SURFACE.get_width()
        self.HEIGHT = self.SURFACE.get_height()

        self.CAPTION = None
        self.ICON = None

        self.set_caption(util.SURFACE_CAPTION)
        self.set_icon(util.ICON)

    def set_caption(self, caption):
        self.CAPTION = caption
        pygame.display.set_caption(caption)

    def set_icon(self, icon):
        self.ICON = icon
        pygame.display.set_icon(icon)

class GameEngine():
    def __init__(self, argv, surface):
        self.Surface = surface

        self.DEBUG_MODE = settings.DEBUG_MODE
        self.DEBUG_INFO = "None"

        self.TIME_MOD = 1

        self.command_line_args(argv)

        self.EXIT = False

        #self.GAMESTATE = util.enum(world.MenuState(self),
                                   #world.GameState(self))

        # Events
        self.resize = False
        self.reload = False

        # Keyboard Inputs
        self.escape = False
        self.delete = False
        self.k_space = False
        self.k_left = False
        self.k_right = False
        self.k_up = False
        self.k_down = False
        self.k_a = False
        self.k_d = False

        # Keyboard Numberpad
        self.keypad_0 = False
        self.keypad_1 = False
        self.keypad_2 = False
        self.keypad_3 = False
        self.keypad_4 = False
        self.keypad_5 = False
        self.keypad_6 = False
        self.keypad_7 = False
        self.keypad_8 = False
        self.keypad_9 = False

        # Keyboard Number row
        self.k_0 = False
        self.k_1 = False
        self.k_2 = False
        self.k_3 = False

        # Keyboard Function keys
        self.k_f4 = False

        # Mouse Inputs
        self.mouse_pressed = [False, False, False]
        self.mouse_pos = [0, 0]

        # CURRENT STATE AS INT (TEMP)
        self.n_state = 0

        self.set_state(self.n_state)
        self.game_loop()
        self.exit()

    def set_state(self, new_state):
        #self.state = self.GAMESTATE.reverse_mapping[new_state]
        if(new_state == 0):
            self.state = world.MenuState(self)
            self.n_state = 0
        elif(new_state == 1):
            self.state = world.GameStateController(self)
            self.n_state = 1

    def game_loop(self):
        MS_PER_TICK = 15.625 * self.TIME_MOD
        previous = pygame.time.get_ticks()
        self.lag = 0.0

        self.timer = pygame.time.get_ticks()
        self.frames = 0
        self.ticks = 0

        while not(self.EXIT):
            current = pygame.time.get_ticks()
            elapsed = current - previous
            previous = current
            self.lag += elapsed

            self.handle_input()

            while(self.lag >= MS_PER_TICK):
                self.fixed_update()
                self.lag -= MS_PER_TICK

            delta = self.lag / MS_PER_TICK
            self.update(delta)
            self.render()

    def handle_input(self):
        for event in pygame.event.get():
            pygame.event.pump()
            if event.type == pygame.QUIT:
                self.EXIT = True
            elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(self.mouse_pressed)):
                    if pygame.mouse.get_pressed()[i]:
                        self.mouse_pressed[i] = True
                    else:
                        self.mouse_pressed[i] = False
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    if (event.type == pygame.KEYDOWN):
                        if(self.escape == True):
                            self.escape = False
                        else:
                            self.escape = True
                if event.key == pygame.K_F4:
                    if (event.type == pygame.KEYDOWN):
                        if(self.reload == True):
                            self.reload = False
                        else:
                            self.reload = True
                elif event.key == pygame.K_DELETE:
                    self.delete = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_SPACE:
                    self.k_space = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_KP0:
                    self.keypad_0 = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_KP1:
                    self.keypad_1 = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_KP2:
                    self.keypad_2 = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_KP3:
                    self.keypad_3 = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_KP4:
                    self.keypad_4 = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_KP5:
                    self.keypad_5 = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_KP6:
                    self.keypad_6 = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_KP7:
                    self.keypad_7 = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_KP8:
                    self.keypad_8 = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_KP9:
                    self.keypad_9 = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_0:
                    self.k_0 = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_1:
                    self.k_1 = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_2:
                    self.k_2 = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_3:
                    self.k_3 = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_LEFT:
                    self.k_left = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_RIGHT:
                    self.k_right = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_DOWN:
                    self.k_down = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_UP:
                    self.k_up = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_a:
                    self.k_a = event.type == pygame.KEYDOWN
                elif event.key == pygame.K_d:
                    self.k_d = event.type == pygame.KEYDOWN

        self.mouse_pos = pygame.mouse.get_pos()
        self.state.handle_input()

        # if(self.reload):
        #     self.reload_world()
        #     self.reload = False

    # def clean(self):
    #     print("CLEAN")
    #
    # def reload_world(self):
    #     print("RELOAD START!")
    #     self.clean()
    #     reload(settings)
    #     reload(world)
    #     self.set_state(self.n_state)
    #     print("RELOADED!")

    def fixed_update(self):
        self.state.fixed_update()
        self.ticks += 1
        if(pygame.time.get_ticks() - self.timer >= 1000):
            self.DEBUG_INFO = ("Ticks: %i  |  FPS: %i  |  " % (self.ticks, self.frames))
            self.timer = pygame.time.get_ticks()
            self.frames = 0
            self.ticks = 0

    def update(self, delta):
        self.state.update(delta)

    def render(self):
        self.state.render()
        pygame.display.flip()
        self.frames += 1

    def exit(self):
        pygame.quit()
        sys.exit()

    def command_line_args(self, argv):
       try:
           opts, args = getopt.getopt(argv,"hd")
       except getopt.GetoptError:
           print '\nUsage main.py [-h] [-d]'
           sys.exit(2)
       for opt, arg in opts:
           if opt == '-h':
               print '\nOptional arguments: \n\n -h, --help  Shows this help message and exit\n -d, --debug  Runs program in debug mode.'
               sys.exit()
           elif opt in ("-d", "--debug"):
               self.DEBUG_MODE = True
       if self.DEBUG_MODE:
           print("\n\n----------DEBUG----------\n\n")

def initiate(argv):
    surface = Surface()
    game = GameEngine(argv, surface)
    pygame.quit()

if __name__ == "__main__":
    initiate(sys.argv[1:])
