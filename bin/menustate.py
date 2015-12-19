import world

import pygame
import util


class MenuState(world.WorldState):
    def __init__(self, world):
        super(MenuState, self).__init__(world)
        self.guiobjects.GUI(self, "MENU", 60, util.TERM_BLUE,
                            [self.world.WIDTH / 2, 30])

    def handleInput(self):
        super(MenuState, self).handleInput()
        if (self.right):
            self.right = False
            return self.world.GAMESTATE.reverse_mapping[1]
        return self.world.GAMESTATE.reverse_mapping[0]

    def update(self):
        super(MenuState, self).update()
        util.BLACK = (0, 0, 0)

    def render(self):
        super(MenuState, self).render()
