
from settings import *
from charecter import *

class NPC_Manager:
    def __init__(self, game, npcs) -> None:
        self.game = game
        self.npcs = npcs
        self.npc_list = []

        data = load_json("data/npcs.json")

        # populate world with NPC's
        for i, row in enumerate(self.npcs):
            for t, column in enumerate(self.npcs):
                if str(self.npcs[i][t]) in data:
                    npc = str(self.npcs[i][t])

                    self.npc_list.append(NPC(self.game, data[npc]["path"], 
                                             data[npc]["name"], data[npc]["hp"], 
                                             data[npc]["atk"], data[npc]["deff"], x=t, y=i))
    
                    #print(f"{self.npc_list[-1].name}: ({self.npc_list[-1].x}, {self.npc_list[-1].y})")
        #print(self.npc_list)

    def update(self):
        for npc in range(len(self.npc_list)):
            self.npc_list[npc].update()
        #     print(f"{self.npc_list[npc].name}: ({self.npc_list[npc].x}, {self.npc_list[npc].y})")
        # print("")

    def draw(self):
        for npc in range(len(self.npc_list)):
            self.npc_list[npc].draw()