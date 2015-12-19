import entities

import pygame
import util


class GUI(entities.Entities):
    def __init__(self, world, text, fontsize, color, position):
        super(GUI, self).__init__(world)
        self.scale = 1
        self.angle = 0
        self.text = text
        self.fontsize = fontsize
        self.font = util.DEFAULT_FONT
        self.GUI_size = [0, 0]
        self.GUI_center = [0, 0]
        self.position = position
        self.new_position = position
        self.text = text
        self.fontsize = fontsize
        self.color = color
        self.GUIinfo = None
        self.GUI = None

        self.addtext(self.text, self.fontsize, self.color)
        world.N_GUIobjects += 1

    def addtext(self, text, fontsize, color):
        self.GUIinfo = pygame.font.SysFont(self.font, fontsize)
        self.GUI = self.GUIinfo.render(text, True, color)

        self.GUI_size = [(self.GUI.get_width()), (self.GUI.get_height())]
        self.GUI_center = [((self.GUI_size[0])/2), ((self.GUI_size[1])/2)]

        self.updatehitbox()

    def updatehitbox(self):
        self.new_position = [int(self.position[0] - self.GUI_center[0]),
                             int(self.position[1] - self.GUI_center[1])]

        a = [int(-self.GUI_center[0]), (-self.GUI_center[1])]
        b = [int(self.GUI_center[0]), (-self.GUI_center[1])]
        c = [int(self.GUI_center[0]), (self.GUI_center[1])]
        d = [int(-self.GUI_center[0]), (self.GUI_center[1])]

        self.hitbox[0] = a
        self.hitbox[1] = b
        self.hitbox[2] = b
        self.hitbox[3] = c
        self.hitbox[4] = c
        self.hitbox[5] = d
        self.hitbox[6] = d
        self.hitbox[7] = a

        super(GUI, self).updatehitbox()

    def handleInput(self):
        super(GUI, self).handleInput()
        if(self.hover):
            self.addtext(self.text, self.fontsize, util.RED)
            if(self.worldstate.mouse_pressed[0]):
                self.position = self.worldstate.mouse_pos
                self.updatehitbox()
        else:
            self.addtext(self.text, self.fontsize, self.color)

    def Update(self):
        super(GUI, self).Update()

    def Draw(self):
        super(GUI, self).Draw()
        self.worldstate.world.SURFACE.blit(self.GUI, self.new_position)
