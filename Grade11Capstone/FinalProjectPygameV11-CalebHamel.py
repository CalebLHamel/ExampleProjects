##################################
# Final Project V11
# Caleb Hamel
# 2021/1/20
##################################

#####################
# Notes
#####################
# Screen size determines how big many of the textures are, this often involves lots of math.
# The game will force the width to be greater than or equal to the height, otherwise many textures would break.
# I did not initially create the program to have an adjustable screen size. I had to edit that in
#    once I realized that the school computers use a lower resolution screen.
# Screens taller than they are wide will not be full-screen. I don't know why you'd use one anyways.
# A tile is a list [rect, xcor, ycor, type, num_of_surrounding_mines, flag]
# The game's rects are created from the images which are scaled to the correct size beforehand.
# Image sizes do not matter to the program. The program resizes them anyways. (Playability is affected though).
# The game's folder has more folders that contain images for the program. All images have been made in...
# ...Microsoft Paint, or Microsoft Paint 3D (for the transparent backgrounds).
# I downloaded some Creative Commons sounds and credited them in a folder titled "CREDIT".
# There are some print statements throughout the program. These helped me to debug the program.
# It is impossible to click on a mine on the first click. The mines are generated after the first click and a certain distance away.

#####################
# How the game runs.
#####################
# Initially, the game will create variables, they are changed in the menu screen as the difficulty is chosen.
# Then, the grid is generated when the game starts.
# The user clicks on a tile to be there starting point.
# Mines are now generated, avoiding where the user initially clicked.
# A function is then run to allow each tile to 'know' how many mines surround it.
# The area around the user's starting point is cleared.
# The play_game() function then controls the game.
# The user continues to clear and flag mines until they win or lose.
# The game_over variable determines the end screen. (YOU WIN! or GAME OVER!)
# All mines are revealed if the user lost.
# The game_end() function allows the user to play again or quit.
# This determines whether the game starts over, or ends.




##############################
#Modules and intitialization.
##############################


# Importing Modules
import pygame, math, random 

pygame.init()




###############################
# Setting up the Screen
###############################


screen_size = pygame.display.get_desktop_sizes()[0] #Gets the screen's size.
width, height = screen_size[0], screen_size[1] #Defines the width and height of the screen.

#The program breaks if the height is greater than the width, this prevents that.
if height > width:
    old_width = width
    width = height
    height = old_width
    
screen_size = width, height # Easy way of giving 2 dimensions at once.

#Creating a screen with a certain size.
screen = pygame.display.set_mode(screen_size)

#Defining a color for the screen fill..
grey = 100, 100, 100

#Fills the entire screen with grey.
screen.fill(grey)

#Updates the screen
pygame.display.flip()

if width <= height: #Ensures that the grid doesn't go off the screen border.
    max_grid_size = math.floor((width * .7)) #Maximum size of the grid
else:
    max_grid_size = math.floor((height * .7)) #Maximum size of the grid




###############################
# Loading sound files.
###############################


explosion_sound = pygame.mixer.Sound("sounds/willlewis__musket-explosion.wav")
click_sound = pygame.mixer.Sound("sounds/eminyildirim__ui-click.wav")
victory_sound = pygame.mixer.Sound("sounds/337049__shinephoenixstormcrow__320655-rhodesmas-level-up-01.mp3")




###############################
# Loading and altering images
###############################


###############
# Grid textures.

#Loading the image textures for the numbers..
images_to_load = ["one", "two", "three", "four", "five", "six", "seven", "eight"] #Names of all the number images.
number_images = [] #List containing all number textures.

#Adds all the number images to the number_images list.
for image in images_to_load:
    number_images.append(pygame.image.load("numbers/" + image + ".png"))

undiscovered_tile = pygame.image.load("level_textures/undiscovered_tile.png") #The undiscovered tile.

discovered_tile = pygame.image.load("level_textures/discovered_tile.png") #The discovered tile.

flag = pygame.image.load("level_textures/flag.png") #The flag.

