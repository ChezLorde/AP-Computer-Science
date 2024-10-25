import turtle
import random
import time

# ----------------------------------------------------------------------Configurations

# maze specifications
num_walls = 10
wall_gap = 30
num_walls_to_skip = 6
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
walls = []

# stopwatch
start_time = 60


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
# Has the maze builder build walls that are saved for collision detection
def forward_wall(distance):
  global walls
  amount_travelled = 0
  while amount_travelled < distance:
    amount_travelled += 1
    maze_builder.forward(1)
    walls.append([int(maze_builder.xcor()), int(maze_builder.ycor())])

# Has the player move forward, but accounts for walls
def forward_player(distance):
  global walls
  amount_travelled = 0
  maze_runner.goto(int(maze_runner.xcor()), int(maze_runner.ycor()))
  orig_x = maze_runner.xcor()
  orig_y = maze_runner.ycor()
  on_point = False
  while amount_travelled < distance:
    if distance < 0:
      maze_runner.backward(1)
    else:
      maze_runner.forward(1)
    for point in walls:
      if maze_runner.xcor() == point[0] and maze_runner.ycor() == point[1]:
        maze_runner.goto(orig_x, orig_y)
        on_point = True
        break
    if on_point:
      maze_runner.backward(1)
      break
    else:
      amount_travelled += 1

# Creates an opening in the maze
def build_opening(length):
  if maze_builder.pen(pendown=False):
    maze_builder.forward(length)
  else:
    maze_builder.penup()
    maze_builder.forward(length)
    maze_builder.pendown()

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
print(walls)

window.onkeypress(left, "a")
window.onkeypress(right, "d")
window.onkeypress(forward, "w")
window.onkeypress(reverse, "s")
window.onkeypress(gforward, "g")

window.listen()
window.mainloop()