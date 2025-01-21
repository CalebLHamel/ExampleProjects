#############################
# Final Project V1
# Caleb Hamel
# 12/22/2021
#############################

import turtle, random

#turtle.tracer(0, 0)

#Setting up the window.
window = turtle.Screen()

window.setup(600, 600)
window.setworldcoordinates(-600, -600, 600, 600)

pen = turtle.Turtle() #Defining a turtle.
pen.penup()
pen.pensize(2)
pen.speed(0)

coordinate_limit = 500 #Maximum distance away from 0.
possible_sizes = [10, 50]



def draw_grid(a_turtle, size):
    
    distance = (coordinate_limit * 2) / size #Distance between 2 grid lines.
    
    pen.goto(-coordinate_limit, -coordinate_limit) #Bottom left.
    
    #Making the grid.
    for columb in range(size+1):
        pen.pendown()
        pen.goto(pen.xcor(),coordinate_limit)
        pen.penup()
        pen.goto(pen.xcor() + distance, -coordinate_limit)
        
    pen.goto(-coordinate_limit, -coordinate_limit)
    
    for row in range(size+1):
        pen.pendown()
        pen.goto(coordinate_limit, pen.ycor())
        pen.penup()
        pen.goto(-coordinate_limit, pen.ycor() + distance)
        

def create_mines(a_turtle, size, number_of_mines):
    coordinate_interval = (coordinate_limit * 2) / size #Spacing between coordinates for the mines.
    
    for mine in range(number_of_mines):
        while True:
            new_mine = [random.randrange(-500+(0.5*coordinate_interval),501 - (0.5*coordinate_interval), coordinate_interval), (random.randrange(-500+(0.5*coordinate_interval),501 - (0.5*coordinate_interval), coordinate_interval))]
        
            if new_mine in all_mines:
                continue
            else:
                all_mines.append(new_mine)
                break
        
        
all_mines = []
create_mines(pen, 25, 10)
print(all_mines)
print(len(all_mines))


        
draw_grid(pen, 25)

for mine in range(len(all_mines)):
    print(mine)
    pen.penup()
    pen.goto(all_mines[mine][0],all_mines[mine][1])
    print(pen.xcor() / 40)
    print(pen.ycor() / 40)
    pen.color("red")
    pen.pendown()
    pen.fd(10)
    pen.right(180)
    pen.fd(20)
    pen.right(180)


window.exitonclick()