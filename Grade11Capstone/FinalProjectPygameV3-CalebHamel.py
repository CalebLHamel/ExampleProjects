##################################
# Final Project V3
# Caleb Hamel
# 2021/12/29
##################################

# Importing Modules
import sys, pygame, math, random
pygame.init()

###################
# Variables
###################

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

max_grid_width = 500
max_grid_height = 500
grid_width = 10
grid_height = 10
total_tiles = grid_width * grid_height

number_of_mines_to_place = 20

if grid_width >= grid_height:
    tile_resize = math.floor(max_grid_width / grid_width)
else:
    tile_resize = math.floor(max_grid_height / grid_height)
blank_tile = pygame.transform.scale(blank_tile, (tile_resize,tile_resize))

blank_tile_rect = blank_tile.get_rect()

tile_size = blank_tile_rect[2]


grid_x_offset = (screen_size[0] / 2) - ((grid_width * tile_size) / 2)
grid_y_offset = (screen_size[1] / 2) - ((grid_height * tile_size) / 2)
#screen.blit(blank_tile, blank_tile_rect)

pygame.display.flip()


temp_tile_list = []

def add_new_tile_to_list(tile_type):
    if tile_type == "undiscovered":
        new_tile = blank_tile_rect.copy()
        temp_tile_list.append([new_tile, "undiscovered"])
    if tile_type == "mine":
        new_tile = blank_tile_rect.copy()
        temp_tile_list.append([new_tile, "mine"])

mine_numbers = []
for a_mine in range(number_of_mines_to_place):
    while True:
        a_mine_number = random.randrange(total_tiles)
        if a_mine_number in mine_numbers:
            continue
        else:
            mine_numbers.append(a_mine_number)
            break
        
print(mine_numbers)

for columb in range(grid_height):
    for count in range(grid_width):
        current_tile = (columb * grid_width) + count
        if current_tile in mine_numbers:
            add_new_tile_to_list("mine")
        else:
            add_new_tile_to_list("undiscovered")
        temp_tile_list[current_tile][0] = temp_tile_list[current_tile][0].move(tile_size * count + grid_x_offset, tile_size * columb + grid_y_offset)
        screen.blit(blank_tile, temp_tile_list[current_tile][0])
pygame.display.flip()


    
print(temp_tile_list)
#print(temp_tile_list[0][2:4])


end_click = True
while 1:
    
    pygame.event.get()

    #If the mouse button was pressed down.
    if pygame.mouse.get_pressed(3)[0] == True and end_click == True:
        mouse_posistion = pygame.mouse.get_pos() #Gets the mouse position.
        
        for tile in temp_tile_list:
            if tile[0].collidepoint(mouse_posistion) == True:
                print("You clicked on tile number " + str(temp_tile_list.index(tile)) + ".")
                print(tile)
                if tile[1] == "mine":
                    print("It was a mine!")
                end_click = False
            
    if pygame.mouse.get_pressed(3)[0] == False:
        end_click = True


    