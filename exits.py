from helper import *


class Exits:
    def __init__(self, game) -> None:
        self.game = game
        self.triggers = self.game.trigger_manager.trigger_list
        self.data_list = {}


    def update(self):
        if find_trigger(self.triggers, "3"):
            self.switch_rooms("test_map_2")
            return
        
        elif find_trigger(self.triggers, "4"):
            self.switch_rooms("test_map")
            return


    def switch_rooms(self, map):
        temp_data = {}

        temp_data["items"] = self.game.item_manager.item_list
        temp_data["npcs"] = self.game.npc_manager.npc_list
        #temp_data["triggers"] = {}
        temp_data["triggers"] = self.triggers
        self.data_list[self.game.map_key] = temp_data

        new_map = self.game.world_data[map]
        self.game.map_key = map
        self.game.word_map = new_map
        
        self.game.world.reload_world(new_map)
        
        if map in self.data_list:
            
            self.game.item_manager.item_list = self.data_list[map]["items"]
            self.game.npc_manager.npc_list = self.data_list[map]["npcs"]
            
            #self.game.trigger_manager.tri
            self.game.trigger_manager.trigger_list = self.data_list[map]["triggers"]
            self.triggers = self.game.trigger_manager.trigger_list 
            #print(self.game.trigger_manager.trigger_list)
            self.game.trigger_manager.reset()
            #print(f"trigger list: {map}, {self.data_list[map]["triggers"]}")
            print(f"{self.data_list}")
            
            
            #print(f"temp data: {self.data_list["test_map"]["items"]}")
        else:
            print("new area")
            #self.game.step = True
            self.game.item_manager.load_items(new_map, new_map["items"])
            self.game.npc_manager.load_npcs(new_map, new_map["npcs"])

            self.game.trigger_manager.load_triggers(new_map, new_map["triggers"])
            self.triggers = self.game.trigger_manager.trigger_list
        
        self.game.textbox.triggers = self.triggers
        self.game.textbox.text = f"you travel to {new_map["name"]}"