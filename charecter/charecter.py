from settings import *
from helper import *

class Charecter:
    def __init__(self, game, path, name, hp, atk, deff, x=1, y=1) -> None:
        self.game = game
        self.name = name
        self.hp = hp
        self.atk = atk
        self.deff = deff
        self.x = x
        self.y = y

        self.inventory = []

        self.tile_size = TILE_SIZE
        self.image = load_image(path)




