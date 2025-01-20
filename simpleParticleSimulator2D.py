##############################
# Caleb Hamel
# 23/10/2023
# 2D Particle Simulator
##############################

'''
This is one of my older projects that I worked on occassionally in first year for fun.
Unfortunately I did not know how to use Git at this time so there's not much of a version history other than some file backups.
A lot of this was also done later at night after completing my homework and studying so I apologize for any mistakes it may
contain as a result.
The function docstrings are lacking too.

A lot of this uses style I was taught in my high school courses.
Pygame was an optional library that was available for my class to use in Computer Science 20 and 30.
I mainly just used Pygame for the window and drawing circles.

Different 'demos' of this project can be ran by changing which sections were commented out.

At some point I plan to remake this project in Java since I learned about a lot of design patterns since making this project.
'''

# Importing modules
import pygame, math, time, random

pygame.init()

total_collisions = 0

###############################
# Setting up the Screen
###############################

#Colors
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
red = pygame.Color(255,0,0)
green = pygame.Color(0,255,0)
blue = pygame.Color(0,0,255)
yellow = pygame.Color(255,255,0)
magenta = pygame.Color(255,0,255)
cyan = pygame.Color(0,255,255)

screen_size = pygame.display.get_desktop_sizes()[0] #Gets the screen's size.
width, height = screen_size[0], screen_size[1] #Defines the width and height of the screen.
screen_size = width, height

#Creating the screen.
screen = pygame.display.set_mode(screen_size)
screen.fill(black)



##############################
# Default Simulation Settings.
##############################

screen_bound = False

do_gravity = False
gravity_coefficient = 1



##############################
# Classes
##############################

