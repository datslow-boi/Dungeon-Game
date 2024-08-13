
from settings import *
from charecter import *

class NPC_Manager:
    def __init__(self, game, npcs) -> None:
        self.game = game
        self.npcs = npcs
        self.npc_list = []

        self.map = game.world_map
        
        self.load_npcs(self.map, self.npcs)

    def load_npcs(self, map, npcs):
        self.npc_list = []
        self.map = map
        self.npcs = npcs

        data = load_json("data/npcs.json")

        # populate world with NPC's
        for row in range(self.map["height"]):
            for column in range(self.map["width"]):
                if str(self.npcs[row][column]) in data:
                    npc = str(self.npcs[row][column])

                    self.npc_list.append(NPC(self.game, data[npc]["path"], 
                                             data[npc]["name"], data[npc]["hp"], 
                                             data[npc]["atk"], data[npc]["deff"], x=column, y=row))
    
                    #print(f"{self.npc_list[-1].name}: ({self.npc_list[-1].x}, {self.npc_list[-1].y})")
        #print(self.npc_list)

    def update(self):
        for npc in self.npc_list:
            npc.update()
        #     print(f"{self.npc_list[npc].name}: ({self.npc_list[npc].x}, {self.npc_list[npc].y})")
        # print("")

    def draw(self):
        for npc in range(len(self.npc_list)):
            self.npc_list[npc].draw()