mine = pygame.image.load("level_textures/mine.png") #The mine
    
    
###############
# Menu Textures

#Start screen texture.
start_screen = pygame.image.load("title_screen/title_screen.png")
start_screen = pygame.transform.scale(start_screen, (max_grid_size, max_grid_size))

#Difficulty button textures.
difficulty_button_size = ((math.floor(max_grid_size * .15), math.floor(max_grid_size * .15)))

easy_difficulty_button = pygame.transform.scale(pygame.image.load("title_screen/easy_difficulty_button.png"), difficulty_button_size)
moderate_difficulty_button = pygame.transform.scale(pygame.image.load("title_screen/moderate_difficulty_button.png"), difficulty_button_size)
difficult_difficulty_button = pygame.transform.scale(pygame.image.load("title_screen/difficult_difficulty_button.png"), difficulty_button_size)
very_difficult_difficulty_button = pygame.transform.scale(pygame.image.load("title_screen/verydifficult_difficulty_button.png"), difficulty_button_size)

#Start button texture.
start_button = pygame.image.load("title_screen/start_button.png")
start_button = pygame.transform.scale(start_button, (math.floor(max_grid_size * .2), math.floor(max_grid_size * .12)))

#Difficulty Selection Texture.
difficulty_selection = pygame.image.load("title_screen/difficulty_selection.png")
difficulty_selection = pygame.transform.scale(difficulty_selection, difficulty_button_size)


##################
#Game end textures
    
game_won_screen = pygame.image.load("game_over_screen/user_won_screen.png")
game_won_screen = pygame.transform.scale(game_won_screen, (max_grid_size, math.floor(height * .1)))

game_lost_screen = pygame.image.load("game_over_screen/user_lost_screen.png")
game_lost_screen = pygame.transform.scale(game_lost_screen, (max_grid_size, math.floor(height * .1)))

play_again_button = pygame.image.load("game_over_screen/play_again_button.png")
play_again_button = pygame.transform.scale(play_again_button, (math.floor(max_grid_size * .2), math.floor(max_grid_size * .1)))

quit_game_button = pygame.image.load("game_over_screen/quit_game_button.png")
quit_game_button = pygame.transform.scale(quit_game_button, (math.floor(max_grid_size * .2), math.floor(max_grid_size * .1)))

game_end_rect = game_won_screen.get_rect()
game_end_button_rect = play_again_button.get_rect()




########################################
# Defining Variables and Default values.
########################################


number_of_mines = 40 #Mines on grid.
grid_tile_width = 15 #How many tiles wide the grid is.
grid_tile_height = 15 #How many tiles hight the grid is.

tile_rect = undiscovered_tile.get_rect()
tile_size = tile_rect[2]
tile_resize = 0 #Size that tiles will be set to.
tile_origin_x = 0 #Origin point for top left tile.
tile_origin_y = 0 #Origin point for top left tile.
tile_list = []
first_tile_clicked = []
tiles_cleared = []
tiles_left_to_clear = []
game_over = False

#These are all the variables that affect how to game plays. They are grouped together for easy reasignent from a return function.
game_variables = (number_of_mines, grid_tile_width, grid_tile_height, tile_resize, tile_origin_x,
                          tile_origin_y, tile_list, first_tile_clicked, tiles_cleared, tiles_left_to_clear,
                          undiscovered_tile, discovered_tile, flag, mine, tile_rect, tile_size, game_over)




##########################
# Functions
##########################


#Function to check if the user wants to quit.
def check_for_quit():
    for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit()
                if event.type == pygame.QUIT:
                    quit()
                
                
                
#Add a new tile to the list of tiles.
def add_new_tile_to_list(xcor, ycor):
    new_tile_rect = undiscovered_tile.get_rect()
    new_tile = [new_tile_rect, xcor, ycor, "undiscovered", 0, ""]
    tile_list.append(new_tile)
    
    
    
#Changing a tile in the list.
def change_tile_in_list(tile_number, tile_type):
    
    #Changing the tile type of a specific tile.
    tile_list[tile_number][3] = tile_type
    
    
    