#Class for what a particle is.
class Particle():
    #Particles have mass, radius, charge, position, and velocity. Additionally, color.
    def __init__(self, mass, radius, charge, position_x, position_y, velocity_x, velocity_y, color):
        self.mass = mass
        self.radius = radius
        self.charge = charge

        self.position_x = position_x
        self.position_y = position_y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

        self.color = color

        self.force_x = 0
        self.force_y = 0

        #Where the particle could move given no obstacles.
        self.potential_new_position_x = position_x
        self.potential_new_positiony = position_y

        #The effects of collision. A change of velocity.
        self.collision_change_x = 0
        self.collision_change_y = 0


    #Draws the particle to the screen.
    def draw(self, offset_x=0, offset_y=0, color=None):
        if color==None:
            color=self.color

        pygame.draw.circle(screen, color, (self.position_x-offset_x, self.position_y-offset_y), self.radius)


    #Calculates forces acting on the particle.
    def fields(self, particles):
        #The net force acting on the particle.
        net_force_x = 0
        net_force_y = 0

        #Checking the effect of each particle.
        for p in particles:
            if p is self: #Particle has no effect on itself.
                continue

            #Calculating the magnitude of force.
            distance_squared = (self.position_x-p.position_x)**2 + (self.position_y-p.position_y)**2

            force_magnitude = (self.charge * p.charge) / distance_squared
            
            #Calculating the angle.
            if self.position_x == p.position_x:
                angle = math.pi / 2
            else:
                angle = math.atan((self.position_y-p.position_y)/(self.position_x-p.position_x))

            #Calculating the x and y components.
            force_x = force_magnitude * abs(math.cos(angle))
            force_y = force_magnitude * abs(math.sin(angle))

            #Calculating how the relative position affects direction of force.
            if self.position_x < p.position_x:
                force_x *= -1
            if self.position_y < p.position_y:
                force_y *= -1

            net_force_x += force_x
            net_force_y += force_y

            if do_gravity:
                gravity_magnitude = gravity_coefficient * (self.mass * p.mass) / distance_squared

                #Calculating the x and y components.
                force_x = gravity_magnitude * abs(math.cos(angle))
                force_y = gravity_magnitude * abs(math.sin(angle))

                #Calculating how the relative position affects direction of force.
                if self.position_x > p.position_x:
                    force_x *= -1
                if self.position_y > p.position_y:
                    force_y *= -1

                net_force_x += force_x
                net_force_y += force_y


        #Setting force to new value.
        self.force_x = net_force_x
        self.force_y = net_force_y


    #Calculates the acceleration based on forces.
    def accelerate(self, time):
        self.velocity_x += (self.force_x / self.mass) * time
        self.velocity_y += (self.force_y / self.mass) * time


    #Calculates where the particle would move given no obstacles.
    def potential_move(self, time):
        self.potential_new_position_x = self.position_x + self.velocity_x * time
        self.potential_new_position_y = self.position_y + self.velocity_y * time


    #Determines what the particle is colliding with and returns the changes in velocity that would result from it.
    def collide(self, particles):

        did_collide = False #Keeps track of whether the particle collided with another.

        for p in particles: #Resetting each particle's effects from collision.
            p.collision_change_x = 0
            p.collision_change_y = 0

        for p in particles:
            if p is self: #Particle does not collide with itself.
                continue

            #Calculating distance of the particle from the other.
            new_distance = math.sqrt((self.potential_new_position_x-p.potential_new_position_x)**2 + (self.potential_new_position_y-p.potential_new_position_y)**2)
            
            #If the distance is close enough to be a collision, calculate the rate of change of distance (how direct the collision is).
            if new_distance < (self.radius + p.radius):
                rate_of_change_of_distance = ((self.position_x - p.position_x)*(self.velocity_x - p.velocity_x) + (self.position_y - p.position_y)*(self.velocity_y - p.velocity_y)) / math.sqrt((self.position_x-p.position_x)**2 + (self.position_y-p.position_y)**2)
                did_collide = True #Particle did collide. This is remembered.
            else: #Particle does not collide with this one, check the next one.
                continue

            #Calculating the angle of collision.
            if self.position_x == p.position_x:
                angle = math.pi / 2
            else:
                angle = math.atan((self.position_y-p.position_y)/(self.position_x-p.position_x))

            #x and y components of the rate of change of distance.
            x_component = rate_of_change_of_distance * abs(math.cos(angle))
            y_component = rate_of_change_of_distance * abs(math.sin(angle))

            #Since only relative values are taken, the other particles velocity is considered 0. Calculating for both this particle and the one it hits.
            x = x_component * (2*p.mass)/(self.mass+p.mass)
            y = y_component * (2*p.mass)/(self.mass+p.mass)
            px = -x_component * (2*self.mass)/(self.mass+p.mass)
            py = -y_component * (2*self.mass)/(self.mass+p.mass)

            #Determining the direction of collision. Particles keep track of the changes from collision.
            if self.position_x < p.position_x:
                self.collision_change_x += x #These values keep track of the total collision results for later.
                p.collision_change_x += px
            else:
                self.collision_change_x -= x
                p.collision_change_x -= px

            if self.position_y < p.position_y:
                self.collision_change_y += y
                p.collision_change_y += py
            else:
                self.collision_change_y -= y
                p.collision_change_y -= py

            #Whether or not a collision occcured.
            return did_collide


    #Moves the particle.
    def move(self):
        #If there was no collision, move the particle.
        if self.collision_change_x == 0 and self.collision_change_y == 0:
            self.position_x = self.potential_new_position_x
            self.position_y = self.potential_new_position_y

            #If screenbound, bounce off of edges.
            if screen_bound:
                if self.position_x + self.radius > width or self.position_x - self.radius < 0:
                    self.velocity_x *= -1
                if self.position_y + self.radius > height or self.position_y - self.radius < 0:
                    self.velocity_y *= -1

        #If there was a collision, add the results to the velocity.
        else:
            self.velocity_x += self.collision_change_x
            self.velocity_y += self.collision_change_y

    

class Player_particle(Particle):
    def __init__(self, mass, radius, charge, position_x, position_y, velocity_x, velocity_y, color, angle):
        Particle.__init__(self, mass, radius, charge, position_x, position_y, velocity_x, velocity_y, color)

        self.angle = angle

    def rotate(self, rotation):
        self.angle = (self.angle + rotation) % (2*math.pi)

    def apply_force(self, force):

        if self.angle > math.pi/2 and self.angle < 3*math.pi/2:
            self.velocity_x -= abs(math.cos(self.angle)) * force / self.mass
        else:
            self.velocity_x += abs(math.cos(self.angle)) * force / self.mass
        if self.angle > math.pi and self.angle < 2*math.pi:
            self.velocity_y -= abs(math.sin(self.angle)) * force / self.mass
        else:
            self.velocity_y += abs(math.sin(self.angle)) * force / self.mass

    #Draws the particle to the screen.
    def draw(self, offset_x=0, offset_y=0, color=None):
        if color==None:
            color=self.color

        if self.angle > math.pi/2 and self.angle < 3*math.pi/2:
            offset_x2 = -abs(math.cos(self.angle)) * self.radius
        else:
            offset_x2 = abs(math.cos(self.angle)) * self.radius
        if self.angle > math.pi and self.angle < 2*math.pi:
            offset_y2 = -abs(math.sin(self.angle)) * self.radius
        else:
            offset_y2 = abs(math.sin(self.angle)) * self.radius

        pygame.draw.circle(screen, color, (self.position_x-offset_x, self.position_y-offset_y), self.radius)
        pygame.draw.circle(screen, white, (self.position_x-offset_x-offset_x2, self.position_y-offset_y-offset_y2), self.radius)

    
