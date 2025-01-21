##################################
# Final Project V5
# Caleb Hamel
# 2021/12/31
##################################

# Importing Modules
import sys, pygame, math, random
pygame.init()

#A tile is a list [rect, xcor, ycor, type, num_of_surrounding_mines, flag]

###############################
# Setting up the Screen
###############################

screen_size = width, height = 960, 960

#Defining a color.
grey = 100, 100, 100

#Creating a screen with a certain size.
screen = pygame.display.set_mode(screen_size)

#Fills the entire screen with grey.
screen.fill(grey)

#Updates the screen
pygame.display.flip()




###############################
# Variables
###############################
number_of_mines = 10 #Mines on grid.
grid_tile_width = 25 #How many tiles wide the grid is.
grid_tile_height = 25 #How many tiles hight the grid is.
max_grid_size = 500 #Maximum size of the grid 


if grid_tile_width >= grid_tile_height:
    tile_resize = math.floor(max_grid_size / grid_tile_width)
else:
    tile_resize = math.floor(max_grid_size / grid_tile_height)
                  
tile_origin_x = (960 / 2) - (tile_resize * grid_tile_width / 2) + (tile_resize / 2)
tile_origin_y = (960 / 2) - (tile_resize * grid_tile_height / 2) + (tile_resize / 2)

tile_list = []

first_tile_clicked = []

tiles_cleared = []
tiles_left_to_clear = []



###############################
# Images
###############################


undiscovered_tile = pygame.image.load("level_textures/undiscovered_tile.png") #The undiscovered tile.


discovered_tile = pygame.image.load("level_textures/discovered_tile.png") #The discovered tile.


flag = pygame.image.load("level_textures/flag.png") #The flag.


###############
# Menu Textures

start_screen = pygame.image.load("title_screen/title_screen.png")

easy_difficulty_button = pygame.image.load("title_screen/easy_difficulty_button.png")
moderate_difficulty_button = pygame.image.load("title_screen/moderate_difficulty_button.png")
difficult_difficulty_button = pygame.image.load("title_screen/difficult_difficulty_button.png")
very_difficult_difficulty_button = pygame.image.load("title_screen/verydifficult_difficulty_button.png")

start_button = pygame.image.load("title_screen/start_button.png")


images_to_load = ["one", "two", "three", "four", "five", "six", "seven", "eight"] #Names of all the number images.
number_images = [] #List containing all number textures.

#Adds all the number images to the number_images list.
for image in images_to_load:
    number_images.append(pygame.image.load("numbers/" + image + ".png"))
    
for image in range(len(number_images)):
    number_images[image] = pygame.transform.scale(number_images[image], (tile_resize,tile_resize))
    
#Resizing the tile images.
undiscovered_tile = pygame.transform.scale(undiscovered_tile, (tile_resize,tile_resize))
discovered_tile = pygame.transform.scale(discovered_tile, (tile_resize,tile_resize))
flag = pygame.transform.scale(flag, (tile_resize,tile_resize))


#Resizing the undiscovered tile rect.
tile_rect = undiscovered_tile.get_rect()


tile_size = tile_rect[2] #Size of the tiles.




##########################
# Functions
##########################

#Add a new tile to the list of tiles.
def add_new_tile_to_list(xcor, ycor):
    new_tile_rect = tile_rect.copy()
    new_tile = [new_tile_rect, xcor, ycor, "undiscovered", 0, ""]
    tile_list.append(new_tile)
    
    
#Changing a tile in the list.
    
def change_tile_in_list(tile_number, tile_type):
    previous_tile = tile_list[tile_number]
    tile_list.pop(tile_number)
    previous_tile[3] = tile_type
    tile_list.insert(tile_number, previous_tile)
    
#Update the screen.
def update_screen():
    screen.fill(grey) #Fills screen with grey.
    
    for tile in tile_list: #For each tile.
        
        if tile[3] == "undiscovered" or tile[3] == "mine": #If they are undiscovered or a mine,
            screen.blit(undiscovered_tile, tile[0]) #Make them look like an undiscovered tile.
            if tile[5] == "flag": #If they have a flag.
                screen.blit(flag, tile[0]) #Make a flag appear on them.
                
        elif tile[3] == "discovered": #If they are discovered.
            screen.blit(discovered_tile, tile[0]) #make them look like a discovered tile.
        
        if tile[3] != "mine" and tile[3] != "undiscovered": #If they are not a mine, and not an undiscovered tile.
            
            for number in range(8): #8 possible numbers.
                if number + 1 == tile[4]: #If 1 through 8 matches the 4th element of tile.
                    screen.blit(number_images[number], tile[0]) #Make the matching number appear.
    pygame.display.flip()                 

