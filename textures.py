if __name__ == "__main__":
    quit("запускай только main.py")

import pygame

textures = {}

def load_texture(name, path):
    textures[name] = pygame.image.load(path)

def draw_texture(screen, name, x, y, scale=1, angle="left"):
    tex = textures[name]
    size = tex.get_size()
    scaled = pygame.transform.scale(tex, (size[0] * scale, size[1] * scale))
    match angle:
        case "up": degree = 180+90
        case "down": degree = 90
        case "right": degree = 180
        case "left": degree = 0
        case _: degree = 180
    rotated = pygame.transform.rotate(scaled, degree)
    screen.blit(rotated, (x, y))

texture_scale = 3 # масштаб увеличения текстур
texture_size = 12

# загрузка всех текстур
def loading_textures():
    load_texture("1", "data/sprites/1.png")
    load_texture("2", "data/sprites/2.png")
    load_texture("4", "data/sprites/4.png")
    load_texture("5", "data/sprites/5.png")
    load_texture("7", "data/sprites/7.png")
    load_texture("8", "data/sprites/8.png")
    load_texture("9", "data/sprites/9.png")
    load_texture("10", "data/sprites/10.png")
    load_texture("11", "data/sprites/11.png")
    load_texture("12", "data/sprites/12.png")
    load_texture("пол", "data/sprites/16.png")
    load_texture("игрок", "data/sprites/17.png")
    load_texture("31", "data/sprites/31.png")
    load_texture("31", "data/sprites/31.png")
    load_texture("hp_0", "data/sprites/hp/g.png")
    load_texture("hp_1", "data/sprites/hp/g1.png")
    load_texture("hp_2", "data/sprites/hp/g2.png")
    load_texture("hp_3", "data/sprites/hp/g3.png")
    load_texture("hp_4", "data/sprites/hp/g4.png")
    load_texture("hp_5", "data/sprites/hp/g5.png")
    load_texture("hp_6", "data/sprites/hp/g6.png")
    load_texture("hp_7", "data/sprites/hp/g7.png")
    load_texture("пуля", "data/sprites/puly.png")
