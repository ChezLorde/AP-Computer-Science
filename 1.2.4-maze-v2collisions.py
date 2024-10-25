import turtle
import random
'''
Turtle Maze with collisions for walls: Takes the range that the maze_builder has travelled and saves it in a list. The player iterates over every range to see if it is contacting any of them.
By: Noah Seeno
1.2.4
'''

# ----------------------------------------------------------------------Configurations

# maze specifications
num_walls = 35
wall_gap = 30
num_walls_to_skip = 5
start_wall_length = 40

# maze cosmetics
wall_thickness = 2
wall_color = "black"

# generation 
build_speed = 0

# player controls
turn_amount = 90
forward_amount = 10
control_type = "g"     # wasd: w for forward, s for backward, a for left, d for right           g: wasd for directions, g to move forward

# player cosmetics
player_shape = "classic"
player_color = "red"

# wall detection
horizontalwalls = []
verticalwalls = []
wall_detect_dist = wall_thickness + 1
wall_bounciness = 2


# ----------------------------------------------------------------------Initialize Objects
maze_builder = turtle.Turtle()
maze_builder.pensize(wall_thickness)
maze_builder.pencolor(wall_color)
maze_builder.hideturtle()
maze_builder.speed(build_speed)

maze_runner = turtle.Turtle(shape=player_shape)
maze_runner.color(player_color)

window = turtle.Screen()

# ----------------------------------------------------------------------Function Setup
# Has the maze builder build walls that are saved for collision detection                                       <-----------------Collision Detection for saving walls
def forward_wall(distance):
  global horizontalwalls
  global verticalwalls
 
  # Only save the wall to be collided with if the pen is down (if it is shown)
  if maze_builder.isdown():
    # If facing left or right, save the range you travelled in x and your y position as a line segment.
    if (maze_builder.heading() == 0 or maze_builder.heading() == 180):
      y_value = int(maze_builder.ycor())  #Save the y-position
      start_x_value = int(maze_builder.xcor())  #Save the x-location of one end of the wall
      maze_builder.forward(distance)    #Build the wall
      end_x_value = int(maze_builder.xcor())  #Save the x-location of the other end of the wall
      
      # If you are travelling in the negative direction, switch the start and end values
      if start_x_value > end_x_value:
        end_x_value = start_x_value
        start_x_value = int(maze_builder.xcor())
      
      # Add the x range and y value to the horizontal list
      horizontalwalls.append([y_value, start_x_value, end_x_value])
      print("New Horiz Wall: " + "y: " + str(y_value) + " x: " + str(start_x_value) + " to " + str(end_x_value))
    
    # If facing up or down, save the range you travelled in y and your x position as a line segment.
    elif (maze_builder.heading() == 90 or maze_builder.heading() == 270):
      x_value = int(maze_builder.xcor())  #Save the x-position
      start_y_value = int(maze_builder.ycor())  #Save the y-location of one end of the wall
      maze_builder.forward(distance)  #Build the wall
      end_y_value = int(maze_builder.ycor())  #Save te y-location of the other end of the wall
      
      # If you are travelling in the negative direction, switch the start and end values
      if start_y_value > end_y_value:
        end_y_value = start_y_value
        start_y_value = int(maze_builder.ycor())
      
      # Add the y range and x value to the vertical list
      verticalwalls.append([x_value, start_y_value, end_y_value])
      print("New Vertical Wall: " + "x: " + str(x_value) + " y: " + str(start_y_value) + " to " + str(end_y_value))
    
    else:
      #Otherwise, just go forward, if you are going diagonally.
      maze_builder.forward(distance)

  # If the pen is up, do not save that as a wall.
  else:
    maze_builder.forward(distance)

