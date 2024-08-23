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
            self.game.trigger_manager.update()
            self.game.player.update()
            self.game.npc_manager.update()
            self.game.item_manager.update()
            self.game.textbox.update()
            self.game.world.update()
            self.game.exits.update()
            
            self.game.step = False

    def draw(self):
        self.game.display.fill("black")
        self.game.world.draw()
        #self.troll.draw()
        self.game.item_manager.draw()
        self.game.npc_manager.draw()
        self.game.player.draw()
        self.game.textbox.draw()
        self.game.trigger_manager.draw()

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.__init__()
                self.game.game_state_manager.set_state("title")

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
        
        draw_text(self.game.display, "Space: to continue", self.game.font_small, "white", SCALE_WIDTH/2,(SCALE_HEIGHT/2)+50)
        draw_text(self.game.display, "Esc: to quit", self.game.font_small, "white", SCALE_WIDTH/2,(SCALE_HEIGHT/2)+60)


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


class Title_State(State):
    def __init__(self, display, game_state_manager) -> None:
        super().__init__(display, game_state_manager)
        self.game = game_state_manager.game

    def check_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.game_state_manager.set_state("world")

    def update(self):
        pass

    def draw(self):
        self.game.display.fill("black")
        draw_text(self.game.display, "Shadow Tower", self.game.font_title, "yellow", SCALE_WIDTH/2-120,(10))
        draw_text(self.game.display, "Space: to play", self.game.font_small, "white", SCALE_WIDTH/2,(SCALE_HEIGHT/2))
        draw_text(self.game.display, "Esc: to quit", self.game.font_small, "white", SCALE_WIDTH/2,(SCALE_HEIGHT/2+10))


class Win_State(State):
    def __init__(self, display, game_state_manager) -> None:
        super().__init__(display, game_state_manager)
        self.game = game_state_manager.game

    def check_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.__init__()
                self.game.game_state_manager.set_state("title")

    def update(self):
        pass

    def draw(self):
        self.game.display.fill("black")
        draw_text(self.game.display, "Unlimited Power is Yours!", self.game.font_big, "red", SCALE_WIDTH/2-50,(10))

        draw_text(self.game.display, "Thanks for playing!", self.game.font_small, "yellow", SCALE_WIDTH/2-10,30)

        pygame.draw.circle(self.game.display, "white", ((SCALE_WIDTH/2)+TILE_SIZE/2,((SCALE_HEIGHT/2)-(TILE_SIZE*2))+TILE_SIZE/2), TILE_SIZE)
        self.game.player.draw_player(SCALE_WIDTH/2,(SCALE_HEIGHT/2)-(TILE_SIZE*2))
        

        draw_text(self.game.display, "Space: to continue", self.game.font_small, "white", SCALE_WIDTH/2,(SCALE_HEIGHT/2))
        draw_text(self.game.display, "Esc: to quit", self.game.font_small, "white", SCALE_WIDTH/2,(SCALE_HEIGHT/2+10))


class Generator_State(State):
    def __init__(self, display, game_state_manager) -> None:
        super().__init__(display, game_state_manager)
        self.game = game_state_manager.game

    def check_events(self, event):
        self.game.generator.check_events(event)

    def update(self):
        pass

    def draw(self):
        self.game.display.fill("black")
        self.game.world.draw()