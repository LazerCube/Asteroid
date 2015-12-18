import world
import SharedEntities.playership

import pygame
import util


class GameState(world.WorldState):
    def __init__(self, world):
        super(GameState, self).__init__(world)
        self.n_players = 0

    def handleInput(self):
        super(GameState, self).handleInput()
        if (self.left):
            self.left = False
            return self.world.GAMESTATE.reverse_mapping[0]
        elif(self.down):
            self.down = False
            SharedEntities.playership.PlayerShip(self)
        elif(self.up):
            self.up = False
            self.guiobjects.GUI(self, "Test", 49, util.TERM_BLUE, [50, 50])
        return self.world.GAMESTATE.reverse_mapping[1]

    def update(self):
        super(GameState, self).update()
        util.BLACK = (120, 120, 120)

    def render(self):
        super(GameState, self).render()
