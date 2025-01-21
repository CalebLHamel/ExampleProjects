##################################
# Final Project V4
# Caleb Hamel
# 2021/12/30
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




undiscovered_tile = pygame.image.load("level_textures/undiscovered_tile.png") #The undiscovered tile.
discovered_tile = pygame.image.load("level_textures/discovered_tile.png") #The discovered tile.
flag = pygame.image.load("level_textures/flag.png")

images_to_load = ["one", "two", "three", "four", "five", "six", "seven", "eight"]
number_images = []
for image in images_to_load:
    number_images.append(pygame.image.load("numbers/" + image + ".png"))

# Maximum space that the grid can take up.
max_grid_width = 500
max_grid_height = 500

#Size of the grid.
grid_width = 10
grid_height = 10

total_tiles = grid_width * grid_height #Total amount of tiles.

number_of_mines_to_place = 10 #Number of mines.

#Determines the size of the tiles. The if statement ensures that rectangle grids won't cross over the maximum.
if grid_width >= grid_height:
    tile_resize = math.floor(max_grid_width / grid_width)
else:
    tile_resize = math.floor(max_grid_height / grid_height)
    
#Resizing the tile images.
undiscovered_tile = pygame.transform.scale(undiscovered_tile, (tile_resize,tile_resize))
discovered_tile = pygame.transform.scale(discovered_tile, (tile_resize,tile_resize))
flag = pygame.transform.scale(flag, (tile_resize,tile_resize))

#Resizing the undiscovered tile rect.
tile_rect = undiscovered_tile.get_rect()

tile_size = tile_rect[2] #Size of the tiles.

#The offsets are how far the tiles have to move for the grid to be centered.
grid_x_offset = (screen_size[0] / 2) - ((grid_width * tile_size) / 2)
grid_y_offset = (screen_size[1] / 2) - ((grid_height * tile_size) / 2)

#Updating the screen.
pygame.display.flip()


tile_list = [] #Defining the list of tiles.

#Function to add a new tile to the list.
def add_new_tile_to_list(tile_type):
    
    #Adding an undiscovered tile to the list.
    if tile_type == "undiscovered":
        new_tile = tile_rect.copy()
        tile_list.append([new_tile, "undiscovered", "", 0])
        
    #Adding a mine to the list.
    if tile_type == "mine":
        new_tile = tile_rect.copy()
        tile_list.append([new_tile, "mine", "", 0])
        
        
def change_tile_in_list(tile_number, tile_type):
    previous_tile_rect = tile_list[tile_number][0].copy()
    mine_count = tile_list[tile_number][3]
    tile_list.pop(tile_number)
    tile_list.insert(tile_number, [previous_tile_rect, tile_type, "", mine_count])
    
    


mine_numbers = [] #All the indexes of the mines.

#Determining what the mine indexes will be.
for a_mine in range(number_of_mines_to_place): #Once for every mine that has to be placed.
    
    while True:
        a_mine_number = random.randrange(total_tiles) #Random number.
        
        if a_mine_number in mine_numbers: #If the number has already been chosen.
            continue #Try again.
        
        else: #Number has not been chosen yet.
            mine_numbers.append(a_mine_number) #Add number to list.
            break #End the loop.
        
print(mine_numbers) #For debuging.

def update_screen():
    screen.fill(grey)
    for tile in tile_list:
        if tile[1] == "undiscovered" or tile[1] == "mine":
            screen.blit(undiscovered_tile, tile[0])
            if tile[2] == "flag":
                screen.blit(flag, tile[0])
        elif tile[1] == "discovered":
            screen.blit(discovered_tile, tile[0])
        
        if tile[1] != "mine" and tile[1] != "undiscovered":
            for number in range(8):
                if number + 1 == tile[3]:
                    screen.blit(number_images[number], tile[0])
            
            
            
    pygame.display.flip()