# Has the player move forward, but accounts for walls                                                 <----------------Player Collision Detection
def forward_player(distance):

  #check_completion()
  
  # Go forward only 1 at a time
  for amount_gone in range(distance):

    touching_wall = False
    maze_runner.forward(1)
    
    # Go through all the vertical walls to see if you are colliding with them
    for rg in verticalwalls:
     
      wall_x = rg[0] 
      wall_y_start = rg[1]
      wall_y_end = rg[2]
     
     # If you are too close to the wall's x-value and are within the wall's y-range, you are touching it.
      if abs(wall_x - maze_runner.xcor()) < wall_detect_dist:
          if maze_runner.ycor() < wall_y_end and maze_runner.ycor() > wall_y_start:
            touching_wall = True
            break
    
    # Go through all the horizontal walls to see if you are colliding with them
    for rg in horizontalwalls:
       wall_y = rg[0]
       wall_x_start = rg[1]
       wall_x_end = rg[2]
       
       # If you are too close to the wall's y-value and are within the wall's x-range, you are touching it.
       if abs(wall_y - maze_runner.ycor()) < wall_detect_dist:
          if maze_runner.xcor() < wall_x_end and maze_runner.xcor() > wall_x_start:
            touching_wall = True
            break
    
    # If you are touching a wall, bouce backward.
    if touching_wall:
      maze_runner.backward(wall_bounciness)
      break

# Creates an opening in the maze
def build_opening(length):
  if maze_builder.isdown():
    maze_builder.penup()
    maze_builder.forward(length)
    maze_builder.pendown()
  else:
    maze_builder.forward(length)

# Creates a barrier in the maze
def build_barrier(length):
  maze_builder.right(90)
  forward_wall(length)
  maze_builder.backward(length)
  maze_builder.left(90)

def build_maze():
  index = 0
  length = start_wall_length

  maze_builder.clear()
  maze_builder.penup()
  maze_builder.goto(wall_gap, wall_gap)
  maze_builder.pendown()

  for index in range(num_walls):

    maze_builder.right(90)
      
    # Remove the first few walls so they don't mess up.
    if index < num_walls_to_skip:
      maze_builder.penup()
      opening_dist_from_edge = 10
      barrier_dist_from_edge = 20
    else:
      maze_builder.pendown()
      opening_dist_from_edge = random.randint(wall_gap * 2, length - wall_gap * 2)
      barrier_dist_from_edge = random.randint(wall_gap * 2, length - wall_gap * 2)

      # Make sure openings and barriers do not overlap
      while (barrier_dist_from_edge > opening_dist_from_edge and barrier_dist_from_edge < (opening_dist_from_edge - wall_gap)):
        barrier_dist_from_edge = random.randint(wall_gap * 2, length - wall_gap * 2)

    # -------------------------------If the barrier comes first:
    if barrier_dist_from_edge < opening_dist_from_edge:
      #Do the wall 
      forward_wall(barrier_dist_from_edge)

      #Build the Barrier
      build_barrier(wall_gap)

      #Go to the opening
      forward_wall(opening_dist_from_edge - barrier_dist_from_edge)

      #Do the Opening
      build_opening(wall_gap)
      
      #Finish the wall
      forward_wall(length - opening_dist_from_edge)

    # --------------------------------------If the opening comes first:
    elif barrier_dist_from_edge >= opening_dist_from_edge:
      #Go to the opening 
      forward_wall(opening_dist_from_edge)

      #Do the Opening
      build_opening(wall_gap)

      #Go to the barrier
      forward_wall(barrier_dist_from_edge - opening_dist_from_edge)

      #Build the Barrier
      build_barrier(wall_gap)
      
      #Finish the wall
      forward_wall(length - barrier_dist_from_edge)

    # Change the size of the wall at corners so the maze spirals outward
    if index % 2 == 0:
      length += wall_gap
    if length <= wall_gap:
      break

# PLAYER CONTROLS
def left():
  if control_type == "g":
    maze_runner.setheading(180)
  else:
    maze_runner.left(turn_amount)

def right():
  if control_type == "g":
    maze_runner.setheading(0)
  else:
    maze_runner.right(turn_amount)

def forward():
  if control_type == "g":
    maze_runner.setheading(90)
  else:
    forward_player(forward_amount)

def reverse():
  if control_type == "g":
    maze_runner.setheading(270)
  else:
    maze_runner.right(180)
    forward_player(forward_amount)
    maze_runner.right(180)

def gforward():
  if control_type == "g":
    forward_player(forward_amount)

# ----------------------------------------------------------------------Events and Function Calls
build_maze()
print(horizontalwalls)
print(verticalwalls)

window.onkeypress(left, "a")
window.onkeypress(right, "d")
window.onkeypress(forward, "w")
window.onkeypress(reverse, "s")
window.onkeypress(gforward, "g")

window.listen()
window.mainloop()