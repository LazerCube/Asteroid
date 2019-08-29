import pygame

from vesta.objects.objects import GUI

class Label(GUI):
    def __init__(self, world, text, fontsize, color, position):
        super(Label, self).__init__(world, text, fontsize, color, position)
        self.hover = False

class ValueLabel(Label):
    def __init__(self, world, text, fontsize, color, position, start_value=0):
        super(ValueLabel, self).__init__(world, text, fontsize, color, position)
        self.value = start_value

    def update(self, delta):
        self.add_text(("%s: %s" %(self.text, self.value)) , self.fontsize, self.color)
        super(Label, self).update(delta)
