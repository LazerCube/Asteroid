import pygame
import util
import worldstate
import sprite
import playership


class MenuState(worldstate.WorldState):
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
            playership.PlayerShip(self)
        return self.world.GAMESTATE.reverse_mapping[0]

    def update(self):
        super(MenuState, self).update()
        util.BLACK = (250, 50, 20)

    def render(self):
        super(MenuState, self).render()
