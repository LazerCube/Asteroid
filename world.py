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
                                   gamestate.GameState(self),
                                   'STATE_EXIT')

        self.state = self.GAMESTATE.reverse_mapping[0]
        self._state = None

    def handleInput(self):
        self._state = (self.state.handleInput())
        self.state = self._state

    def update(self):
        self.handleInput()
        self.state.update()

    def render(self):
        self.state.render()
