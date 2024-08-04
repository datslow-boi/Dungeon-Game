import pygame

from settings import *
from helper import *

class Inventory_manager:
    def __init__(self, game) -> None:
        self.game = game

        self.items = []

        self.font_big = game.font_big
        self.font_small = game.font_small

        self.x = SCALE_WIDTH/2
        self.y = 20
        self.width = 60
        self.height = SCALE_HEIGHT/2

    def add_item(self, item):
        self.items.append(item)

    def check_events(self, event):
        if event.type == pygame.KEYDOWN:
            # Exit Inventory
            if event.key == pygame.K_i:
                self.game.game_state_manager.set_state(self.game.game_state_manager.previous_state)
            

    def update(self):
        pass

    def draw(self):
        self.game.display.fill("black")

        pygame.draw.rect(self.game.display, "white", (self.x, self.y, self.width, self.height), width=1, border_radius=3)

        draw_text(self.game.display, "Inventory", self.font_big, "yellow", self.x, self.y-20)

        # Item List
        for i, item in enumerate(self.items):
            draw_text(self.game.display, item.name, self.font_small, "white", self.x, self.y+(i*10))