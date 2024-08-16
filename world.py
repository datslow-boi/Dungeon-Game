import math

import pygame

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

        self.occlude_list = []
        self.caster_ist = []

        self.build_world()
        #print(self.world_data)

    def build_world(self):
        # Populate dictionary with tiles and coords
        #print("build world")
        data = load_json("data/tiles.json")

        for row in range(self.map["height"]):
            for column in range(self.map["width"]):
                if str(self.map["map"][row][column]) in data:
                    tile = str(self.map["map"][row][column])
                    self.world_data[(column, row)] = Tile(data[tile]["name"], data[tile]["path"], data[tile]["solid"])
                else:
                    # if the tile doesn't exist add an error tile
                    self.world_data[(column, row)] = Tile(data["default"]["name"], data["default"]["path"], data["default"]["solid"])
        #print(self.map["width"], self.map["height"])
    
    def reload_world(self, map):
        self.world_data = {}
        self.map = map
        self.build_world()

    def update(self):
        
        #print(self.occlude_list)
        
        self.occlude_list = []
        if SHADOW:
            self.draw_shadows()
            self.draw_walls()

    """Beguining of the shadow casting shit"""
    def draw_shadows(self):
        px, py = self.game.player.x, self.game.player.y
        dx, dy = self.game.player.draw_x, self.game.player.draw_y
        
        slope = (1, 1) # (x, y) not rize/run
        self.generate_octants(slope, px, py, True, "red")
        self.generate_octants(slope, px, py, False, "red")
        slope = (1, -1)
        self.generate_octants(slope, px, py, True, "green")
        self.generate_octants(slope, px, py, False, "green")
        slope = (-1, 1)
        self.generate_octants(slope, px, py, True, "blue")
        self.generate_octants(slope, px, py, False, "blue")
        slope = (-1, -1)
        self.generate_octants(slope, px, py, True, "yellow")
        self.generate_octants(slope, px, py, False, "yellow")

        # for tile in self.occlude_list:
        #     self.draw_octants((tile[0]-py, tile[1]-py), tile[0], tile[1], True, "white", shadow=True)
        
    def draw_walls(self):
        # please fix!
        _visible_list = []
        for tile in self.world_data:
            if tile in self.occlude_list:
                continue
            else:
                _visible_list.append(tile)
        
        for tile in _visible_list:
            if (tile[0]-1, tile[1]) in self.occlude_list:
                if (tile[0]-1, tile[1]) in self.world_data: # left
                    if self.world_data[(tile[0]-1, tile[1])].solid:
                        self.occlude_list.remove(((tile[0]-1, tile[1])))
            
            elif (tile[0]+1, tile[1]) in self.occlude_list:
                if (tile[0]+1, tile[1]) in self.world_data: # Right
                    if self.world_data[(tile[0]+1, tile[1])].solid:
                        self.occlude_list.remove(((tile[0]+1, tile[1])))
            
            elif (tile[0], tile[1]-1) in self.occlude_list:
                if (tile[0], tile[1]-1) in self.world_data: # Up
                    if self.world_data[(tile[0], tile[1]-1)].solid:
                        self.occlude_list.remove(((tile[0], tile[1]-1)))
            
            elif (tile[0], tile[1]+1) in self.occlude_list:
                if (tile[0], tile[1]+1) in self.world_data: # Down
                    if self.world_data[(tile[0], tile[1]+1)].solid:
                        self.occlude_list.remove(((tile[0], tile[1]+1)))
                              
    def generate_octants(self, slope, x, y, horizontal, color, shadow=False, first_step=True):
        """If there is a god, I beg for forgivness for what ive done here.  Also sorry future Ben."""
        view_distance = 10
        row = 0
        col = 0
        x_slope = slope[0]
        y_slope = slope[1]
        dx =  1 if x_slope > 0 else -1
        dy = -1 if y_slope > 0 else 1
        for i in range(view_distance):
            if horizontal:
                for scan_x in range(abs(x_slope)+1):
                    tile_x = (x+self.game.camera_offset_x) + ((x_slope-(scan_x*dx)))
                    tile_y = (y+self.game.camera_offset_y) + ((i*dy))

                    draw_x = tile_x * self.tile_size
                    draw_y = tile_y * self.tile_size

                    pos = int(x + ((x_slope-(scan_x*dx)))), int(y+ ((i*dy)))
                    
                    if not shadow:
                        if pos in self.world_data:
                            if self.world_data[pos].solid:
                                if pos not in self.occlude_list:
                                    self.generate_octants((pos[0]-x, (pos[1]-y)*-1), pos[0], pos[1], True, "white", shadow=True)
                                    #print(f"Slope: {(pos[0]-x, pos[1]-y)}, x: {pos[0]}, y: {pos[1]}")
                                #pygame.draw.rect(self.game.display, color, (draw_x, draw_y, self.tile_size, self.tile_size))   
                    else:
                        #pygame.draw.rect(self.game.display, color, (draw_x, draw_y, self.tile_size, self.tile_size))   
                        
                        
                        
                        if pos not in self.occlude_list:
                            self.occlude_list.append(pos)
                
                  
                            
            else:
                for scan_y in range(abs(y_slope)+1):
                    tile_x = ((x+dx)+self.game.camera_offset_x) + ((i*dx))
                    tile_y = (y+self.game.camera_offset_y) + ((y_slope+(scan_y*dy)))
                    
                    draw_x = tile_x * self.tile_size
                    draw_y = tile_y * self.tile_size

                    pos = int((x+dx) + ((i*dx))), int(y+ ((y_slope+(scan_y*dy))))
                    if not shadow:
                        if pos in self.world_data:
                            if self.world_data[pos].solid:
                                if pos not in self.occlude_list:
                                    self.generate_octants((pos[0]-x, (pos[1]-y)*-1), pos[0], pos[1], True, "white", shadow=True)
                                    #pygame.draw.rect(self.game.display, color, (draw_x, draw_y, self.tile_size, self.tile_size))
                    else:
                        #pygame.draw.rect(self.game.display, color, (draw_x, draw_y, self.tile_size, self.tile_size))   
                        
                        
                        if pos not in self.occlude_list:
                            self.occlude_list.append(pos)
               

            try:
                if row % slope[1] == 0:
                    x_slope += slope[0]
                    #print(x_slope)
                if col % slope[0] == 0:
                    y_slope += slope[1]
                    #print(y_slope)

                    row+=1
                    col+=1
            except:
                row+=1
                col+=1
        


    def draw(self):
        
        for tile in self.world_data:
            if tile not in self.occlude_list:
                self.game.display.blit(self.world_data[tile].image, ((tile[0]+self.game.camera_offset_x)*self.tile_size, (tile[1]+self.game.camera_offset_y)*self.tile_size))
            else:
                continue
