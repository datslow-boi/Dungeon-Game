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

class Equipment(Items):
    def __init__(self, path, name, in_world=False, x=0, y=0, atk=0, deff=0, 
                 chest=False, legs=False, head=False, weapon=False) -> None:
        super().__init__(path, name, in_world, x, y)

        # Stats
        self.atk = atk
        self.deff = deff

        # Equipment slots
        self.chest = chest
        self.legs = legs
        self.head = head
        self.weapon = weapon

        self.equipped = False
    
    def equip_item(self, game):
        self.equipped = True
        game.player.atk += self.atk
        game.player.deff += self.deff

        if self.chest:
            game.player.chest_image = self.image
        if self.head:
            game.player.head_image = self.image
        if self.legs:
            game.player.legs_image = self.image

    def unequip_item(self, game):
        self.equipped = False
        game.player.atk -= self.atk
        game.player.deff -= self.deff

        if self.chest:
            game.player.chest_image = None
        if self.head:
            game.player.head_image = None
        if self.legs:
            game.player.legs_image = None
          


class Item_Manager:
        # Handles items whithin the world space
        def __init__(self, game, items) -> None:
            self.game = game
            self.items = items
            self.tile_size = TILE_SIZE
            self.item_list = []

            data = load_json("data/items.json")

            # loads items in world data to item list
            for row in range(len(self.items)):
                for column in range(len(self.items)):
                    if str(self.items[row][column]) in data:
                        item = str(self.items[row][column])
                        
                        if data[item]["type"] == "equipment":
                            self.load_equipment(data, item, row, column)
                        
                        elif data[item]["type"] == "consume":
                            self.load_consume(data, item, row, column)

                            
        def load_equipment(self, data, item, row, column):
            # Loads in speciface items from file to their position on the map  
            print(f"item: {data[item]["name"]}")
            self.item_list.append(Equipment(data[item]["path"], 
                                        data[item]["name"], in_world=True, x=column, y=row))
            
            # Optional peramiters
            if "atk" in data[item]:
                self.item_list[-1].atk = data[item]["atk"]
            if "deff" in data[item]:
                self.item_list[-1].deff = data[item]["deff"]
            if "chest" in data[item]:
                self.item_list[-1].chest = data[item]["chest"]
            if "legs" in data[item]:
                self.item_list[-1].legs = data[item]["legs"]
            if "head" in data[item]:
                self.item_list[-1].head = data[item]["head"]
            if "weapon" in data[item]:
                self.item_list[-1].weapon = data[item]["weapon"]
            
            
        def load_consume(self, data, item, row, column):
            print(f"consume: {data[item]["name"]}")
            self.item_list.append(Consume(data[item]["path"], 
                                        data[item]["name"], in_world=True, x=column, y=row))
            # Optional peramiters
            if "heal" in data[item]:
                self.item_list[-1].heal = data[item]["heal"]
                print("heal")

                        
                        

        def add_item(self, item, x, y):
            self.item_list.append(item)
            item.x = x
            item.y = y
                        

        def update(self):
            for item in range(len(self.item_list)):
                # Pick up an item
                if self.game.player.x == self.item_list[item].x:
                        if self.game.player.y == self.item_list[item].y:
                            self.game.inventory_manager.add_item(self.item_list[item])
                            self.game.textbox.update_text(f"you picked up {self.item_list[item].name}")
                            self.item_list.pop(item)
                            break

        def draw(self):
            for item in range(len(self.item_list)):
                self.game.display.blit(self.item_list[item].image, ((self.item_list[item].x+self.game.camera_offset_x)*self.tile_size, (self.item_list[item].y+self.game.camera_offset_y)*self.tile_size))