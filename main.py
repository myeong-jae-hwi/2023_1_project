import pygame
from pygame.locals import *
import ctypes
import tetris
import slither
import Rithomgame
# import RPi.GPIO as GPIO

def main():
    pygame.init()
    # GPIO.setmode(GPIO.BCM)

    gpio_pins = {"left": 17, "right": 18, "select": 27}
    # for pin in gpio_pins.values():
        # GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # define colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255,0,0)

    # get screen size
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    current_selection = 0  # 0: Tetris, 1: Slither, 2: Rithom
    is_space_pressed = False

    # create the screen
    screen = pygame.display.set_mode(screensize, FULLSCREEN)

    # create font object
    font = pygame.font.Font('font/neodgm.ttf',52)
    acade_font = pygame.font.Font('font/ka1.ttf', 78)

    # load button images
    Tetris = pygame.image.load('image/tetris.png')
    Slither = pygame.image.load('image/slither.png')
    Music = pygame.image.load('image/music.png')

    # define button dimensions and positions
    btn_width = Tetris.get_width()
    btn_height = Tetris.get_height()

    button_spacing = 100
    button_x = (screensize[0] // 2) - (((btn_width * 3) + button_spacing * 2) // 2)
    button_y = (screensize[1] // 2) + 100
    tetris_rect = pygame.Rect(button_x, button_y, btn_width, btn_height)
    slither_rect = pygame.Rect(button_x + btn_width + button_spacing, button_y, btn_width, btn_height)
    music_rect = pygame.Rect(button_x + (btn_width + button_spacing) * 2, button_y, btn_width, btn_height)

    # main loop
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:

                # left_pressed = not GPIO.input(gpio_pins["left"])
                # right_pressed = not GPIO.input(gpio_pins["right"])
                # select_pressed = not GPIO.input(gpio_pins["select"])

                if event.key == K_ESCAPE:       # 하얀 버튼으로 바꾸기
                    running = False
                elif event.key == K_SPACE:       # 노란 버튼으로 바꾸기
                    is_space_pressed = True
                # elif left_pressed:
                #     current_selection = (current_selection - 1) % 3
                # elif right_pressed:
                #     current_selection = (current_selection + 1) % 3

                if is_space_pressed:
                    if current_selection == 0:
                        print('Tetris button clicked!')
                        App = tetris.App
                        App.run()
                    elif current_selection == 1:
                        print('Slither button clicked!')
                        App = slither.App()
                        App.run()
                    elif current_selection == 2:
                        print('Music button clicked!')
                        App = Rithomgame.Rithomgame_run()
                        App.run()

                    elif event.type == KEYUP:           # 버튼으로 변경해야함
                        if event.key == K_SPACE:
                            is_space_pressed = False

            elif event.type == QUIT:
                running = False

        # fill the screen with black
        screen.fill(BLACK)

        # draw the Tetris button

        if current_selection == 0:
            screen.blit(pygame.transform.scale(Tetris, (btn_width + 10, btn_height + 10)),
                        (tetris_rect.x - 5, tetris_rect.y - 5))
            pygame.draw.rect(screen, (255, 0, 0), tetris_rect.inflate(10, 10), 5)
        else:
            screen.blit(Tetris, tetris_rect)

        if current_selection == 1:
            screen.blit(pygame.transform.scale(Slither, (btn_width + 10, btn_height + 10)),
                        (slither_rect.x - 5, slither_rect.y - 5))
            pygame.draw.rect(screen, (255, 0, 0), slither_rect.inflate(10, 10), 5)
        else:
            screen.blit(Slither, slither_rect)

        if current_selection == 2:
            screen.blit(pygame.transform.scale(Music, (btn_width + 10, btn_height + 10)),
                        (music_rect.x - 5, music_rect.y - 5))
            pygame.draw.rect(screen, (255, 0, 0), music_rect.inflate(10, 10), 5)
        else:
            screen.blit(Music, music_rect)


        # render text surface
        acade = acade_font.render('ACADE GAME', True, WHITE)
        text_surface = font.render('게임을 고르세요!', True, WHITE)

        # get text surface rectangle and center it
        text_rect = text_surface.get_rect()
        text_rect.center = screen.get_rect().center

        acade_rect = acade.get_rect()
        acade_rect.center = screen.get_rect().center
        acade_rect.top = text_rect.top - 150

        # draw text surface onto main surface
        screen.blit(acade, acade_rect)
        screen.blit(text_surface, text_rect)

        pygame.display.flip()

    # GPIO.cleanup()  # Add this at the end
    pygame.quit()

main()