#Update the screen.
def update_screen():
    
    screen.fill(grey) #To prevent a 'lagging' appearance.
    
    for tile in tile_list: #For each tile.
        
        
            
        if tile[3] == "undiscovered" or tile[3] == "mine": #If tile is undiscovered, make them look like it.
            screen.blit(undiscovered_tile, tile[0])
         
         
        if tile[3] == "mine" and game_over == True: #If the tile has a mine, and the game is lost, display the mine.
            screen.blit(mine, tile[0])
            
            
        if tile[5] == "flag": #If they have a flag, make it appear.
            screen.blit(flag, tile[0])
             
        elif tile[3] == "discovered": #If they are discovered, make them look like it..
            screen.blit(discovered_tile, tile[0])
        
        
        if tile[3] == "discovered": #If they have been discovered, label them with how many mines surrount them.
            for number in range(8): #8 possible numbers.
                if number + 1 == tile[4]: #If the number matches the 4th element of tile.
                    screen.blit(number_images[number], tile[0]) #Make the matching number appear.
                    
    pygame.display.flip() #Update the screen now that the changes have finished.              



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
                
            else: #If the mines are too close to where the user clicked first, try again.
                continue
        
    print(mine_cords_list) #For debugging.
    
    for tile in tile_list: #For each tile.
        for mine_cords in mine_cords_list:#For each mine coordinate.
            
            if tile[1] == mine_cords[0] and tile[2] == mine_cords[1]: #If their coordinates match
                tile[3] = "mine" #Make the tile a mine.


                
#Function to determine how many mines surround a tile.
def find_surrounding_mines():
    for tile in tile_list:
        
        #Defining the 'out of bounds' so the program doesn't try to check their and crash.
        out_of_bounds_y = [-1, grid_tile_height]
        out_of_bounds_x = [-1, grid_tile_width]
    
        #Where the current tile it.
        x_origin = tile[1]
        y_origin = tile[2]
    
        #Possible x and y coordinates of surrounding tiles.
        x_coords = [x_origin - 1, x_origin - 1, x_origin - 1, x_origin, x_origin, x_origin + 1, x_origin + 1, x_origin + 1]
        y_coords = [y_origin + 1, y_origin, y_origin - 1, y_origin - 1, y_origin + 1, y_origin + 1, y_origin, y_origin - 1]

        num_of_surrounding_mines = 0 #Counter to keep track.
        
        #For every possible surrounding tile.
        for index in range(8):
            
            if x_coords[index] not in out_of_bounds_x and y_coords[index] not in out_of_bounds_y: #If coordinates are in bounds.
                
                surrounding_tile = find_tile_with_xy(x_coords[index], y_coords[index]) #Find a tile using its coordinates.
                
                #Increase the counter if the tile is a 'mine' tile.
                if surrounding_tile[3] == "mine":
                    num_of_surrounding_mines += 1
                   
        #update the current tile's element to the right value.
        tile[4] = num_of_surrounding_mines
    
    
    
#Find a tile using coordinates.
def find_tile_with_xy(x_cor, y_cor): #Take 2 coordinates.
    
    tile_index = x_cor + (y_cor * grid_tile_width) #Finding the index with the coordinates.
    return tile_list[tile_index] #Returning the tile using the index.



