import random

import pygame

class Generator:
    def __init__(self, game, width, height, seed, backtracking=True) -> None:
        self.game = game
        self.width = width
        self.height = height
        self.seed = seed
        self.backtracking = backtracking

        self.game.camera_offset_x -= self.width/2
        self.game.camera_offset_y -= self.height/2

        self.tile_map = []
        self.open_space = []

        self.gen_tilemap()

        self.drunken_walk()

    def gen_tilemap(self):
        self.open_space = []
        self.tile_map = []
        for row in range(self.height):
            _map = []
            for column in range(self.width):
                _map.append(1)
            self.tile_map.append(_map)

    def send_world(self):
        temp_data = {"name" : "gen map", "width" : self.width, "height" : self.height}
        temp_data["map"] = self.tile_map
        #print(temp_data)

        self.game.world.world_data = temp_data["map"]
        self.game.world.reload_world(temp_data)


    def drunken_walk(self):
        x, y = int(self.width/2), int(self.height/2)
        
        length = random.randint(10, 50)
        self.walker(x,y, length)
        for i in range(20):
            start = random.choice(self.open_space)
            print(start)
            length = random.randint(10, 50)
            self.walker(start[0], start[1], length)


        self.send_world()

    def walker(self, initial_x, initial_y, length):
        x, y = initial_x, initial_y
        self.tile_map[y][x] = 0
        
        up = -1
        down = 1
        left = -1
        right = 1

        if not self.backtracking: 
            direction = ["up", "down", "left", "right"]
            direction = random.choice(direction)
            if direction == "up":
                down = 0
            elif direction == "down":
                up = 0
            elif direction == "left":
                right = 0
            elif direction == "right":
                left = 0

        for i in range(length):
            dx, dy = random.randint(up,down), random.randint(left,right)
            
            hor = bool(random.randint(0,1))
            if hor:
                x+=dx
            else:
                y+=dy
            
            try:
                if self.tile_map[y][x]:
                    self.tile_map[y][x] = 0
                    if ((x,y)) not in self.open_space:
                        self.open_space.append((x,y))
            except:
                return

    def check_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.gen_tilemap()
                self.drunken_walk()
