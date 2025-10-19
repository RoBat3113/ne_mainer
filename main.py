import pygame
import textures
import level
import objects
import hud
import font
import lan

lan.init()

# размеры окна
screen_x = textures.texture_size * textures.texture_scale * level.level_max_x
screen_y = textures.texture_size * textures.texture_scale * level.level_max_y
bg_color = (0,0,0) # цвет фона
screen = pygame.display.set_mode((screen_x, screen_y), vsync=0)
clock = pygame.time.Clock()
font.load_fonts()

textures.loading_textures()
level.generate_level()

# основной цикл игры
running = True
while running:   
    #я
    # цикл обработки событий из Pygame
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    #lan.send_data("X")
    txt = lan.upload_data()
    if txt != None:
        print(f"uploaded: {txt}")

    screen.fill(bg_color) # залить экран цветом
    level.draw_level(screen)
    for o in objects.objects:
        o.action(keys)
        o.draw(screen)
    for o in objects.objects:
        if o.hp <= 0:
            objects.objects.remove(o)  
    hud.draw_hp(screen)

    if objects.get_player().hp <= 0:
        font.draw_text(screen, "GAME OVER ☻♥, Санс признателен", 100, screen_y/2, (255, 255, 0))
    pygame.display.flip() # показать кадр на экране
    clock.tick(60) # скорость игры

pygame.quit()