#Clear area
def clear_area_start(tile):
    
    tile_index = tile_list.index(tile) #Index of the tile.
    tiles_cleared.append(tile_index) #Used to prevent infinite loops.
    
    #Remove it from the lineup of tiles to clear to prevent infinie loops.
    if tile_index in tiles_left_to_clear:
        tiles_left_to_clear.remove(tile_index)
        
    #Tile has been discovered, or "cleared".
    change_tile_in_list(tile_list.index(tile), "discovered")
    
    #Defining the out of bounds coordinates.
    out_of_bounds_y = [-1, grid_tile_height]
    out_of_bounds_x = [-1, grid_tile_width]
    
    #Coordinates of current tile.
    x_origin = tile[1]
    y_origin = tile[2]
    
    #Possible x and y coordinates of surrounding tiles.
    x_coords = [x_origin - 1, x_origin - 1, x_origin - 1, x_origin, x_origin, x_origin + 1, x_origin + 1, x_origin + 1]
    y_coords = [y_origin + 1, y_origin, y_origin - 1, y_origin - 1, y_origin + 1, y_origin + 1, y_origin, y_origin - 1]

    #If the current tile has no surrounding mines, then check the surrounding tiles.
    if tile_list[tile_index][4] == 0 and tile_list[tile_index][3] != "mine":
        for index in range(8):
            if x_coords[index] not in out_of_bounds_x and y_coords[index] not in out_of_bounds_y: #If surrounding tile is in bounds, find its index.
                current_tile_index = tile_list.index(find_tile_with_xy(x_coords[index], y_coords[index]))
                
                #If the tile's index is not in the tiles left to clear list, or the tiles already cleared list, and is not a mine, then add it to the list of tiles left to clear.
                if current_tile_index not in tiles_left_to_clear and current_tile_index not in tiles_cleared and tile_list[current_tile_index][3] != "mine":
                    tiles_left_to_clear.append(current_tile_index)
    
    
    
#Function clear the entire area using the list of tiles left to clear.
def complete_clear_area():
    while tiles_left_to_clear != []:
        clear_area_start(tile_list[tiles_left_to_clear[0]])
        
    

#Function to clear an entire area starting from a tile. Uses 2 other function to clear the area (not counting update_screen())
def clear_area(tile):
    clear_area_start(tile)
    complete_clear_area()
    update_screen()



#Function for the first click of the game.
def first_click():
    end_click = False
    new_first_tile_clicked = []
    
    while True:
        check_for_quit()
        pygame.event.get()
        mouse_posistion = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed(3)[0] == True and end_click == True:
            for tile in tile_list:
                if tile[0].collidepoint(mouse_posistion) == True:
                    click_sound.play()
                    new_first_tile_clicked = tile
                    end_click = False
                    break
            
        if pygame.mouse.get_pressed(3)[0] != True:
            end_click = True
        if new_first_tile_clicked != []:
            return new_first_tile_clicked
        
        
    
#Function to generate the grid.
def generate_grid():
    for row in range(grid_tile_height):
        for columb in range(grid_tile_width):
            add_new_tile_to_list(columb, row)
        
    for tile in tile_list:
        tile[0] = tile[0].move(tile_origin_x + (tile[1] * tile_size), tile_origin_y + (tile[2] * tile_size))
    
    update_screen()
    
    
    
# Prevents the images from losing quality.
def reload_grid_textures():
    new_undiscovered_tile = pygame.image.load("level_textures/undiscovered_tile.png") #The undiscovered tile.

    new_discovered_tile = pygame.image.load("level_textures/discovered_tile.png") #The discovered tile.

    new_flag = pygame.image.load("level_textures/flag.png") #The flag.

    new_mine = pygame.image.load("level_textures/mine.png") #The mine
    
    #Loading the image textures for the numbers..
    images_to_load = ["one", "two", "three", "four", "five", "six", "seven", "eight"] #Names of all the number images.
    
    new_number_images = [] #List containing all number textures.
    
    #Adds all the number images to the number_images list.
    for image in images_to_load:
        new_number_images.append(pygame.image.load("numbers/" + image + ".png"))
        
    return (new_undiscovered_tile, new_discovered_tile, new_flag, new_mine, new_number_images)



