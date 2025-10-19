if __name__ == "__main__":
    quit("запускай только main.py")

import textures
import level
import pygame
import random
import math
import lan
class Object:
    x = 0
    y = 0
    old_x = 0
    old_y = 0
    texture = None
    hp = 0
    hp_max = 0
    damage = 0
    angle = "up"

    # проверка что объект не вышел за уровень
    def check_in_screen(self):
        if self.x >= level.level_max_x: self.x = level.level_max_x - 1
        if self.x < 0: self.x = 0
        if self.y >= level.level_max_y: self.y = level.level_max_y - 1
        if self.y < 0: self.y = 0

    # действие объекта
    def action(self, keys):
        if (self.hp <= 0):
            return
        self.check_in_screen()
        tile = level.get_tile(self.x, self.y)
        if tile and tile.walk == False:
            self.x = self.old_x
            self.y = self.old_y
        self.old_x = self.x
        self.old_y = self.y
        lan.send_data(f"SPRITE_RENDER:{self.x}:{self.y}:{self.texture}:{self.angle}")
        
    def draw(self, screen):
        if (self.hp <= 0):
            return
        textures.draw_texture(screen, self.texture,
                     self.x*textures.texture_size*textures.texture_scale,
                     self.y*textures.texture_size*textures.texture_scale,
                     textures.texture_scale, self.angle)

objects = []

class Bullet(Object):
    is_player_bullet = True
    vx = 0
    vy = 0

    def check_collision(self):
        # пройтись по всем объектам и найти тех, в кого можно врезаться
        for obj in objects:
            # не проверять себя с собой
            if obj == self:
                continue
            if isinstance(obj, Bot) and obj.x == self.x and obj.y == self.y:
                self.hp = 0
                obj.hp -= self.damage
                print(f"столкновение обнаружено на {obj.x}, {obj.y}")

    def action(self, keys):
        self.x += self.vx
        self.y += self.vy
        self.check_collision()

class Player(Object):
    cheats = False
    shot_delay = 10
    timer_shot = shot_delay

    def shot(self):
        if self.timer_shot > 0:
            return

        self.timer_shot = self.shot_delay
        b = Bullet()
        b.texture = "пуля"
        b.hp = b.hp_max = 1
        b.x = self.x
        b.y = self.y
        b.damage = 911

        if self.angle == "up":    b.vy = -1
        if self.angle == "down":  b.vy = +1
        if self.angle == "left":  b.vx = -1
        if self.angle == "right": b.vx = +1
        objects.append(b)

    def action(self, keys):
        self.timer_shot -= 1

        if (self.hp <= 0):
            return
        
        # вверх
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= 1
            self.angle = "up"
        # вниз
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += 1 
            self.angle = "down"
        # влево
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= 1 
            self.angle = "left"
        # вправо
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += 1 
            self.angle = "right"
        
        if keys[pygame.K_q]: # читы
            self.cheats = True
        if keys[pygame.K_e]: # читы выкл.
            self.cheats = False

        if keys[pygame.K_SPACE]: # временная стрельба
            self.shot()

        if not self.cheats:
            super().action(keys)

class Bot(Object):
    def __init__(self):
        super().__init__()
        self.move_cooldown = random.random()*400 + 300  # 2 секунды между движениями
        self.last_move_time = 0
        self.attack_cooldown = 800  # 1 секунда между атаками
        self.last_attack_time = 0
    
    def action(self, keys):
        #print(f"bot hp {self.hp}")

        if (self.hp <= 0):
            return
        
        super().action(keys)
        
        current_time = pygame.time.get_ticks()
        
        # Двигаемся только раз в несколько секунд
        if current_time - self.last_move_time < self.move_cooldown:
            return
            
        self.last_move_time = current_time
        
        # Находим игрока
        player = None
        for obj in objects:
            if isinstance(obj, Player):
                player = obj
                break
        
        if player:
            # Вычисляем направление к игроку
            dx = player.x - self.x
            dy = player.y - self.y
            
            # Двигаемся к игроку только по целым координатам
            move_x, move_y = 0, 0
            
            # Случайным образом выбираем направление (делаем движение менее предсказуемым)
            if random.random() < 0.7:  # 70% chance двигаться к игроку
                if abs(dx) > abs(dy):
                    # Двигаемся по X
                    if dx > 0:
                        move_x = 1
                        self.angle = "right"
                    elif dx < 0:
                        move_x = -1
                        self.angle = "left"
                else:
                    # Двигаемся по Y
                    if dy > 0:
                        move_y = 1
                        self.angle = "down"
                    elif dy < 0:
                        move_y = -1
                        self.angle = "up"
            else:
                # 30% chance случайного движения (более естественное поведение)
                directions = [(1, 0, "right"), (-1, 0, "left"), (0, 1, "down"), (0, -1, "up")]
                move_x, move_y, angle = random.choice(directions)
                self.angle = angle
            
            # Пробуем двигаться
            if move_x != 0 or move_y != 0:
                # Сохраняем старую позицию
                old_x, old_y = self.x, self.y
                
                # Пробуем двигаться
                self.x += move_x
                self.y += move_y
                
                # Проверяем коллизии
                self.check_in_screen()
                tile = level.get_tile(self.x, self.y)
                if tile and tile.walk == False:
                    # Возвращаемся назад если нельзя пройти
                    self.x, self.y = old_x, old_y
                else:
                    # Обновляем old позиции при успешном движении
                    self.old_x, self.old_y = old_x, old_y
            
            # Атака если рядом с игроком
            distance = max(abs(dx), abs(dy))
            if distance <= 1:  # соседняя клетка
                if current_time - self.last_attack_time > self.attack_cooldown:
                    self.attack(player)
                    self.last_attack_time = current_time
    
    def attack(self, player):
        """Атака игрока"""
        if hasattr(player, 'hp'):
            player.hp -= self.damage
            # print(f"Бот атаковал! У игрока осталось {player.hp} HP")
            
            # Проверяем смерть игрока
            if player.hp <= 0:
                print("Игрок умер!")

def get_player():
    return objects[0]