if __name__ == "__main__":
    quit("запускай только main.py")

import pygame
import objects
import textures

def draw_hp(screen):
    player = objects.get_player()
    '''
    pos_x = 50
    pos_y = 50
    size_x = 100
    size_y = 10
    size_hp = (player.hp / player.hp_max) * size_x
    bg_color = (0,0,0)
    line_color = (0,255,0)
    bg = pygame.Surface((size_x, size_y))
    bg.fill(bg_color)
    line = pygame.Surface((size_hp, size_y))
    line.fill(line_color)
    screen.blit(bg, (pos_x, pos_y))
    screen.blit(line, (pos_x, pos_y))
    '''
    idx = int((1.0 - (player.hp / player.hp_max)) * 8)
    idx = min(idx, 7)
    textures.draw_texture(screen, "hp_" + str(idx), 20, -20, 2)
