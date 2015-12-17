import pygame
import entities
import util


class GUI(entities.Entities):
    def __init__(self, world, text, fontsize, color, position):
        super(GUI, self).__init__(world)
        self.font = util.DEFAULT_FONT
        self.text = text
        self.fontsize = fontsize
        self.color = color
        self.position = position
        self.hover = False

        self.GUIinfo = pygame.font.SysFont(self.font, self.fontsize)
        self.GUI = self.GUIinfo.render(self.text, True, self.color)

        world.N_GUIobjects += 1
        print("GUI")

    def hover(self):
        pass

    def Update(self):
        super(GUI, self).Update()

    def Draw(self):
        super(GUI, self).Draw()
        self.worldstate.world.SURFACE.blit(self.GUI, self.position)
