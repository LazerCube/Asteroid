import pygame

from utilites import util
from objects import objects

class Button(objects.GUI):
    def __init__(self, world, text, fontsize, color, position):
        super(Button, self).__init__(world, text, fontsize, color, position)
        self.hover = True

    def on_click(self):
        print("Nothing Set")

    def fixedUpdate(self):
        super(Button, self).fixedUpdate()
        if(self.mouse_active_press[0]):
            self.on_click()

class PlayButton(Button):
    def __init__(self, world, text, fontsize, color, position):
        super(PlayButton, self).__init__(world, text, fontsize, color, position)

    def on_click(self):
        self.GameEngine.SetState(1)

    def fixedUpdate(self):
        super(PlayButton, self).fixedUpdate()
