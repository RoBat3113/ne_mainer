if __name__ == "__main__":
    quit("запускай только main.py")

import textures
import objects
import random
import math
# из этого состоит уровень
class Tile:
    texture = None
    walk = True

# все тайлы уровня здесь:
level = []
# размеры уровня
level_max_x = 16
level_max_y = 12

# указать тайл для уровня
def set_tile(x, y, texture, walk=True):
    if x >= 0 and x < level_max_x and y >= 0 and y < level_max_y:
        level[y * level_max_x + x].texture = texture
        level[y * level_max_x + x].walk = walk

# узнать что за клетка на уровне
def get_tile(x, y):
    if x >= 0 and x < level_max_x and y >= 0 and y < level_max_y:
        return level[y * level_max_x + x]
    return None

# генератор уровня
def generate_level():
    for y in range(level_max_y):
        for x in range(level_max_x):
            t = Tile()
            t.walk = True
            t.texture = "пол"
            level.append(t)
    
    set_tile(15, 3, "10", False)
    set_tile(13, 1, "7", False)
    set_tile(14, 1, "11", False)
    set_tile(14, 2, "8", False)
    set_tile(14, 3, "7", False)
    set_tile(12, 0, "10", False)
    set_tile(15, 2, "11", False)
    set_tile(15, 1, "11", False)
    set_tile(15, 0, "11", False)
    set_tile(14, 0, "11", False)
    set_tile(13, 0, "11", False)
    set_tile(11, 0, "7", False)#
    set_tile(0, 3, "10", False)
    set_tile(2, 1, "5", False)
    set_tile(1, 1, "11", False)
    set_tile(1, 2, "4", False)
    set_tile(1, 3, "5", False)
    set_tile(3, 0, "10", False)
    set_tile(0, 2, "11", False)
    set_tile(0, 1, "11", False)
    set_tile(0, 0, "11", False)
    set_tile(1, 0, "11", False)
    set_tile(2, 0, "11", False)
    set_tile(4, 0, "5", False)#
    set_tile(15, 8, "2", False)
    set_tile(13, 10, "1", False)
    set_tile(14, 10, "11", False)
    set_tile(14, 9, "8", False)
    set_tile(14, 8, "1", False)
    set_tile(12, 11, "2", False)
    set_tile(15, 9, "11", False)
    set_tile(15, 10, "11", False)
    set_tile(15, 11, "11", False)
    set_tile(14, 11, "11", False)
    set_tile(13, 11, "11", False)
    set_tile(11, 11, "1", False)#
    set_tile(0, 8, "2", False)
    set_tile(2, 10, "9", False)
    set_tile(1, 10, "11", False)
    set_tile(1, 9, "4", False)
    set_tile(1, 8, "9", False)
    set_tile(3, 11, "2", False)
    set_tile(0, 9, "11", False)
    set_tile(0, 10, "11", False)
    set_tile(0, 11, "11", False)
    set_tile(1, 11, "11", False)
    set_tile(2, 11, "11", False)
    set_tile(4, 11, "9", False)#

    player = objects.Player()
    player.texture = "игрок"
    player.hp = player.hp_max = 310
    player.x = 5
    player.y = 5
    player.damage = 1
    objects.objects.append(player)

    for _ in range(10):
        bot = objects.Bot()
        bot.texture = "31"
        bot.hp = bot.hp_max = 333
        bot.old_x = bot.x = random.randint(0, level_max_x)
        bot.old_y = bot.y = random.randint(0, level_max_y)
        bot.damage = 5
        objects.objects.append(bot)

# нарисовать уровень
def draw_level(screen):
    for y in range(level_max_y):
        for x in range(level_max_x):
            pos_x = x * textures.texture_size*textures.texture_scale
            pos_y = y * textures.texture_size*textures.texture_scale
            tex = level[y * level_max_x + x]
            textures.draw_texture(screen, tex.texture, pos_x, pos_y, textures.texture_scale)
