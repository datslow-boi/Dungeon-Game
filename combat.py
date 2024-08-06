import time

import pygame

from helper import *
from settings import *

class Combat_Manager:
    def __init__(self, game) -> None:
        self.game = game
        self.npcs = []

        self.menu_elements = 2
        self.selected_element = 0

        self.font = self.game.font_small

        self.box_text = f"You've been attacked!"

        self.turn = True

    def add_npcs(self, npc):
        self.npcs.append(npc)

    def attack(self, target, atk):
        damage = (atk - target.deff)
        if damage <= 0: damage = 0
        target.hp -= damage

    def check_events(self, event):
        # Player input
        if self.turn:
            if event.type == pygame.KEYDOWN:
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

                # Activate Selected option
                if event.key == pygame.K_e:
                    if self.selected_element == 0:
                        self.attack(self.npcs[0], self.game.player.atk)
                        self.turn = False
                    if self.selected_element == 1:
                        self.game.game_state_manager.set_state("inventory")
                    if self.selected_element == 2:
                        self.game.textbox.update_text(f"You fled the {self.npcs[0].name}")
                        self.npcs = []
                        self.game.game_state_manager.set_state("world")
                        
    
    def update(self):
        # Check if enemies are dead
        for npc in range(len(self.npcs)):
            if self.npcs:
                if self.npcs[npc].hp <= 0:
                    self.npcs[npc].image = self.npcs[npc].dead_image
                    self.npcs[npc].dead = True
                    self.npcs.pop(npc)
                    break
        # Check if all enemies are dead
        if len(self.npcs) == 0:
            self.npcs = []
            self.game.game_state_manager.set_state("world")
            self.game.textbox.update_text("You Survived")

        if not self.turn:
            for npc in range(len(self.npcs)):
                self.attack(self.game.player, self.npcs[npc].atk)
            self.turn = True

        if self.game.player.hp <= 0:
            self.game.game_state_manager.set_state("dead")

    def draw(self):
        if self.turn:
            self.game.display.fill("black")
        else:
            self.game.display.fill("red")

        i = 1 # Number of monsters
        for npc in self.npcs:
            scale = 2
            image_size = TILE_SIZE*scale # Gets size of scaled image
            scale_image = pygame.transform.scale_by(npc.image, (scale,scale)) # Scale enemy sprite
            pos_x = SCALE_WIDTH/(len(self.npcs)+1)*i    # Place Enemy on screen baced on how many enemies there are
            image_x = pos_x-(image_size/2)
            image_y = SCALE_HEIGHT/2-(image_size)

            
            self.game.display.blit(scale_image, (image_x, image_y))
            draw_text(self.game.display, f"{npc.name}  HP: {npc.hp}", self.font, "white", image_x, image_y+image_size)

            i+=1
        
        # Interface Box
        buffer = 4
        box_y = 150
        menu_width = 30
        pygame.draw.rect(self.game.display, "white", (buffer+menu_width+buffer, box_y, SCALE_WIDTH-(buffer*2)-menu_width-buffer, 
                                                      (SCALE_HEIGHT-box_y)-buffer), width=1)
        draw_text(self.game.display, self.box_text, self.font, "white", buffer+menu_width+buffer, box_y)
        # Combat menu
        pygame.draw.rect(self.game.display, "white", (buffer, box_y, 30, (SCALE_HEIGHT-box_y)-buffer), width=1)
        if self.selected_element == 0:
            draw_text(self.game.display, "ATACK", self.font, "yellow", buffer+1, box_y)
        else:
            draw_text(self.game.display, "ATACK", self.font, "white", buffer+1, box_y)
        if self.selected_element == 1:
            draw_text(self.game.display, "ITEMS", self.font, "yellow", buffer+1, box_y+10)
        else:
            draw_text(self.game.display, "ITEMS", self.font, "white", buffer+1, box_y+10)
        if self.selected_element == 2:
            draw_text(self.game.display, "FLEE", self.font, "yellow", buffer+1, box_y+20)
        else:
            draw_text(self.game.display, "FLEE", self.font, "white", buffer+1, box_y+20)

        # Player stat box
        pygame.draw.rect(self.game.display, "white", (SCALE_WIDTH-TILE_SIZE-4, box_y-TILE_SIZE*2-7, TILE_SIZE, TILE_SIZE+35), width=1)
        # Draw Player
        self.game.display.blit(self.game.player.image, (SCALE_WIDTH-TILE_SIZE, box_y-TILE_SIZE*2))
        # Player Stats
        draw_text(self.game.display, self.game.player.name, # Name
                  self.font, "white", SCALE_WIDTH-TILE_SIZE, box_y-TILE_SIZE*2-6)
        draw_text(self.game.display, f"HP: {self.game.player.hp}", # HP
                  self.font, "white", SCALE_WIDTH-TILE_SIZE, box_y-TILE_SIZE)
        draw_text(self.game.display, f"ATK: {self.game.player.atk}", # ATK
                  self.font, "white", SCALE_WIDTH-TILE_SIZE, box_y-TILE_SIZE+8)
        draw_text(self.game.display, f"DEF: {self.game.player.deff}", # DEF
                  self.font, "white", SCALE_WIDTH-TILE_SIZE, box_y-TILE_SIZE+16)
        
        