# Used for the camera. May be overridden for other behaviors if desired.
def offset_x():
    return 0
def offset_y():
    return 0

#Random grid of positive (red), neutral (yellow), and negative (blue) particles.
'''
screen_bound = True
particles = []

for i in range(10):
    for j in range(10):
        n = random.randrange(0,1702)
        n2 = random.randrange(0,3)
        vx = random.randint(-6,8)
        vy = random.randint(-6,8)

        x=i*(1707/10)+20
        y=j*(960/10)+20

        if n2 == 2:
            particles.append(Particle(10, 10, 0, x, y, vx, vy, yellow))
        elif i*(1707/10+20) > n:
            particles.append(Particle(10, 10, 1500, x, y, vx, vy, red))
        elif i*(1707/10+20) < n:
            particles.append(Particle(10, 10, -500, x, y, vx, vy, blue))
        else:
            continue
        #'''

#Identical collision demo.
'''
particles = [Particle(5,15,0,100,480,10,0,yellow), Particle(5,15,0,1620,480,-10,0,yellow)]
#'''

#Full momentum transfer demo.
'''
screen_bound = True
particles = [Particle(5,15,0,100,480,50,0,yellow), Particle(5,15,0,860,480,0,0,yellow)]
#'''

#Grazed collision demo.
'''
screen_bound = True
particles = [Particle(5,10,0,500,480,10,0,yellow), Particle(5,10,0,860,499,0,0,yellow)]
#'''

#Oblique impact.
'''
screen_bound = True
radius = 20
particles = [Particle(5,radius,0,500,480,10,0,yellow), Particle(5,radius,0,860,480+radius,0,0,yellow)]
#'''

#Heavy into light.
'''
particles = [Particle(1000,10,0,800,480,10,0,yellow), Particle(10,10,0,900,480,0,0,yellow)]
screen_bound = True
#'''

#Light into heavy.
'''
particles = [Particle(1,10,0,100,480,50,0,yellow), Particle(50,10,0,860,480,0,0,yellow)]
screen_bound = True
#'''

#Newtons cradle.
'''
particles = [Particle(5,10,0,100,480,60,0,yellow), Particle(5,10,0,860,480,0,0,yellow),Particle(5,10,0,880,480,0,0,yellow),Particle(5,10,0,900,480,0,0,yellow),Particle(5,10,0,920,480,0,0,yellow),Particle(5,10,0,940,480,0,0,yellow)]
screen_bound = True
#'''

#4 Way collision.
'''
particles = [Particle(5,10,0,860,480,0,0,yellow),Particle(5,10,0,860,680,0,-20,yellow),Particle(5,10,0,860,280,0,20,yellow),Particle(5,10,0,1060,480,-20,0,yellow),Particle(5,10,0,660,480,20,0,yellow)]
particles2 = [Particle(5,10,0,1160,780,-10,-10,yellow),Particle(5,10,0,560,180,10,10,yellow),Particle(5,10,0,1160,180,-10,10,yellow),Particle(5,10,0,560,780,10,-10,yellow)]
for p in particles2:
    particles.append(p)
screen_bound = True
#'''


#Pool break.
'''
r = 15
particles = [Particle(10,r,0,100,480+random.randint(-4,4),random.randint(75,100),0,white)]
#particles = [Particle(10,r*.9,0,100,480,100,0,white)]
for i in range(5):
    x = 860+i*math.cos(math.pi/6)*2*r*1.1
    yi = 480-i*math.sin(math.pi/6)*2*r*1.1
    for j in range(i+1):
        y = yi + j*2*r*1.1
        particles.append(Particle(5,r,0,x,y,0,0,random.choice([red,yellow,green,blue,magenta,cyan])))
screen_bound = True
#'''


#"SPACE 1"
'''
particles = [ Particle(1000, 10, 0, 0, 0, 0, 0,yellow) , Particle(9, 4, 0, 360, 0, 0, 9, green), Particle(3, 2, 0, 374, 0, 0, 4, white)]

do_gravity = True
gravity_coefficient = 30

#Additional: Planets
particles2 = [Particle(4, 3, 0, 30, 0, 0, 30, red), Particle(9, 4, 0, 200, 0, 0, 11, magenta)]#, Particle(1, 2, 0, 700, 0, -3, 3, cyan),Particle(1, 2, 0, 721, 5, -1, 3, cyan),Particle(1, 2, 0, 660, -5, -3, 2, cyan),Particle(1, 2, 0, 712, 12, -4, 3, cyan)]
for i in particles2:
    particles.append(i)

def offset_x():
    return particles[0].position_x - width/2
def offset_y():
    return particles[0].position_y - height/2
#'''


