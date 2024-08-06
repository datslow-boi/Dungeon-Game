import pygame

from settings import *
from helper import *
from items import *

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

        self.menu_elements = 0
        self.selected_element = 0

    def add_item(self, item):
        self.items.append(item)

    def drop_item(self, item):
        self.game.item_manager.add_item(item, self.game.player.x, self.game.player.y)
        self.game.textbox.update_text(f"You dropped {item.name}")
        self.items.remove(item)

    def check_events(self, event):
        if event.type == pygame.KEYDOWN:
            # Exit Inventory
            if event.key == pygame.K_i:
                self.game.step = False
                self.game.game_state_manager.set_state(self.game.game_state_manager.previous_state)

    
            # Select item in menu
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                if self.selected_element >= self.menu_elements:
                    self.selected_element = 0
                else:
                    self.selected_element += 1
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                if self.selected_element <= 0:
                    self.selected_element = self.menu_elements
                else:
                    self.selected_element -= 1

            # Use item
            if event.key == pygame.K_e:
                if self.items:
                    if isinstance(self.items[self.selected_element], Consume):
                        self.items[self.selected_element].activate(self.game.player)
                        self.game.textbox.update_text(f"You used {self.items[self.selected_element].name}")
                        self.items.pop(self.selected_element)

            # Drop item
            if event.key == pygame.K_x:
                self.drop_item(self.items[self.selected_element])

            

    def update(self):
        self.menu_elements = len(self.items)

    def draw(self):
        self.game.display.fill("black")

        pygame.draw.rect(self.game.display, "white", (self.x, self.y, self.width, self.height), width=1, border_radius=3)

        draw_text(self.game.display, "Inventory", self.font_big, "yellow", self.x, self.y-20)
        draw_text(self.game.display, "X: drop E: use", self.font_small, "white", self.x, self.y+self.height+5)

        # Item List
        for i, item in enumerate(self.items):
            color = "white"
            if i == self.selected_element:
                color = "yellow"
            draw_text(self.game.display, item.name, self.font_small, color, self.x, self.y+(i*10))