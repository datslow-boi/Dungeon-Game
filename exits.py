from helper import *


class Exits:
    def __init__(self, game) -> None:
        self.game = game
        self.triggers = self.game.trigger_manager.trigger_list



    def update(self):
        if find_trigger(self.triggers, "3"):
            self.switch_rooms("test_map_2")
            return
        
        elif find_trigger(self.triggers, "4"):
            self.switch_rooms("test_map")
            return


    def switch_rooms(self, map):
        new_map = self.game.world_data[map]
        self.game.word_map = new_map
        
        self.game.world.reload_world(new_map)
        self.game.item_manager.load_items(new_map, new_map["items"])
        self.game.npc_manager.load_npcs(new_map, new_map["npcs"])

        self.game.trigger_manager.load_triggers(self.game_map, self.game_map["triggers"])
        self.triggers = self.game.trigger_manager.trigger_list
        
        self.game.textbox.text = f"you travel to {new_map["name"]}"