#Function for the main game.
def play_game():
    
    game_over = False
    end_click = False

    while True: #Controls the game.
    
        check_for_quit()
        
        pygame.event.get() #Needed for mouse.get_pressed to work.

        #If the mouse button was pressed down.
        if pygame.mouse.get_pressed(3)[0] == True and end_click == True: #If the mouse button is pressed down.
            mouse_posistion = pygame.mouse.get_pos() #Gets the mouse position.
        
            for tile in tile_list: #For every tile.
                current_index = tile_list.index(tile)
                if tile[0].collidepoint(mouse_posistion) == True: #If the mouse is overtop of the tile.
                    click_sound.play()
                    print("You clicked on tile number " + str(tile_list.index(tile)) + ".") #For debugging.
                    print(tile) #Debugging
                
                    if tile[3] != "mine" and tile[5] != "flag":
                        clear_area(tile)
                
                    if tile[3] == "mine" and tile[5] != "flag": #Debugging.
                        game_over = True
                    
                    end_click = False #Mouse button has not been released.
            update_screen()
        
            if game_over == True: #If the user clicked on a mine.
                print("game over") #Debugging.
                return game_over #used to signal the game's end.
            
            
        if pygame.mouse.get_pressed(3)[0] == False: #If the button is up.
            end_click = True #The mouse button has now been released.
        
    
        if pygame.mouse.get_pressed(3)[2] == True and end_r_click == True: #If right mouse down.
            
            mouse_posistion = pygame.mouse.get_pos() #Gets the mouse position.
            
            for tile in tile_list: #Once for every tile.
                
                if tile[0].collidepoint(mouse_posistion) == True: #If the mouse is overtop of the tile.
                    click_sound.play()
                    
                    if tile[3] != "discovered": #If the tile is not discovered.
                        if tile[5] != "flag": #Places a flag if there isn't one there.
                            tile[5] = "flag"
                        else: #Removes a flag if there is one there.
                            tile[5] = ""
                            
            update_screen()
                
            end_r_click = False #Signals that the right mouse button is down.
            
            
        #Determines if the right mouse button went up. Used for better control of the game.
        if pygame.mouse.get_pressed(3)[2] == False:
            end_r_click = True
        
        
        #These are used to determine if the user won.
        correct_flags = 0
        total_cleared_tiles = 0
        
        for tile in tile_list:
            if tile[3] == "mine" and tile[5] == "flag": #If the flag is on a mine, increment correct_flags.
                correct_flags += 1
            if tile[3] == "discovered": #For every blank tile, increment total_cleared_tiles.
                total_cleared_tiles += 1
    
        #If all the mines have flags, and all other tiles have been cleared, the game is won.
        if correct_flags == number_of_mines and total_cleared_tiles == (grid_tile_width * grid_tile_height) - number_of_mines:
            break



#End game function.
def game_end():
    
    #Moving the rectangle for the game_end display.
    local_game_end_rect = game_end_rect.move((width / 2) - (game_end_rect[2] / 2) , 20)
    
    
    #Display the appropiate image and play the appropiate sound depending on whether the user won or lost.
    if game_over == True:
        explosion_sound.play()
        pygame.time.wait(3000)
        screen.blit(game_lost_screen, local_game_end_rect)
    else:
        victory_sound.play()
        pygame.time.wait(3000)
        screen.blit(game_won_screen, local_game_end_rect)
        
        
    #Moving rectangles and applying images for the buttons.
    local_play_again_button_rect = game_end_button_rect.move(width / 2, height * .045)
    screen.blit(play_again_button, local_play_again_button_rect)
    local_quit_button_rect = game_end_button_rect.move(width / 2 + max_grid_size * .25, height * .045)
    screen.blit(quit_game_button, local_quit_button_rect)
    
    #Updating screen so that the display appears. (No fill was used to keep the appearance of the grid)
    pygame.display.flip()
        

    end_click = False #Used to ensure a proper click rather than holding and moving the mouse.
    
    while True:
        check_for_quit()
        
        pygame.event.get()
        
        mouse_posistion = pygame.mouse.get_pos() #Used to determine where the mouse is.
    
        #If play_again button is pressed, return True.
        if pygame.mouse.get_pressed(3)[0] == True and end_click == True:
            if local_play_again_button_rect.collidepoint(mouse_posistion) == True:
                click_sound.play()
                return True
            
        #If quit button is pressed, return False.
        if pygame.mouse.get_pressed(3)[0] == True and end_click == True:
            if local_quit_button_rect.collidepoint(mouse_posistion) == True:
                click_sound.play()
                return False
            
        #If mouse button is down, end_click = False to ensure that only proper clicks are accepted.
        if pygame.mouse.get_pressed(3)[0] == True:
            end_click = False
            
        #If mouse button is up, end_click = True.
        if pygame.mouse.get_pressed(3)[0] == False:
            end_click = True
    
    
    
    
