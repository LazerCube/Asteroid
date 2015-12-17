import world
import SharedEntities.playership

import pygame
import util


class MenuState(world.WorldState):
    def __init__(self, world):
        super(MenuState, self).__init__(world)
        self.n_players = 0

    def handleInput(self):
        super(MenuState, self).handleInput()
        if (self.right):
            self.right = False
            return self.world.GAMESTATE.reverse_mapping[1]
        elif(self.down):
            self.down = False
            SharedEntities.playership.PlayerShip(self)
        elif(self.up):
            self.up = False
            self.guiobjects.GUI(self, "Test", 50, util.TERM_BLUE, [50, 50])
        return self.world.GAMESTATE.reverse_mapping[0]

    def update(self):
        super(MenuState, self).update()
        util.BLACK = (250, 50, 20)

    def render(self):
        super(MenuState, self).render()
