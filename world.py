from settings import *
from helper import *


class Tile:
    def __init__(self, name, path, solid=False) -> None:
        self.name = name
        self.image = load_image(path)
        self.solid = solid
        

class World:
    def __init__(self, game, map) -> None:
        self.game = game
        self.map = map
        self.tile_size = TILE_SIZE
        self.world_data = {}
        self.wall = Tile("wall", "art\enviroment\catacombs_0.png", solid=True)
        self.floor = Tile("floor", "art\enviroment\pebble_brown_2_new.png")
    
        self.build_world()
        #print(self.world_data)

    def build_world(self):
        # Populate dictionary with tiles and coords
        data = load_json("data/tiles.json")

        for row in range(len(self.map)):
            for column in range(len(self.map)):
                if str(self.map[row][column]) in data:
                    tile = str(self.map[row][column])
                    self.world_data[(column, row)] = Tile(data[tile]["name"], data[tile]["path"], data[tile]["solid"])


        
        
    def draw(self):
        for tile in self.world_data:
            self.game.display.blit(self.world_data[tile].image, ((tile[0]+self.game.camera_offset_x)*self.tile_size, (tile[1]+self.game.camera_offset_y)*self.tile_size))
        
