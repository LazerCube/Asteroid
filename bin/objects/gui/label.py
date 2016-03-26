import pygame

from utilites import util
from objects import objects

class Label(objects.GUI):
    def __init__(self, world, text, fontsize, color, position):
        super(Label, self).__init__(world, text, fontsize, color, position)
        self.hover = True

    def Update(self):
        super(Label, self).Update()
