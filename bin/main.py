#!/usr/bin/python
import sys
import getopt
import pygame

import world
import settings
from utilites import util

class _Game():
    def __init__(self, argv, SURFACE):
        self.SURFACE = SURFACE
        self.WIDTH = SURFACE.get_width()
        self.HEIGHT = SURFACE.get_height()
        self.DEBUG_MODE = settings.DEBUG_MODE
        self.DEBUG_INFO = "None"

        self.EXIT = False

        self.GAMEID = None
        self.NUM = None
        self.HOST = None

        self.commandLineArgs(argv)

        self.GAMESTATE = util.enum(world.MenuState(self),
                                   world.GameState(self))

        self.state = self.GAMESTATE.reverse_mapping[0]
        self._state = None

        self.Engine()

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

    def HandleState(self):
        self._state = (self.state.HandleInput())
        self.state = self._state

    def Engine(self):
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

            self.HandleInput()

            while(self.lag >= MS_PER_TICK):
                self.Update()
                self.lag -= MS_PER_TICK

            delta = self.lag / MS_PER_TICK
            self.RenderFrame(delta)

    def HandleInput(self):
        self.HandleState()

    def Update(self):
        self.state.Update()
        self.ticks += 1
        if(pygame.time.get_ticks() - self.timer >= 1000):
            self.DEBUG_INFO = ("Ticks: %i  |  FPS: %i  |  " % (self.ticks, self.frames))
            self.timer = pygame.time.get_ticks()
            self.frames = 0
            self.ticks = 0

    def RenderFrame(self, delta):
        self.SURFACE.fill(util.BLACK)
        self.state.RenderFrame(delta)
        pygame.display.flip()
        self.frames += 1

def _Initiate(argv):
    pygame.init()
    SURFACE = pygame.display.set_mode(
        [util.SURFACE_WIDTH, util.SURFACE_HEIGHT], pygame.HWSURFACE |
        pygame.DOUBLEBUF)
    pygame.display.set_caption(util.SURFACE_CAPTION)
    pygame.display.set_icon(util.ICON)
    game = _Game(argv, SURFACE)

    pygame.quit()

if __name__ == "__main__":
    _Initiate(sys.argv[1:])
