import pygame

from vesta.objects.objects import GUI

class Button(GUI):
    def __init__(self, world, text, fontsize, color, position):
        super(Button, self).__init__(world, text, fontsize, color, position)
        self.hover = True

    def on_click(self):
        pass

    def fixed_update(self):
        super(Button, self).fixed_update()
        if(self.mouse_active_press[0]):
            self.on_click()

class PlayButton(Button):
    def on_click(self):
        self.GameEngine.set_state(1)

class ExitToMainMenuButton(Button):
    def on_click(self):
        self.GameEngine.set_state(0)

class ExitButton(Button):
    def on_click(self):
        self.GameEngine.EXIT = True

class ResetButton(Button):
    def on_click(self):
        self.worldstate.reset_world()
