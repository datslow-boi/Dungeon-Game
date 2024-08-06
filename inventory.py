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

        self.equipped_items = []

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
                if self.selected_element >= self.menu_elements-1:
                    self.selected_element = 0
                else:
                    self.selected_element += 1
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                if self.selected_element <= 0:
                    self.selected_element = self.menu_elements-1
                else:
                    self.selected_element -= 1

            # Use item
            try:
                current_item = self.items[self.selected_element]
            except:
                current_item = None

            if event.key == pygame.K_e:
                if self.items:
                    if current_item and isinstance(current_item, Consume):
                        current_item.activate(self.game.player)
                        self.game.textbox.update_text(f"You used {current_item.name}")
                        self.items.pop(self.selected_element)
                        
                    if current_item and isinstance(current_item, Equipment):
                        

                        
                        
                        if not current_item.equipped:
                            for item in self.equipped_items:
                                if current_item.weapon and current_item.weapon == item.weapon:
                                    return
                                if current_item.chest and current_item.chest == item.chest:
                                    return
                                if current_item.legs and current_item.legs == item.legs:
                                    return
                                if current_item.head and current_item.head == item.head:
                                    return
                                
                            self.game.textbox.update_text(f"You equipped {current_item.name}")
                            current_item.equip_item(self.game)
                            self.equipped_items.append(current_item)
                        else:
                            self.game.textbox.update_text(f"You dropped {current_item.name}")
                            current_item.unequip_item(self.game)
                            self.equipped_items.remove(current_item)

            # Drop item
            if event.key == pygame.K_x:
                if current_item:
                    if isinstance(current_item, Equipment) and current_item.equipped:
                        current_item.unequip_item(self.game)
                        self.equipped_items.remove(current_item)
                    self.drop_item(current_item)
                

            

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
            if isinstance(item, Equipment) and item.equipped:
                color = "green"
            if i == self.selected_element:
                color = "yellow"
            draw_text(self.game.display, item.name, self.font_small, color, self.x, self.y+(i*10))

        
        box_y = 150
        # Player stat box
        pygame.draw.rect(self.game.display, "white", (SCALE_WIDTH-TILE_SIZE-4, box_y-TILE_SIZE*2-7, TILE_SIZE, TILE_SIZE+35), width=1)
        # Draw Player
        self.game.player.draw_player(SCALE_WIDTH-TILE_SIZE, box_y-TILE_SIZE*2)
        # Player Stats
        draw_text(self.game.display, self.game.player.name, # Name
                  self.font_small, "white", SCALE_WIDTH-TILE_SIZE, box_y-TILE_SIZE*2-6)
        draw_text(self.game.display, f"HP: {self.game.player.hp}", # HP
                  self.font_small, "white", SCALE_WIDTH-TILE_SIZE, box_y-TILE_SIZE)
        draw_text(self.game.display, f"ATK: {self.game.player.atk}", # ATK
                  self.font_small, "white", SCALE_WIDTH-TILE_SIZE, box_y-TILE_SIZE+8)
        draw_text(self.game.display, f"DEF: {self.game.player.deff}", # DEF
                  self.font_small, "white", SCALE_WIDTH-TILE_SIZE, box_y-TILE_SIZE+16)