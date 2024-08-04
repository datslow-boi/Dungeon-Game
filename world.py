import pygame

from settings import *
from helper import *

map = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,1,0,0,0,1],
    [1,0,0,0,0,1,0,0,0,1],
    [1,0,0,0,0,1,1,0,1,1],
    [1,0,0,0,0,1,0,0,0,1],
    [1,0,0,0,0,1,0,0,0,1],
    [1,1,0,1,1,1,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1]
]
npcs = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0,1,0],
    [0,0,0,0,0,0,0,0,0,0],
]
items = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,2,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
]


class Tile:
    def __init__(self, path, solid=False) -> None:
        self.image = load_image(path)
        self.solid = solid
        

class World:
    def __init__(self, game, map) -> None:
        self.game = game
        self.map = map
        self.tile_size = TILE_SIZE
        self.world_data = {}
        self.wall = Tile("art\enviroment\catacombs_0.png", solid=True)
        self.floor = Tile("art\enviroment\pebble_brown_2_new.png")
    
        self.build_world()
        #print(self.world_data)

    def build_world(self):
        # Populate dictionary with tiles and coords
        for row in range(len(self.map)):
            for column in range(len(self.map)):
                if self.map[row][column] == 0:
                    self.world_data[(column, row)] = self.floor
                else:
                    self.world_data[(column, row)] = self.wall

        
        
    def draw(self):
        for tile in self.world_data:
            self.game.display.blit(self.world_data[tile].image, ((tile[0]+self.game.camera_offset_x)*self.tile_size, (tile[1]+self.game.camera_offset_y)*self.tile_size))
        