#############################
# Start Menu Function
#############################


#Function for the graphics of the start menu.
def start_menu_graphics(difficulty):
    ###########################
    # Creating images and rects
    screen.fill(grey)
    
    start_screen_rect = start_screen.get_rect()
        
    distance_to_move_x = ((width / 2) - (start_screen_rect[2] / 2)) #Calculating how far the rect has to move to be centered.
    distance_to_move_y = ((height / 2) - (start_screen_rect[2] / 2))
    
    start_screen_rect = start_screen_rect.move(distance_to_move_x, distance_to_move_y) #Moving the rect to be centered.
    
    screen.blit(start_screen, start_screen_rect) #Placing image ontop of rect.
    
    #Creating the rect for the start button and button selection.
    start_button_rect = start_button.get_rect()
    difficulty_selection_rect = easy_difficulty_button.get_rect().copy()
    
    #Moving the start button rect.
    start_button_rect = start_button_rect.move(((width / 2) - (start_button_rect[2] / 2)), height * .58)
    
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
    moderate_difficulty_button_rect = moderate_difficulty_button_rect.move((width / 2) - (button_spacing / 2) - difficulty_button_width, max_grid_size * 1.05)
    easy_difficulty_button_rect = easy_difficulty_button_rect.move((width / 2) - (button_spacing / 2) - (difficulty_button_width * 2) - button_spacing, max_grid_size * 1.05)
    difficult_difficulty_button_rect = difficult_difficulty_button_rect.move((width / 2) + (button_spacing / 2), max_grid_size * 1.05)
    very_difficult_difficulty_button_rect = very_difficult_difficulty_button_rect.move((width / 2) + (button_spacing / 2) + (difficulty_button_width) + button_spacing, max_grid_size * 1.05)
    
    
    #Moves the red button outline overtop of the correct button, determined by which button is currently selected.
    if difficulty == "easy":
        difficulty_selection_rect = difficulty_selection_rect.move((width / 2) - (button_spacing / 2) - (difficulty_button_width * 2) - button_spacing, max_grid_size * 1.05)
    elif difficulty == "moderate":
        difficulty_selection_rect = difficulty_selection_rect.move((width / 2) - (button_spacing / 2) - difficulty_button_width, max_grid_size * 1.05)
    elif difficulty == "difficult":
        difficulty_selection_rect = difficulty_selection_rect.move((width / 2) + (button_spacing / 2), max_grid_size * 1.05)
    elif difficulty == "very_difficult":
        difficulty_selection_rect = difficulty_selection_rect.move((width / 2) + (button_spacing / 2) + (difficulty_button_width) + button_spacing, max_grid_size * 1.05)

    #Difficulty is easy by default, when no button has been selected, easy is chosen.
    else:
        difficulty_selection_rect = difficulty_selection_rect.move((width / 2) - (button_spacing / 2) - (difficulty_button_width * 2) - button_spacing, max_grid_size * 1.05)
    
    
    #Adding images to the difficulty_buttons.
    screen.blit(easy_difficulty_button, easy_difficulty_button_rect)
    screen.blit(moderate_difficulty_button, moderate_difficulty_button_rect)
    screen.blit(difficult_difficulty_button, difficult_difficulty_button_rect)
    screen.blit(very_difficult_difficulty_button, very_difficult_difficulty_button_rect)
    
    #Button outline.
    screen.blit(difficulty_selection, difficulty_selection_rect)
    
    pygame.display.flip() #Updating screen.
    
    
    
