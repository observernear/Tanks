import pygame
import os
from random import randint
from settings import *
from main_class import main_class

pygame.init()

ui = UI()

menu = main_menu()

main_class.spawn_tanks()

main_class.spawn_obstacles()

soundStart.play()

menu_trigger = True
play = True
while play:
    for event in pygame.event.get():
        if pygame.QUIT == event.type:
            play = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menu_trigger = not menu_trigger
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
    if menu_trigger:
        menu.draw()
    else:
        main_class.spawn_bonuses()

        keys = pygame.key.get_pressed()
        main_class.update(keys)

        screen.fill((0, 0, 0))

        main_class.draw()

        ui.draw()

        main_class.check_winner()

    if pygame.mouse.get_focused():
        cursor_rect.center = pygame.mouse.get_pos()
        screen.blit(cursor_image, cursor_rect)

    pygame.display.update()
    clock.tick(FPS)


pygame.quit()
