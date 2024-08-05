import random
import pygame

from settings import *
from helper import *


class NPC:
    def __init__(self, game, path, name, hp, atk, deff, x=1, y=1) -> None:
        self.game = game
        self.name = name
        self.hp = hp
        self.atk = atk
        self.deff = deff
        self.x = x
        self.y = y
        self.tile_size = TILE_SIZE
        
        # try:
        #     self.image = pygame.image.load(path).convert_alpha()
        # except:
        #     self.image = pygame.image.load("art\error.png").convert_alpha()
        self.image = load_image(path)
        self.dead_image = load_image("art\characters\\blood_puddle_red.png")

        self.npc_data = {}

        self.dead = False

    def check_events(self, event):
        pass

    def update(self):
        if not self.dead:
            # Check if collided with player
            if self.x == self.game.player.x:
                if self.y == self.game.player.y:
                    self.game.game_state_manager.set_state("combat")
                    # Randomly cloan itself into the combat list
                    # for i in range(random.randrange(1,4)):
                    #     self.game.combat_manager.add_npcs(self)
                    
                    self.game.combat_manager.add_npcs(self) # Add npc to the combat list
                

            #dx, dy = self.wander()
            dx, dy = self.follow(self.game.player)

            if self.get_wall(dx, dy).solid == False:
                self.x = dx
                self.y = dy

    def follow(self, target):
        # AI state to follow a target
        target_x, target_y = target.x, target.y
        dx, dy = self.x, self.y
        
        if target_x > self.x:
            dx += 1
        else:
            dx -= 1
        if target_y > self.y:
            dy += 1
        else:
            dy -= 1

        return dx, dy

    def wander(self):
        #AI state to wander aimlessly
        dx = self.x + random.randrange(-1,1)
        dy = self.y + random.randrange(-1,1)

        return (dx, dy)
        #print(f"{dx},{dy}")

    def get_wall(self, x, y):
        return self.game.world.world_data[(x,y)]

    def draw(self):
        self.game.display.blit(self.image, ((self.x+self.game.camera_offset_x)*self.tile_size, (self.y+self.game.camera_offset_y)*self.tile_size))


