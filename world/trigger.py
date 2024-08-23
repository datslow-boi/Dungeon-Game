from helper import *
from settings import *

class Trigger:
    def __init__(self, name, destroy=True) -> None:
        self.name = name
        self.is_active = False
        self.destroy = destroy

        self.x = 0
        self.y = 0

        self.dead = False

class Trigger_Manager:
    def __init__(self, game, triggers) -> None:
        self.game = game
        self.tile_size = TILE_SIZE
        self.triggers = triggers
        self.map = game.world_map
        self.trigger_list = {}
        
        self.load_triggers(self.map, self.triggers)

    def load_triggers(self, map, triggers):
        self.trigger_list = {}
        self.map = map
        self.triggers = triggers

        data = load_json("data/triggers.json")

        # loads triggers in world data to item list
        for row in range(self.map["height"]):
            for column in range(self.map["width"]):
                if str(self.triggers[row][column]) in data:
                    trigger = str(self.triggers[row][column])
                    
                    self.trigger_list[trigger] = Trigger(data[trigger]["name"])
                    self.trigger_list[trigger].x = column
                    self.trigger_list[trigger].y = row

                    if "destroy" in data[trigger]:
                         self.trigger_list[trigger].destroy = data[trigger]["destroy"]

                  
        #print("load trigger", self.trigger_list)
        #print(self.trigger_list)
        #print([f"{i.name}: x={i.x}, y={i.y}" for i in self.trigger_list]) 

                    
    def reset(self):
        for trigger in self.trigger_list:
            self.trigger_list[trigger].active = False


    def update(self):
        for i in self.trigger_list:
            trigger = self.trigger_list[i]
            trigger.is_active = False

            if trigger.dead:
                del self.trigger_list[i]
                break
            
            if self.game.player.x == trigger.x:
                if self.game.player.y == trigger.y:
                    trigger.is_active = True
                    print(trigger.name, "active")

                    if trigger.destroy:
                        trigger.dead = True
                        

                    

    def draw(self):
        if VISABLE_TRIGGER:
            for trigger in self.trigger_list:
                self.game.display.blit(load_image("art\error.png"), 
                                    ((self.trigger_list[trigger].x+self.game.camera_offset_x)*self.tile_size, 
                                    (self.trigger_list[trigger].y+self.game.camera_offset_y)*self.tile_size))