#Add mines to the level.
def add_mines_to_level():
    mine_cords_list = [] #List of all the mines.
    
    for mine in range(number_of_mines): #For each mine that should exist.
        
        while True:
            #Generate coordinates.
            mine_x = random.randrange(grid_tile_width)
            mine_y = random.randrange(grid_tile_height)
            
            #If the coordinates are too close to where the user clicked first.
            if mine_x < first_tile_clicked[1] - 1  or mine_x > first_tile_clicked[1] + 1 or mine_y < first_tile_clicked[2] - 1  or mine_y > first_tile_clicked[2] + 1:
                
                new_mine_cords = [mine_x, mine_y] #Defining the coordinates into a list.
                
                if new_mine_cords in mine_cords_list: #If the coordinates were already chosen.
                    continue #Try to generate new coordinates.
                
                else: #Coordinates are not duplicates, and are far enough from the inititial click.
                    mine_cords_list.append(new_mine_cords) #Coordinates are added to the list.
                    break #Break the loop. Moving to the next mine that should exist.
            else:
                continue
        
    print(mine_cords_list) #For debugging.
    
    for tile in tile_list: #For each tile.
        for mine_cords in mine_cords_list:#For each mine coordinate.
            
            if tile[1] == mine_cords[0] and tile[2] == mine_cords[1]: #If their coordinates match
                tile[3] = "mine" #Make the tile a mine.
                
def find_surrounding_mines():
    for tile in tile_list:
        out_of_bounds_y = [-1, grid_tile_height]
        out_of_bounds_x = [-1, grid_tile_width]
    
        x_origin = tile[1]
        y_origin = tile[2]
    
        x_coords = [x_origin - 1, x_origin - 1, x_origin - 1, x_origin, x_origin, x_origin + 1, x_origin + 1, x_origin + 1]
        y_coords = [y_origin + 1, y_origin, y_origin - 1, y_origin - 1, y_origin + 1, y_origin + 1, y_origin, y_origin - 1]

        num_of_surrounding_mines = 0
        
        for index in range(8):
            if x_coords[index] not in out_of_bounds_x and y_coords[index] not in out_of_bounds_y:
                surrounding_tile = find_tile_with_xy(x_coords[index], y_coords[index])
                if surrounding_tile[3] == "mine":
                    num_of_surrounding_mines += 1
                    
        tile[4] = num_of_surrounding_mines
                
    
#Find a tile using coordinates.
def find_tile_with_xy(x_cor, y_cor): #Take 2 coordinates.
    tile_index = x_cor + (y_cor * grid_tile_width) #Finding the index with the coordinates.
    return tile_list[tile_index] #Returning the tile using the index.

#Clear area
def clear_area_start(tile):
    
    tile_index = tile_list.index(tile)
    tiles_cleared.append(tile_index)
    if tile_index in tiles_left_to_clear:
        tiles_left_to_clear.remove(tile_index)
        
    change_tile_in_list(tile_list.index(tile), "discovered")
    
    #Defining the out of bounds coordinates.
    out_of_bounds_y = [-1, grid_tile_height]
    out_of_bounds_x = [-1, grid_tile_width]
    
    x_origin = tile[1]
    y_origin = tile[2]
    
    x_coords = [x_origin - 1, x_origin - 1, x_origin - 1, x_origin, x_origin, x_origin + 1, x_origin + 1, x_origin + 1]
    y_coords = [y_origin + 1, y_origin, y_origin - 1, y_origin - 1, y_origin + 1, y_origin + 1, y_origin, y_origin - 1]

    if tile_list[tile_index][4] == 0 and tile_list[tile_index][3] != "mine":
        for index in range(8):
            if x_coords[index] not in out_of_bounds_x and y_coords[index] not in out_of_bounds_y:
                current_tile_index = tile_list.index(find_tile_with_xy(x_coords[index], y_coords[index]))
                if current_tile_index not in tiles_left_to_clear and current_tile_index not in tiles_cleared and tile_list[current_tile_index][3] != "mine":
                    tiles_left_to_clear.append(current_tile_index)
    
def complete_clear_area():
    while tiles_left_to_clear != []:
        clear_area(tile_list[tiles_left_to_clear[0]])
        
    
def clear_area(tile):
    clear_area_start(tile)
    complete_clear_area()
    update_screen()



#############################
# Start Menu Function
#############################

