import pygame
import worldstate
import util


class GameState(worldstate.WorldState):
    def __init__(self, world):
        super(GameState, self).__init__(world)

    def handleInput(self):
        super(GameState, self).handleInput()
        if (self.left):
            self.left = False
            return self.world.GAMESTATE.reverse_mapping[0]
        return self.world.GAMESTATE.reverse_mapping[1]

    def update(self):
        super(GameState, self).update()
        util.BLACK = (140, 250, 10)

    def render(self):
        super(GameState, self).render()
