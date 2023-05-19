import pygame
from pygame.locals import *
import ctypes
import tetris
import slither
import galaga

pygame.init()

# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# get screen size
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# create the screen
screen = pygame.display.set_mode(screensize, FULLSCREEN)

# create font object
font = pygame.font.Font('font/a시월구일1.ttf',52)

# load button images
Tetris = pygame.image.load('image/tetris.png')
Slither = pygame.image.load('image/slither.png')
Galaga = pygame.image.load('image/Galaga.png')

# define button dimensions and positions
btn_width = Tetris.get_width()
btn_height = Tetris.get_height()

button_spacing = 100
button_x = (screensize[0] // 2) - (((btn_width * 3) + button_spacing * 2) // 2)
button_y = (screensize[1] // 2) + 100
tetris_rect = pygame.Rect(button_x, button_y, btn_width, btn_height)
slither_rect = pygame.Rect(button_x + btn_width + button_spacing, button_y, btn_width, btn_height)
galaga_rect = pygame.Rect(button_x + (btn_width + button_spacing) * 2, button_y, btn_width, btn_height)


# set up initial button states
tetris_active = False
slither_active = False
galaga_active = False

# main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == MOUSEBUTTONDOWN and event.button == 1: # check for left mouse button press
            if tetris_rect.collidepoint(event.pos): # check if mouse is within Tetris button boundaries
                print('Tetris button clicked!')
                App = tetris.App
                App.run()

            elif slither_rect.collidepoint(event.pos): # check if mouse is within slither button boundaries
                print('Slither button clicked!')
                App = slither.App()
                App.run()

            elif galaga_rect.collidepoint(event.pos):
                print('Galaga button clicked!')
                App = galaga.initGame()
                App.run()

        # check for mouse position
        elif event.type == MOUSEMOTION:
            if tetris_rect.collidepoint(event.pos):
                tetris_active = True
            else:
                tetris_active = False

            if slither_rect.collidepoint(event.pos):
                slither_active = True
            else:
                slither_active = False

            if galaga_rect.collidepoint(event.pos):
                galaga_active = True
            else:
                galaga_active = False

        elif event.type == QUIT:
            running = False

    # fill the screen with black
    screen.fill(BLACK)

    # draw the Tetris button
    if tetris_active:
        screen.blit(pygame.transform.scale(Tetris, (btn_width+10, btn_height+10)), (tetris_rect.x-5, tetris_rect.y-5))
    else:
        screen.blit(Tetris, tetris_rect)

    # draw the slither button
    if slither_active:
        screen.blit(pygame.transform.scale(Slither, (btn_width+10, btn_width+10)), (slither_rect.x-5, slither_rect.y-5))
    else:
        screen.blit(Slither, slither_rect)

    if galaga_active:
        screen.blit(pygame.transform.scale(Galaga, (btn_width+10, btn_width+10)), (galaga_rect.x-5, galaga_rect.y-5))
    else:
        screen.blit(Galaga, galaga_rect)


    # render text surface
    text_surface = font.render('게임을 고르세요!', True, WHITE)

    # get text surface rectangle and center it
    text_rect = text_surface.get_rect()
    text_rect.center = screen.get_rect().center

    # draw text surface onto main surface
    screen.blit(text_surface, text_rect)

    pygame.display.flip()

pygame.quit()