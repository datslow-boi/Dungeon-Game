import json

import pygame

def draw_text(screen, text, font, color, x, y):
    image = font.render(text, False, color)

    screen.blit(image, (x, y))

def load_image(path):
    try:
        image =  pygame.image.load(path).convert_alpha()
    except:
        image = pygame.image.load("art\error.png").convert_alpha()
    return image

def load_json(path):
    with open(path, "r") as file:
        return json.load(file)
    
def find_trigger(list, trigger, destroy=False):
    # if destroy:
    #     del list[trigger]
    #     return True
    if trigger in list and list[trigger].is_active == True:
        return True
    