def start_menu():
    
    ###########################
    # Creating images and rects
    
    start_screen_rect = start_screen.get_rect() #Defining a rect for the start screen.
    
    distance_to_move = (960 - start_screen_rect[2]) / 2 #Calculating how far the rect has to move to be centered.
    start_screen_rect = start_screen_rect.move(distance_to_move, distance_to_move) #Moving the rect to be centered.
    
    screen.blit(start_screen, start_screen_rect) #Placing image ontop of rect.
    
    #Creating the rect for the start button.
    start_button_rect = start_button.get_rect()
    
    #Moving the start button rect.
    start_button_rect = start_button_rect.move((960 - start_button_rect[2]) / 2, 550)
    
    #Adding an image to the start button rect.
    screen.blit(start_button, start_button_rect)
    
    #Creating the difficulty_button rects.
    easy_difficulty_button_rect = easy_difficulty_button.get_rect()
    moderate_difficulty_button_rect = moderate_difficulty_button.get_rect()
    difficult_difficulty_button_rect = difficult_difficulty_button.get_rect()
    very_difficult_difficulty_button_rect = very_difficult_difficulty_button.get_rect()
    
    #Used to determine how far the difficulty_buttons move.
    button_spacing = 20
    difficulty_button_width = easy_difficulty_button_rect[3]
    
    #Moving the rects for the difficulty_buttons.
    moderate_difficulty_button_rect = moderate_difficulty_button_rect.move((960 / 2) - (button_spacing / 2) - difficulty_button_width, 700)
    easy_difficulty_button_rect = easy_difficulty_button_rect.move((960 / 2) - (button_spacing / 2) - (difficulty_button_width * 2) - button_spacing, 700)
    difficult_difficulty_button_rect = difficult_difficulty_button_rect.move((960 / 2) + (button_spacing / 2), 700)
    very_difficult_difficulty_button_rect = very_difficult_difficulty_button_rect.move((960 / 2) + (button_spacing / 2) + (difficulty_button_width) + button_spacing, 700)
    
    #Adding images to the difficulty_buttons.
    screen.blit(easy_difficulty_button, easy_difficulty_button_rect)
    screen.blit(moderate_difficulty_button, moderate_difficulty_button_rect)
    screen.blit(difficult_difficulty_button, difficult_difficulty_button_rect)
    screen.blit(very_difficult_difficulty_button, very_difficult_difficulty_button_rect)
    
    pygame.display.flip() #Updating screen.
    
    
    #############################
    # User control of menu.
    
    
    end_click = True
    
    global number_of_mines
    global grid_tile_width
    global grid_tile_height
    
    while True:
        pygame.event.get()
        mouse_posistion = pygame.mouse.get_pos()
    
        if pygame.mouse.get_pressed(3)[0] == True and end_click == True:
            if easy_difficulty_button_rect.collidepoint(mouse_posistion) == True:
                print("easy difficulty selected")
                end_click = False
                
                number_of_mines = 10
                grid_tile_width = 10
                grid_tile_height = 10
                
        if pygame.mouse.get_pressed(3)[0] == True and end_click == True:
            if moderate_difficulty_button_rect.collidepoint(mouse_posistion) == True:
                print("moderate difficulty selected")
                end_click = False
                
                number_of_mines = 40
                grid_tile_width = 15
                grid_tile_height = 15
                
        if pygame.mouse.get_pressed(3)[0] == True and end_click == True:
            if difficult_difficulty_button_rect.collidepoint(mouse_posistion) == True:
                print("difficult difficulty selected")
                end_click = False
                
                number_of_mines = 80
                grid_tile_width = 20
                grid_tile_height = 20
                
        if pygame.mouse.get_pressed(3)[0] == True and end_click == True:
            if very_difficult_difficulty_button_rect.collidepoint(mouse_posistion) == True:
                print("very difficult difficulty selected")
                end_click = False
                
                number_of_mines = 200
                grid_tile_width = 25
                grid_tile_height = 25
                
        if pygame.mouse.get_pressed(3)[0] == True and end_click == True:
            if start_button_rect.collidepoint(mouse_posistion) == True:
                print("start selected")
                end_click = False

                break
                
        if pygame.mouse.get_pressed(3)[0] != True:
            end_click = True
            
###########################
# Game Control
###########################

start_menu()

for row in range(grid_tile_height):
    for columb in range(grid_tile_width):
        add_new_tile_to_list(columb, row)
print(tile_list)
        
for tile in tile_list:
    tile[0] = tile[0].move(tile_origin_x + (tile[1] * tile_size), tile_origin_y + (tile[2] * tile_size))
    
for tile in tile_list:
    screen.blit(undiscovered_tile, tile[0])
    
pygame.display.flip()

update_screen()


#################################
# First Click (Mines spawn after)

end_click = False

while True:
    pygame.event.get()
    mouse_posistion = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed(3)[0] == True and end_click == True:
        for tile in tile_list:
            if tile[0].collidepoint(mouse_posistion) == True:
                first_tile_clicked = tile
                print("it worked")
                end_click = False
                break
            
    if pygame.mouse.get_pressed(3)[0] != True:
        end_click = True
    if first_tile_clicked != []:
        break
    
print("done")
    
add_mines_to_level()

find_surrounding_mines()

clear_area(first_tile_clicked)

#################################
# Main Game

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
                
                if tile[3] != "mine" and tile[5] != "flag":
                    
                    clear_area(tile)
                
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
                if tile[3] == "undiscovered" or tile[3] == "mine":
                    if tile[5] != "flag":
                        tile[5] = "flag"
                    else:
                        tile[5] = ""
        update_screen()
                
        end_r_click = False
    if pygame.mouse.get_pressed(3)[2] == False:
        end_r_click = True