#"SPACE 2 : Binary star."
'''
particles = [ Particle(3000, 10, 0, 0, 0, 0, -30,yellow), Particle(3000, 10, 0, 50, 0, 0, 30,yellow),Particle(4, 3, 0, 130, 0, 0, 40, red),Particle(9, 4, 0, 360, 0, 0, 25, green), Particle(3, 2, 0, 378, 0, 0, 29, white)]

# Optional Extra particles.
#particles.extend([Particle(1, 2, 0, 700, 0, -5, 15, cyan),Particle(1, 2, 0, 721, 5, -3, 9, cyan),Particle(1, 2, 0, 660, -5, -6, 8, cyan),Particle(1, 2, 0, 712, 12, -6, 10, cyan)])

do_gravity = True
gravity_coefficient = 30

def offset_x():
    return 0.5*(particles[0].position_x + particles[1].position_x)-width/2
def offset_y():
    return 0.5*(particles[0].position_y + particles[1].position_y)-height/2
    #'''


#"SPACE 1 with player."
'''
do_gravity = True
gravity_coefficient = 30
particles = [ Particle(3000, 10, 0, 0, 0, 0, -30,yellow), Particle(3000, 10, 0, 50, 0, 0, 30,yellow),Particle(4, 3, 0, 130, 0, 0, 40, red),Particle(9, 4, 0, 360, 0, 0, 25, green), Particle(3, 2, 0, 378, 0, 0, 29, white)]

#Additional: Planets
#particles2 = [Particle(4, 3, 0, 30, 0, 0, 30, red), Particle(9, 4, 0, 200, 0, 0, 11, magenta)]#, Particle(1, 2, 0, 700, 0, -3, 3, cyan),Particle(1, 2, 0, 721, 5, -1, 3, cyan),Particle(1, 2, 0, 660, -5, -3, 2, cyan),Particle(1, 2, 0, 712, 12, -4, 3, cyan)]
#for i in particles2:
#    particles.append(i)


def offset_x():
    return particles[-1].position_x - width/2
def offset_y():
    return particles[-1].position_y - height/2

player = Player_particle(3, 3, 0, 400, 500, 0, 0, cyan, 0)
particles.append(player)
#'''

#Each simulation involves, particles, perspective, bounds, and gravity settings.

time_pass = 0.001
time_step = 0.01
while True:
    time_current = time.time()
    #Managing the screen.
    screen.fill(black)
    
    cam_offset_x = offset_x()
    cam_offset_y = offset_y()

    pygame.event.get()
    keys = pygame.key.get_pressed() 

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
    
    if keys[pygame.K_d]:
        player.rotate(math.pi/100)
    if keys[pygame.K_a]:
        player.rotate(-math.pi/100)

    if keys[pygame.K_w]:
        player.apply_force(0.24)


    for p in particles:
        p.draw(cam_offset_x,cam_offset_y)

    #Applying forces to the particles.
    for p in particles:
        p.fields(particles)
    
    #Accelerated particles based on their forces.
    for p in particles:
        p.accelerate(time_step)


    # Determine where the particle is going to move. 
    # Look for collisions. Once a collision is found, calculate its effects.
    # After this, break the for loop. And start over again.
    # This enables complex collisions that don't destroy energy.
    i = 0
    continue_loop = True
    while continue_loop and i < 1000:
        i+=1

        for p in particles: #Check how each particle's velocity (momentum) changes based on previous colissions, and where this would move them.
            p.velocity_x += p.collision_change_x
            p.velocity_y += p.collision_change_y
            p.potential_move(time_step) 

        continue_loop = False
        for p in particles: #For each particle,
                did_collide = p.collide(particles) #Check what it collided with.
                if did_collide: #If there was a collision, reset the loop.
                    continue_loop = True
                    break

    for p in particles: #Check how each particle's velocity (momentum) changes based on previous colissions, and where this would move them.
            p.velocity_x += p.collision_change_x
            p.velocity_y += p.collision_change_y
            p.potential_move(time_step) 

    #Move each particle based on their velicity (which determined where they would move).
    for p in particles:
        p.move()

    #for p in particles:
     #   p.draw(main_particle.position_x-1720*0.5,main_particle.position_y-960*0.5, red)

    while time.time() - time_current < time_pass:
        continue
    
    pygame.display.flip()
    #time.sleep(0.0025)
    
    