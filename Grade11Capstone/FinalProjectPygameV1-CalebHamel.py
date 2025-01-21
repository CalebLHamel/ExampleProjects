##################################
# Final Project V1
# Caleb Hamel
# 2021/12/27
##################################

# Importing Modules
import sys, pygame
pygame.init()

# Setting up the screen.
screen_size = width, height = 960, 540 

#Defining a color.
grey = 100, 100, 100

#Creating a screen with a certain size.
screen = pygame.display.set_mode(screen_size)

#Fills the entire screen with grey.
screen.fill(grey)

#Updates the screen
pygame.display.flip()

blank_tile = pygame.image.load("level_textures/blank_tile.png")

blank_tile_rect = blank_tile.get_rect()

#screen.blit(blank_tile, blank_tile_rect)

pygame.display.flip()


temp_tile_list = []

def add_new_tile_to_list():
    new_tile = blank_tile_rect.copy()
    temp_tile_list.append(new_tile)

for columb in range(10):
    for count in range(10):
        current_tile = (columb * 10) + count
        add_new_tile_to_list()
        temp_tile_list[current_tile] = temp_tile_list[current_tile].move(50 * count, 50 * columb)
        screen.blit(blank_tile, temp_tile_list[current_tile])
        pygame.display.flip()
    
print(temp_tile_list)
