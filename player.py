import pygame

from charecter import *
from settings import *
from helper import *


class Player(Charecter):
    def __init__(self, game, path, name, hp, atk, deff, x, y) -> None:
        super().__init__(game, path, name, hp, atk, deff, x, y)
        self.draw_x = x
        self.draw_y = y
        self.tile_size = TILE_SIZE
        self.image = load_image(path)

        self.inventory = []

    def check_events(self, event):
        # Player input
        if event.type == pygame.KEYDOWN:
            self.game.step = True
            # Movement
            if event.key == pygame.K_d and self.get_wall(self.x+1, self.y).solid == False:
                    self.game.camera_offset_x -= 1
                    self.x += 1
                
            if event.key == pygame.K_a and self.get_wall(self.x-1, self.y).solid == False:
                self.x -= 1
                self.game.camera_offset_x += 1
            if event.key == pygame.K_w and self.get_wall(self.x, self.y-1).solid == False:
                self.y -= 1
                self.game.camera_offset_y += 1
            if event.key == pygame.K_s and self.get_wall(self.x, self.y+1).solid == False:
                self.y += 1
                self.game.camera_offset_y -= 1

            # Inventory
            if event.key == pygame.K_i:
                self.game.game_state_manager.set_state("inventory")

    def get_wall(self, x, y):
        return self.game.world.world_data[(x,y)]

    def get_xy(self):
        return int(self.x), int(self.y)

    def draw(self):
        self.draw_x = (SCALE_WIDTH / 2) // TILE_SIZE
        self.draw_y = (SCALE_HEIGHT/ 2) // TILE_SIZE
        self.game.display.blit(self.image, (self.draw_x*self.tile_size, self.draw_y*self.tile_size))