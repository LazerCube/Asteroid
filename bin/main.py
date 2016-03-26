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

        self._Run()

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

    def handleState(self):
        self._state = (self.state.handleInput())
        self.state = self._state

    def _Run(self):
        _MS_PER_TICK = 15.625
        _previous_time = pygame.time.get_ticks()
        _previous_timer = pygame.time.get_ticks()
        _current_time = 0

        frames = 0
        ticks = 0
        delta = 0

        while not(self.EXIT):
            _current_time = pygame.time.get_ticks()
            delta += ((_current_time - _previous_time) / _MS_PER_TICK)
            _previous_time = _current_time

            while(delta >= 1):
                self.update()
                ticks += 1
                delta -= 1

            self.Render()
            frames += 1

            if(pygame.time.get_ticks() - _previous_timer >= 1000):
                self.DEBUG_INFO = ("Ticks: %i  |  FPS: %i  |  " % (ticks, frames))
                _previous_timer = pygame.time.get_ticks()
                frames = 0
                ticks = 0

    def update(self):
        self.handleState()
        self.state.update()

    def Render(self):
        self.SURFACE.fill(util.BLACK)
        self.state.render()
        pygame.display.flip()

    def resizeWorld(self):
        pass


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
