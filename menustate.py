import pygame
import util
import worldstate


class MenuState(worldstate.WorldState):
    def __init__(self, world):
        super(MenuState, self).__init__(world)
        self.escape = False

    def handleInput(self):
        super(MenuState, self).handleInput()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return self.world.GAMESTATE.reverse_mapping[1]
        return self.world.GAMESTATE.reverse_mapping[0]

    def update(self):
        super(MenuState, self).update()
        self.handleInput()

        util.BLACK = (250, 50, 20)

    def render(self):
        # super(MenuState, self).render()
        pass
