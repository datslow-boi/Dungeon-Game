import pygame

from helper import *
from settings import *

class Game_State_Manager:
    def __init__(self, game, current_state) -> None:
        self.game = game
        self.current_state = current_state

        self.previous_state = current_state

    def get_state(self):
        return self.current_state
    
    def set_state(self, new_state):
        self.previous_state = self.current_state
        self.current_state = new_state


class State:
    def __init__(self, display, game_state_manager) -> None:
        self.display = display
        self.game_state_manager = game_state_manager


class World_State(State):
    def __init__(self, display, game_state_manager) -> None:
        super().__init__(display, game_state_manager)
        self.game = game_state_manager.game

    def check_events(self, event):
        self.game.player.check_events(event)

    def update(self):
        if self.game.step:
            #self.troll.update()
            self.game.npc_manager.update()
            self.game.item_manager.update()
            self.game.step = False

    def draw(self):
        self.game.display.fill("black")
        self.game.world.draw()
        #self.troll.draw()
        self.game.item_manager.draw()
        self.game.npc_manager.draw()
        self.game.player.draw()
        self.game.textbox.draw()

# States
class Combat_State(State):
    def __init__(self, display, game_state_manager) -> None:
        super().__init__(display, game_state_manager)
        self.game = game_state_manager.game

    def check_events(self, event):
        self.game.combat_manager.check_events(event)

    def update(self):
        self.game.combat_manager.update()

    def draw(self):
        self.game.display.fill("black")
        self.game.combat_manager.draw()

class Dead_State(State):
    def __init__(self, display, game_state_manager) -> None:
        super().__init__(display, game_state_manager)
        self.game = game_state_manager.game

    def check_events(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        self.game.display.fill("black")
        blood = load_image("art\characters\\blood_puddle_red.png")
        self.game.display.blit(blood, (SCALE_WIDTH/2, SCALE_HEIGHT/2))
        player_image = pygame.transform.rotate(self.game.player.image, 90)
        self.game.display.blit(player_image, (SCALE_WIDTH/2, SCALE_HEIGHT/2))

        draw_text(self.game.display, "You Died!", self.game.font_big, "red", SCALE_WIDTH/2,(SCALE_HEIGHT/2)-20)
        draw_text(self.game.display, "Death comes with clarity.  If only you understood sooner.", 
                  self.game.font_small, "white", (SCALE_WIDTH/2)-40,(SCALE_HEIGHT/2)+30)


class Inventory_State(State):
    def __init__(self, display, game_state_manager) -> None:
        super().__init__(display, game_state_manager)
        self.game = game_state_manager.game

    def check_events(self, event):
        self.game.inventory_manager.check_events(event)

    def update(self):
        self.game.inventory_manager.update()

    def draw(self):
        self.game.inventory_manager.draw()