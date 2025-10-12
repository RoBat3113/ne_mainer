import pygame
import random

class BotManager:
    def __init__(self, texture_manager):
        self.bots = []
        self.texture_manager = texture_manager
        self.spawn_timer = 0
        self.spawn_delay = 3000  # 3 секунды между спавном
        self.max_bots = 8
        
    def get_valid_spawn_position(self, player_x, player_y, obstacles, screen_width, screen_height):
        """Находит валидную позицию для спавна без коллизий"""
        max_attempts = 20
        
        for attempt in range(max_attempts):
            # Спавн на краю экрана
            side = random.randint(0, 3)
            
            if side == 0:  # сверху
                x = random.randint(100, screen_width - 100)
                y = -50
            elif side == 1:  # справа
                x = screen_width + 50
                y = random.randint(100, screen_height - 100)
            elif side == 2:  # снизу
                x = random.randint(100, screen_width - 100)
                y = screen_height + 50
            else:  # слева
                x = -50
                y = random.randint(100, screen_height - 100)
            
            # Проверяем коллизии
            test_bot = Bot(x, y)
            test_bot.load_texture(self.texture_manager)
            test_rect = test_bot.get_rect()
            
            valid_position = True
            for obstacle in obstacles:
                if test_rect.colliderect(obstacle):
                    valid_position = False
                    break
            
            if valid_position:
                return x, y
        
        # Если не нашли валидную позицию, возвращаем случайную
        return random.randint(100, screen_width - 100), random.randint(100, screen_height - 100)
    
    def spawn_bot(self, player_x, player_y, obstacles, screen_width, screen_height):
        """Создание нового бота в валидной позиции"""
        if len(self.bots) >= self.max_bots:
            return False
            
        # Находим валидную позицию для спавна
        x, y = self.get_valid_spawn_position(player_x, player_y, obstacles, screen_width, screen_height)
        
        bot = Bot(x, y)
        bot.load_texture(self.texture_manager)
        self.bots.append(bot)
        return True
    
    def update(self, player_x, player_y, obstacles, current_time, screen_width, screen_height):
        """Обновление всех ботов"""
        # Автоматический спавн
        if current_time - self.spawn_timer > self.spawn_delay:
            self.spawn_timer = current_time
            self.spawn_bot(player_x, player_y, obstacles, screen_width, screen_height)
        
        # Обновляем ботов и собираем атаки
        attacks = []
        dead_bots = []
        
        for i, bot in enumerate(self.bots):
            is_attacking = bot.update(player_x, player_y, obstacles)
            if is_attacking:
                attacks.append(bot)
            
            if bot.health <= 0:
                dead_bots.append(i)
        
        # Удаляем мертвых ботов
        for i in sorted(dead_bots, reverse=True):
            self.bots.pop(i)
            
        return attacks
    
    def draw(self, screen, camera_x=0, camera_y=0):
        """Отрисовка всех ботов"""
        for bot in self.bots:
            bot.draw(screen, camera_x, camera_y)
    
    def get_bots(self):
        return self.bots.copy()
    
    def clear(self):
        self.bots = []