for columb in range(grid_height):
    for count in range(grid_width):
        
        current_tile = (columb * grid_width) + count #Number for the current tile.
        
        if current_tile in mine_numbers: #If the tile should be a mine.
            add_new_tile_to_list("mine") #New tile is a mine.
            
        else: #New tile is not a mine.
            add_new_tile_to_list("undiscovered") #New tile is an undiscovered tile.
            
        tile_list[current_tile][0] = tile_list[current_tile][0].move(tile_size * count + grid_x_offset, tile_size * columb + grid_y_offset) #Changing position of the tile.
        screen.blit(undiscovered_tile, tile_list[current_tile][0]) #Moving image overtop of the tile.
     
     
#######################
# Mine counter
#######################

for tile in tile_list:
    tile_index = tile_list.index(tile) + 1
    surrounding_mines = 0
    in_corner = 0
    
    if tile_index > grid_width: #Tile not on top row.
        if tile_list[tile_index - grid_width - 1][1] == "mine":
            surrounding_mines += 1

        if tile_index % grid_width != 1: #Tile not on left columb.
            if tile_list[tile_index - grid_width - 2][1] == "mine":
                surrounding_mines += 1
            

        if tile_index % grid_width != 0: #Tile not on right columb.
            if tile_list[tile_index - grid_width][1] == "mine":
                surrounding_mines += 1
        
    if tile_index < total_tiles - grid_width: #Tile not on bottom row.
        if tile_list[tile_index + grid_width - 1][1] == "mine":
            surrounding_mines += 1

        if tile_index % grid_width != 1: #Tile not on left columb.
            if tile_list[tile_index + grid_width - 2][1] == "mine":
                surrounding_mines += 1

        if tile_index % grid_width != 0: #Tile not on right columb.
            if tile_list[tile_index + grid_width][1] == "mine":
                surrounding_mines += 1
    
    if tile_index % grid_width != 1: #Tile not on left columb.
        if tile_list[tile_index - 2][1] == "mine":
            surrounding_mines += 1
        
    if tile_index % grid_width != 0: #Tile not on right columb.
        if tile_list[tile_index][1] == "mine":
            surrounding_mines += 1
    tile_list[tile_index - 1][3] = surrounding_mines
    
        
#############################
# Cleared area expansion.
#############################

#Used for clear_area() and complete_clear_area()
already_cleared = []
left_to_clear = []
    
#Function to clear an area.
def clear_area(a_tile):
    
    already_cleared.append(tile_list.index(a_tile)) #Adds a_tile to list of tiles that have been cleared already.
    starting_tile_index = tile_list.index(a_tile) #Index of the starting tile.
    
    if a_tile[1] != "mine" and a_tile[2] != "flag": #Don't clear mines or flags.
        change_tile_in_list(tile_list.index(a_tile), "discovered") #Clear a_tile.
    
    
    if starting_tile_index in left_to_clear: # If a_tile is in the line to be cleared,
        left_to_clear.remove(starting_tile_index) # Remove it from the lineup.
        
    if tile_list[starting_tile_index][3] != 0:
        change_tile_in_list(starting_tile_index, "discovered") #Clear a_tile.
        return
    
    #Defining the indexes of the surrounding tiles (what they would be in the right circumstances).
    above_tile = starting_tile_index - grid_width
    below_tile = starting_tile_index + grid_width
    right_tile = starting_tile_index + 1
    left_tile = starting_tile_index - 1

    TL_corner = 0
    TR_corner = 0
    BL_corner = 0
    BR_corner = 0
    
    #If the current tile is a number tile.
    if tile_list[starting_tile_index][3] != 0:
        only_clear_numbers = True #Only clear other neighboring number tiles.
    
    
    #Adjacent Tiles
    #If the above tile hasn't been cleared yet, and it's not already lined up to be cleared
    if above_tile not in already_cleared and above_tile not in left_to_clear:
        if above_tile >= 0: #And the above tile is in bounds.
            TR_corner += 1
            TL_corner += 1
            if tile_list[above_tile][1] != "mine": #And it's not a mine.
                left_to_clear.append(above_tile) #Add the tile to the list to clear.
            
    if below_tile not in already_cleared and below_tile not in left_to_clear:
        if below_tile < total_tiles:
            BR_corner += 1
            BL_corner += 1
            if tile_list[below_tile][1] != "mine":
                left_to_clear.append(below_tile)
    
    if right_tile not in already_cleared and right_tile not in left_to_clear:
        if (starting_tile_index + 1) % grid_width != 0:
            TR_corner += 1
            BR_corner += 1
            if tile_list[right_tile][1] != "mine":
                left_to_clear.append(right_tile)
            
    if left_tile not in already_cleared and left_tile not in left_to_clear:
        if (starting_tile_index) % grid_width != 0:
            TL_corner += 1
            BL_corner += 1
            if tile_list[left_tile][1] != "mine":
                left_to_clear.append(left_tile)
      
        