#Function for the functionality of the start menu.
def start_menu(difficulty):
    
    start_menu_graphics(difficulty) #Display the correct graphics.
    
    #Creating the rect for the start button and button selection.
    start_button_rect = start_button.get_rect()
    difficulty_selection_rect = difficulty_selection.get_rect()
    
    #Moving the start button rect.
    start_button_rect = start_button_rect.move(((width / 2) - (start_button_rect[2] / 2)), height * .58)
    
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
    moderate_difficulty_button_rect = moderate_difficulty_button_rect.move((width / 2) - (button_spacing / 2) - difficulty_button_width, max_grid_size * 1.05)
    easy_difficulty_button_rect = easy_difficulty_button_rect.move((width / 2) - (button_spacing / 2) - (difficulty_button_width * 2) - button_spacing, max_grid_size * 1.05)
    difficult_difficulty_button_rect = difficult_difficulty_button_rect.move((width / 2) + (button_spacing / 2), max_grid_size * 1.05)
    very_difficult_difficulty_button_rect = very_difficult_difficulty_button_rect.move((width / 2) + (button_spacing / 2) + (difficulty_button_width) + button_spacing, max_grid_size * 1.05)
    
    
    #All the variables that can be changed through this function.
    new_number_of_mines = 10
    new_grid_tile_width = 10
    new_grid_tile_height = 10
    new_tile_resize = tile_resize
    new_tile_origin_x = tile_origin_x
    new_tile_origin_y = tile_origin_y
    new_tile_list = tile_list
    new_first_tile_clicked = first_tile_clicked
    new_tiles_cleared = tiles_cleared
    new_tiles_left_to_clear = tiles_left_to_clear
    new_undiscovered_tile = undiscovered_tile
    new_discovered_tile = discovered_tile
    new_flag = flag
    new_tile_rect = tile_rect
    new_tile_size = tile_size
    new_game_over = game_over
    new_mine = mine
    

    #############################
    # User control of menu.
    
    end_click = True
    
    while True:
        
        check_for_quit()
                
        pygame.event.get()
        mouse_posistion = pygame.mouse.get_pos()
    
        #If the easy difficulty button is pressed, change the variables to reflect the difficulty.
        if pygame.mouse.get_pressed(3)[0] == True and end_click == True:
            if easy_difficulty_button_rect.collidepoint(mouse_posistion) == True:
                click_sound.play()
                print("easy difficulty selected")
                start_menu_graphics("easy")
                end_click = False
                
                new_number_of_mines = 10
                new_grid_tile_width = 10
                new_grid_tile_height = 10
               
               
        #If the easy difficulty button is pressed, change the variables to reflect the difficulty.
        if pygame.mouse.get_pressed(3)[0] == True and end_click == True:
            if moderate_difficulty_button_rect.collidepoint(mouse_posistion) == True:
                click_sound.play()
                print("moderate difficulty selected")
                start_menu_graphics("moderate")
                end_click = False
                
                new_number_of_mines = 40
                new_grid_tile_width = 15
                new_grid_tile_height = 15
            
            
        #If the easy difficulty button is pressed, change the variables to reflect the difficulty.
        if pygame.mouse.get_pressed(3)[0] == True and end_click == True:
            if difficult_difficulty_button_rect.collidepoint(mouse_posistion) == True:
                click_sound.play()
                print("difficult difficulty selected")
                start_menu_graphics("difficult")
                end_click = False
                
                new_number_of_mines = 80
                new_grid_tile_width = 20
                new_grid_tile_height = 20
           
           
        #If the easy difficulty button is pressed, change the variables to reflect the difficulty.      
        if pygame.mouse.get_pressed(3)[0] == True and end_click == True:
            if very_difficult_difficulty_button_rect.collidepoint(mouse_posistion) == True:
                click_sound.play()
                print("very difficult difficulty selected")
                start_menu_graphics("very_difficult")
                end_click = False
                
                new_number_of_mines = 200
                new_grid_tile_width = 25
                new_grid_tile_height = 25
                
                
        #If the start button was pressed, break the loop (starts the game).
        if pygame.mouse.get_pressed(3)[0] == True and end_click == True:
            if start_button_rect.collidepoint(mouse_posistion) == True:
                click_sound.play()
                print("start selected")
                end_click = False

                break
        
        #Used to tell if the left mouse button went up.
        if pygame.mouse.get_pressed(3)[0] != True:
            end_click = True
            
            
    # Re-defining variables (resets them for the new game, or changes them based on difficulty).
    
    new_game_over = False #New game, game is no longer over.
    
    #Determines how big the tiles need to be.
    if grid_tile_width >= grid_tile_height:
        new_tile_resize = math.floor(max_grid_size / new_grid_tile_width)
    else:
        new_tile_resize = math.floor(max_grid_size / new_grid_tile_height)
             
    #Where the corner of the grid would be.
    new_tile_origin_x = (width / 2) - (max_grid_size / 2)
    new_tile_origin_y = (height / 2) - (max_grid_size / 2)

    #Clears the previous grid, new grid will be generated.
    new_tile_list = []

    #New game, there will need to be a new first_tile_clicked.
    new_first_tile_clicked = []

    #No tiles have been cleared in the new game.
    new_tiles_cleared = []
    new_tiles_left_to_clear = []
    
    
    #########################
    #Resizing game elements.
    
    #Resizing the numbers.
    for image in range(len(number_images)):
        number_images[image] = pygame.transform.scale(number_images[image], (new_tile_resize,new_tile_resize))
    
    #Resizing the tile images.
    new_undiscovered_tile = pygame.transform.scale(new_undiscovered_tile, (new_tile_resize,new_tile_resize))
    new_discovered_tile = pygame.transform.scale(new_discovered_tile, (new_tile_resize,new_tile_resize))
    new_flag = pygame.transform.scale(new_flag, (new_tile_resize,new_tile_resize))
    new_mine = pygame.transform.scale(new_mine, (new_tile_resize,new_tile_resize))

    #Resizing the undiscovered tile rect.
    new_tile_rect = new_undiscovered_tile.get_rect()

    new_tile_size = new_tile_rect[2] #Size of the tiles.
    
    #All the new variables packed together to be returned.
    new_game_variables = (new_number_of_mines, new_grid_tile_width, new_grid_tile_height, new_tile_resize, new_tile_origin_x,
                          new_tile_origin_y, new_tile_list, new_first_tile_clicked, new_tiles_cleared, new_tiles_left_to_clear,
                          new_undiscovered_tile, new_discovered_tile, new_flag, new_mine, new_tile_rect, new_tile_size, new_game_over)
    
    #Returning the new variables.
    return new_game_variables
    



