import pygame

from settings import *
from helper import *

class Items:
    # Items!
    def __init__(self, path, name, in_world = False, x=0, y=0) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.in_world = in_world

        # load image
        self.image = load_image(path)

class Consume(Items):
    def __init__(self, path, name, in_world=False, x=0, y=0, heal=0) -> None:
        super().__init__(path, name, in_world, x, y)
        
        self.heal = heal

    def activate(self, target):
        target.hp += self.heal
          


class Item_Manager:
        # Handles items whithin the world space
        def __init__(self, game, items) -> None:
            self.game = game
            self.items = items
            self.tile_size = TILE_SIZE
            self.item_list = []

            data = load_json("data/items.json")

            for i, row in enumerate(self.items):
                for t, column in enumerate(self.items):
                    if str(self.items[i][t]) in data:
                        item = str(self.items[i][t])
                        
                        # Loads in speciface items from file to their position on the map
                        if data[item]["type"] == "equipment":
                            print(f"item: {data[item]["name"]}")
                            self.item_list.append(Items(data[item]["path"], 
                                                        data[item]["name"], in_world=True, x=t, y=i))
                        
                        elif data[item]["type"] == "consume":
                            print(f"consume: {data[item]["name"]}")
                            self.item_list.append(Consume(data[item]["path"], 
                                                        data[item]["name"], in_world=True, x=t, y=i))
                            
                            # Optional peramiters
                            if "heal" in data[item]:
                                self.item_list[-1].heal = data[item]["heal"]
                                print("heal")
                        

        def update(self):
            for item in range(len(self.item_list)):
                # Pick up an item
                if self.game.player.x == self.item_list[item].x:
                        if self.game.player.y == self.item_list[item].y:
                            self.game.inventory_manager.add_item(self.item_list[item])
                            print(f"you picked up {self.item_list[item].name}")
                            self.item_list.pop(item)
                            print(self.game.player.inventory)
                            break

        def draw(self):
            for item in range(len(self.item_list)):
                self.game.display.blit(self.item_list[item].image, ((self.item_list[item].x+self.game.camera_offset_x)*self.tile_size, (self.item_list[item].y+self.game.camera_offset_y)*self.tile_size))