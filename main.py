import sys

import pygame


from world import *
from charecter import *
from states import *
from gui import *

from helper import *
from settings import *


from experamental import *

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()

        self.display = pygame.Surface((RES_SCALE))
        self.gui = pygame.Surface(RES_SCALE)
        
        # Init fonts
        self.font_title = pygame.font.SysFont("Arial", 40)
        self.font_big = pygame.font.SysFont("Arial", 15)
        self.font_small = pygame.font.SysFont("Arial", 8)

        self.step = False   # Turns

        # World position ofset by camera position
        self.camera_offset_x = 0 
        self.camera_offset_y = 0

        self.world_data = load_json("data/world_data.json")
        self.map_key = "test_map"
        self.world_map = self.world_data[self.map_key]

        self.new_game()

        
    def new_game(self):

        self.world = World(self, self.world_map)
        self.temp_world = {}
        #print(self.world_map["map"])
        
        # World entities
        self.player = Player(self, "art\characters\human_female.png", "Ben", 20, 5, 3, 1, 1)
        self.npc_manager = NPC_Manager(self, self.world_map["npcs"])
        self.item_manager = Item_Manager(self, self.world_map["items"])
        self.combat_manager = Combat_Manager(self)
        self.inventory_manager = Inventory_manager(self)
        self.trigger_manager = Trigger_Manager(self, self.world_map["triggers"])
        self.textbox = Textbox(self)
        self.exits = Exits(self)
        #self.generator = Generator(self, 30, 30, 69, backtracking=False)

        # Game States
        self.game_state_manager = Game_State_Manager(self, "title")
        self.world_state = World_State(self.screen, self.game_state_manager)
        self.combat_state = Combat_State(self.screen, self.game_state_manager)
        self.dead_state = Dead_State(self.screen, self.game_state_manager)
        self.inventory_state = Inventory_State(self.screen, self.game_state_manager)
        self.title_state = Title_State(self.screen, self.game_state_manager)
        self.win_state = Win_State(self.screen, self.game_state_manager)
        self.generator_state = Generator_State(self.screen, self.game_state_manager)

        self.states = {"world"      : self.world_state, 
                       "combat"     : self.combat_state, 
                       "dead"       : self.dead_state,
                       "inventory"  : self.inventory_state,
                       "title"      : self.title_state,
                       "win"        : self.win_state,
                       "generator"  : self.generator_state}

        #center camera
        _ox, _oy = self.player.get_xy()
        #print(_ox, _oy)
        self.camera_offset_x -= _ox - (SCALE_WIDTH / 2) // TILE_SIZE
        self.camera_offset_y -= _oy - (SCALE_HEIGHT / 2) // TILE_SIZE


    def update(self):
        self.states[self.game_state_manager.get_state()].update() # Update the state we're in

        pygame.display.flip() # Refresh game
        self.clock.tick(FPS)
        pygame.display.set_caption(f"{self.clock.get_fps() :.1f}")

    def draw(self):
        self.states[self.game_state_manager.get_state()].draw() # Draw the state we're in

        surf = pygame.transform.scale(self.display, (RES)) # scale the sceen
        
        self.screen.blit(surf, (0, 0))


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            self.states[self.game_state_manager.get_state()].check_events(event) 
            #self.player.check_events(event)

    def run(self):
        # Game loop
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == "__main__":
    game = Game()
    game.run()