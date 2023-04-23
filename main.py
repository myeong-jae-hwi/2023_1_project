import pygame
from pygame.locals import *
import ctypes

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
font = pygame.font.SysFont('Arial', 72)

# load button image
Tetris = pygame.image.load('image/tetris.jpg')


# define button dimensions and positions
button_width = Tetris.get_width()
button_height = Tetris.get_height()
button_x = (screensize[0] // 2) - (button_width // 2)
button_y = (screensize[1] // 2) + 100
button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

# set up initial button state
button_active = False

# main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == MOUSEBUTTONDOWN and event.button == 1: # check for left mouse button press
            if button_rect.collidepoint(event.pos): # check if mouse is within button boundaries
                print('Button clicked!')

        # check for mouse position
        elif event.type == MOUSEMOTION:
            if button_rect.collidepoint(event.pos):
                button_active = True
            else:
                button_active = False

        elif event.type == QUIT:
            running = False

    # fill the screen with black
    screen.fill(BLACK)

    # draw the button
    if button_active:
        screen.blit(pygame.transform.scale(Tetris, (button_width+10, button_height+10)), (button_x-5, button_y-5))
    else:
        screen.blit(Tetris, button_rect)

    # render text surface
    text_surface = font.render('HELLO!', True, WHITE)

    # get text surface rectangle and center it
    text_rect = text_surface.get_rect()
    text_rect.center = screen.get_rect().center

    # draw text surface onto main surface
    screen.blit(text_surface, text_rect)

    pygame.display.flip()

pygame.quit()
