if __name__ == "__main__":
    quit("запускай только main.py")

import pygame

main_font = None

def load_fonts():
    pygame.font.init()
    global main_font
    main_font = pygame.font.Font("data/HomeVideo_Font_0_8/TrueType (.ttf)/HomeVideo-Regular.ttf", 70)

def draw_text(screen, txt, x, y, color):
    global main_font
    text = main_font.render(txt, True, color)
    screen.blit(text, (x, y))
