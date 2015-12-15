import pygame
import util
import worldstate


class GameState(worldstate.WorldState):
    def __init__(self, world):
        super(GameState, self).__init__(world)

    def handleInput(self):
        # super(GameState, self).handleInput()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return self.world.GAMESTATE.reverse_mapping[0]
        return self.world.GAMESTATE.reverse_mapping[1]

    def update(self):
        # super(GameState, self).update()
        self.handleInput()

        util.BLACK = (140, 250, 10)

    def render(self):
        # super(GameState, self).render()
        pass
