import pygame

from settings import *
from helper import *

class Textbox:
    def __init__(self, game) -> None:
        self.game = game
        self.buffer = 4
        self.x = 0+self.buffer
        self.y = 200
        self.width = SCALE_WIDTH-(self.buffer*2)
        self.height = SCALE_HEIGHT-self.y-self.buffer

        self.surface = self.game.display

        self.font = game.font_small

        self.text = ""
        self.scroll = 0

    def update_text(self, text):
        self.text = text

    def update(self):
        pass

    def draw(self):
        pygame.draw.rect(self.surface, "black", (self.x, self.y, self.width, self.height))
        pygame.draw.rect(self.surface, "white", (self.x, self.y, self.width, self.height), 1)

        
        draw_text(self.surface, self.text, self.font, "white", self.x+self.buffer, self.y+self.buffer)