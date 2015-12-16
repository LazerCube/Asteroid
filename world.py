import pygame
import menustate
import gamestate
import util


class World():
    def __init__(self, SURFACE):
        self.SURFACE = SURFACE
        self.WIDTH = SURFACE.get_width()
        self.HEIGHT = SURFACE.get_height()
        self.GAMESTATE = util.enum(menustate.MenuState(self),
                                   gamestate.GameState(self))

        self.state = self.GAMESTATE.reverse_mapping[0]
        self._state = None

        self.EXIT = False

        self.GAMEID = None
        self.NUM = None
        self.HOST = None

    def handleState(self):
        self._state = (self.state.handleInput())
        self.state = self._state

    def update(self):
        self.handleState()
        self.state.update()

    def render(self):
        self.state.render()

    def resizeWorld(self):
        pass

# handle change in sizing
