
from settings import *
from npc import *

class NPC_Manager:
    def __init__(self, game, npcs) -> None:
        self.game = game
        self.npcs = npcs
        self.npc_list = []

        # populate world with NPC's
        for row in range(len(npcs)):
            for column in range(len(npcs)):
                if npcs[row][column] == 1:
                    self.npc_list.append(NPC(self.game, "art\characters\deep_troll.png", "Troll", 10, 6, 2))
                    self.npc_list[-1].x = column
                    self.npc_list[-1].y = row
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