def check_for_missed_corners():
    for current_tile in tile_list:
        if current_tile[1] == "discovered" and current_tile[3] == 0:
            
            starting_tile_index = tile_list.index(current_tile)
        
            #Defining the indexes of the surrounding tiles (what they would be in the right circumstances).
            above_tile = starting_tile_index - grid_width
            below_tile = starting_tile_index + grid_width
            right_tile = starting_tile_index + 1
            left_tile = starting_tile_index - 1

            TL_corner = 0
            TR_corner = 0
            BL_corner = 0
            BR_corner = 0
    
            if above_tile >= 0: #And the above tile is in bounds.
                TR_corner += 1
                TL_corner += 1
            
            if below_tile < total_tiles:
                BR_corner += 1
                BL_corner += 1
            
            if (starting_tile_index + 1) % grid_width != 0:
                    TR_corner += 1
                    BR_corner += 1

            if (starting_tile_index) % grid_width != 0:
                TL_corner += 1
                BL_corner += 1

            #Corners
            if TR_corner == 2 and tile_list[above_tile + 1][2] != "flag":
                change_tile_in_list(above_tile + 1, "discovered")
            if TL_corner == 2 and tile_list[above_tile - 1][2] != "flag":
                change_tile_in_list(above_tile - 1, "discovered")
            if BR_corner == 2 and tile_list[below_tile + 1][2] != "flag":
                change_tile_in_list(below_tile + 1, "discovered")
            if BL_corner == 2 and tile_list[below_tile - 1][2] != "flag":
                change_tile_in_list(below_tile - 1, "discovered")

def complete_clear_area():

    while left_to_clear != []:
        clear_area(tile_list[left_to_clear[0]])
    check_for_missed_corners()

    
        
pygame.display.flip() #Updating screen now that the grid has generated.



print(tile_list) #For debugging.



end_click = True
end_r_click = True
 
while True: #Controls the game.
    
    pygame.event.get() #Needed for mouse.get_pressed to work.

    #If the mouse button was pressed down.
    if pygame.mouse.get_pressed(3)[0] == True and end_click == True: #If the mouse button is pressed down.
        mouse_posistion = pygame.mouse.get_pos() #Gets the mouse position.
        
        for tile in tile_list: #For every tile.
            current_index = tile_list.index(tile)
            if tile[0].collidepoint(mouse_posistion) == True: #If the mouse is overtop of the tile.
                print("You clicked on tile number " + str(tile_list.index(tile)) + ".") #For debugging.
                print(tile) #Debugging
                
                if tile[1] != "mine" and tile[2] != "flag":
                    
                    #change_tile_in_list(current_index, "discovered")
                    clear_area(tile)
                    complete_clear_area()
                
                if tile[1] == "mine": #Debugging.
                    print("It was a mine!") #Debugging.
                end_click = False #Mouse button has not been released.
        update_screen()
            
    if pygame.mouse.get_pressed(3)[0] == False: #If the button is up.
        end_click = True #The mouse button has now been released.
        
    
    if pygame.mouse.get_pressed(3)[2] == True and end_r_click == True:
        mouse_posistion = pygame.mouse.get_pos() #Gets the mouse position.
        for tile in tile_list: #For every tile.
            if tile[0].collidepoint(mouse_posistion) == True: #If the mouse is overtop of the tile.
                if tile[1] == "undiscovered" or tile[1] == "mine":
                    if tile[2] != "flag":
                        tile[2] = "flag"
                    else:
                        tile[2] = ""
        update_screen()
                
        end_r_click = False
    if pygame.mouse.get_pressed(3)[2] == False:
        end_r_click = True


    