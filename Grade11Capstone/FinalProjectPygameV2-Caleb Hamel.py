##################################
# Final Project V2
# Caleb Hamel
# 2021/12/28
##################################

# Importing Modules
import sys, pygame
pygame.init()

# Setting up the screen.
screen_size = width, height = 960, 960

#Defining a color.
grey = 100, 100, 100

#Creating a screen with a certain size.
screen = pygame.display.set_mode(screen_size)

#Fills the entire screen with grey.
screen.fill(grey)

#Updates the screen
pygame.display.flip()

blank_tile = pygame.image.load("level_textures/undiscovered_tile.png")

blank_tile_rect = blank_tile.get_rect()

tile_size = blank_tile_rect[2]
grid_width = 10
grid_height = 10

grid_x_offset = (screen_size[0] / 2) - ((grid_width * tile_size) / 2)
grid_y_offset = (screen_size[1] / 2) - ((grid_height * tile_size) / 2)
#screen.blit(blank_tile, blank_tile_rect)

pygame.display.flip()


temp_tile_list = []

def add_new_tile_to_list():
    new_tile = blank_tile_rect.copy()
    temp_tile_list.append(new_tile)

for columb in range(grid_height):
    for count in range(grid_width):
        current_tile = (columb * grid_width) + count
        add_new_tile_to_list()
        temp_tile_list[current_tile] = temp_tile_list[current_tile].move(tile_size * count + grid_x_offset, tile_size * columb + grid_y_offset)
        screen.blit(blank_tile, temp_tile_list[current_tile])
        pygame.display.flip()
    
print(temp_tile_list)
print(temp_tile_list[0][2:4])


end_click = True
while 1:
    
    pygame.event.get()

    #If the mouse button was pressed down.
    if pygame.mouse.get_pressed(3)[0] == True and end_click == True:
        mouse_posistion = pygame.mouse.get_pos() #Gets the mouse position.
        
        for tile in temp_tile_list:
            if tile.collidepoint(mouse_posistion) == True:
                print("You clicked on tile number " + str(temp_tile_list.index(tile)) + ".")
                end_click = False
            
    if pygame.mouse.get_pressed(3)[0] == False:
        end_click = True


    