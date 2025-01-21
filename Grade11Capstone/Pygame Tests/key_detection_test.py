########################
# get key test, pygame
# Caleb Hamel
# 1/10/2022
########################

import pygame, math, random

pygame.init()

screen_size = width, height = 200, 100
screen = pygame.display.set_mode(screen_size)

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == 27:
                print("escape key pressed")
                break
    pygame.time.wait(1000)