###########################
# Game Control
###########################


while True:
    
    #Reloading the images to prevent distortion as they are repeatedly resized.
    (undiscovered_tile, discovered_tile, flag, mine, number_images) = reload_grid_textures()
    print(number_images)
    game_variables = start_menu("easy") #Start menu and setting variable values.
    
    #Variables set to proper values.
    (number_of_mines, grid_tile_width, grid_tile_height, tile_resize, tile_origin_x,
    tile_origin_y, tile_list, first_tile_clicked, tiles_cleared, tiles_left_to_clear,
    undiscovered_tile, discovered_tile, flag, mine, tile_rect, tile_size, game_over) = game_variables

    generate_grid() #Generating the grid.
  
    first_tile_clicked = first_click() #User clicks on the grid.

    add_mines_to_level() #Mines are now added (so that the user doesn't start by clicking on a mine).

    find_surrounding_mines() #Each tile's surrounding mine is determined.

    clear_area(first_tile_clicked) #Clearing where the user first clicked.
   
    game_over = play_game() #Game is played until the user wins, or loses. Determines what end screen is shown.
    
    update_screen() #Reveals all the mines if the user lost.
    
    if game_end() == True: #If user chose "play again", then the game restarts.
        continue
    
    else: #If the user chose quit, the program ends.
        pygame.time.wait(800)
        quit()