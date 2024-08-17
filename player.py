import pygame

from charecter import *
from world import *
from items import *
from settings import *
from helper import *


class Player(Charecter):
    def __init__(self, game, path, name, hp, atk, deff, x, y) -> None:
        super().__init__(game, path, name, hp, atk, deff, x, y)
        self.draw_x = x
        self.draw_y = y
        self.tile_size = TILE_SIZE
        self.image = load_image(path)

        self.chest_image = None
        self.legs_image = None
        self.head_image = None

        self.inventory = []

    def check_events(self, event):
        dx, dy = 0, 0
        # Player input
        if event.type == pygame.KEYDOWN:
            # Movement
            if event.key == pygame.K_d:
                self.check_wall(1, 0)
                
            if event.key == pygame.K_a:
                self.check_wall(-1, 0)

            if event.key == pygame.K_w:
                self.check_wall(0, -1)

            if event.key == pygame.K_s:
                self.check_wall(0, 1)


            # Inventory
            if event.key == pygame.K_i:
                self.game.game_state_manager.set_state("inventory")

            # Step
            if event.key == pygame.K_SPACE:
                self.game.step = True


    def check_wall(self, dx, dy):
        wall = self.get_wall(self.x+dx, self.y+dy)
        if not wall.solid:
            self.move_player(dx, dy)
        
        elif isinstance(wall, Door) and wall.locked:
            self.check_door(wall)

    def move_player(self, dx, dy):
        self.game.step = True
        self.game.camera_offset_x += (dx*-1)    #Camera needs to be inverted
        self.game.camera_offset_y += (dy*-1)
        self.x += dx
        self.y += dy

    def check_door(self, wall):
        if self.get_key(wall.id):
            wall.unlock_door()
            self.game.textbox.text = "unlocked door"
        else:
            self.game.textbox.text = "locked"

    def get_wall(self, x, y):
        return self.game.world.world_data[(x,y)]

    def get_xy(self):
        return int(self.x), int(self.y)
    
    def get_key(self, id):
        for item in self.inventory:
            if isinstance(item, Key) and item.id == id:
                self.inventory.remove(item)
                return True
            
        return False
    
    def update(self):
        self.inventory = self.game.inventory_manager.items
    
    def draw_player(self, x, y):
        self.game.display.blit(self.image, (x, y))

        if self.legs_image:
            self.game.display.blit(self.legs_image, (x, y))
        if self.chest_image:
            self.game.display.blit(self.chest_image, (x, y))
        if self.head_image:
            self.game.display.blit(self.head_image, (x, y))

    def draw(self):
        center_x = (SCALE_WIDTH / 2) // self.tile_size
        center_y = (SCALE_HEIGHT/ 2) // self.tile_size
        self.draw_x = center_x*self.tile_size
        self.draw_y = center_y*self.tile_size
        
        self.draw_player(self.draw_x, self.draw_y)