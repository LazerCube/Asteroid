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

        self.commandLineArgs(argv)

        self.EXIT = False

        self.GAMESTATE = util.enum(world.MenuState(self),
                                   world.GameState(self))
        self.SetState(0)
        self.GameLoop()
        self.exit()

    def SetState(self, new_state):
        self.state = self.GAMESTATE.reverse_mapping[new_state]

    def GameLoop(self):
        MS_PER_TICK = 15.625
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

            self.handleInput()

            while(self.lag >= MS_PER_TICK):
                self.fixedUpdate()
                self.lag -= MS_PER_TICK

            delta = self.lag / MS_PER_TICK
            self.update(delta)
            self.render()

    def handleInput(self):
        self.state.handleInput()

    def fixedUpdate(self):
        self.state.fixedUpdate()
        self.ticks += 1
        if(pygame.time.get_ticks() - self.timer >= 1000):
            self.DEBUG_INFO = ("Ticks: %i  |  FPS: %i  |  " % (self.ticks, self.frames))
            self.timer = pygame.time.get_ticks()
            self.frames = 0
            self.ticks = 0

    def update(self, delta):
        self.state.update(delta)

    def render(self):
        self.Surface.SURFACE.fill(util.BLACK)
        self.state.render()
        pygame.display.flip()
        self.frames += 1

    def exit(self):
        pygame.quit()
        sys.exit()

    def commandLineArgs(self, argv):
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

def _Initiate(argv):
    surface = Surface()
    game = GameEngine(argv, surface)
    pygame.quit()

if __name__ == "__main__":
    _Initiate(sys.argv[1:])
