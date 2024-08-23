
from settings import *
from charecter.npc import *

class NPC_Manager:
    def __init__(self, game, npcs) -> None:
        self.game = game
        self.npcs = npcs
        self.npc_list = []
        self.nav_map = []
        #self.generate_nav_map()

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
                                             data[npc]["atk"], data[npc]["deff"], data[npc]["state"], x=column, y=row))
    
                    #print(f"{self.npc_list[-1].name}: ({self.npc_list[-1].x}, {self.npc_list[-1].y})")
        #print(self.npc_list)

    def update(self):
        self.generate_nav_map()

        for npc in self.npc_list:
            npc.update()
        
        
        #print(self.nav_map)

    def generate_nav_map(self):
        # Generate nave map for npc pathfinding
        width = self.game.world.width
        height = self.game.world.height
        for row in range(height):
            _list = []
            for col in range(width):
                tile = list(self.game.world.world_data)[col+(row*width)]
                
                if self.game.world.world_data[tile].solid:
                    _list.append(0)
                else:
                    _list.append(1)
            
            self.nav_map.append(_list)

    def draw(self):
        for npc in range(len(self.npc_list)):
            self.npc_list[npc].draw()