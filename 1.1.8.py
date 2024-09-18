#   a118_turtles_in_traffic.py
#   Move turtles horizontally and vertically across screen.
#   Stopping turtles when they collide.
import turtle as trtl
import math
import random

# grades program
def grades():
  my_courses = ["English", "Math", "CS"]
  redo = "y"

  while (redo == "y"):

    for course in my_courses:
      print() # blank line
      print("Enter your points for " + course)

      points = int(input("Points -> "))

      if (points >= 90):
        print("A")
      elif (points >= 80):
        print("B")
      elif (points >= 70):
        print("C")
      elif (points >= 60):
        print("D")
      else:
        print("F")

    redo = input("Do you need to re-do these grades? (y/n)")

# set up window
wn = trtl.Screen()
    
# create two empty lists of turtles, adding to them later
horiz_turtles = []
vert_turtles = []
turtles = []

# use interesting shapes and colors
turtle_shapes = ["arrow", "turtle", "circle", "triangle", "classic"]
horiz_colors = ["blue", "green", "orange", "purple", "gold"]
vert_colors = ["darkblue", "lime", "salmon", "indigo", "brown"]

# set up speeds for turtles
horiz_speeds = []
vert_speeds = []
horiz_max_speeds = []
vert_max_speeds = []

for i in range(len(turtle_shapes)):
  hor_speed = random.randint(1, 30)
  ver_speed = random.randint(1, 30)
  hor_max = hor_speed + random.randint(5, 10)
  ver_max = ver_speed + random.randint(5, 10)

  horiz_speeds.append(hor_speed)
  vert_speeds.append(ver_speed)
  horiz_max_speeds.append(hor_max)
  vert_max_speeds.append(ver_max)


# starting position for turtle destinations
tloc = 50

# create the horizontal and vertical turtles in rows horizontally and vertically
for s in turtle_shapes:

  # create horizontal turtles
  ht = trtl.Turtle(shape=s)
  horiz_turtles.append(ht)
  ht.penup()
  new_color = horiz_colors.pop()
  ht.fillcolor(new_color)
  ht.goto(-350, tloc)
  ht.setheading(0)
  ht.speed(0)

  # create vertical turtles
  vt = trtl.Turtle(shape=s)
  vert_turtles.append(vt)
  vt.penup()
  new_color = vert_colors.pop()
  vt.fillcolor(new_color)
  vt.goto( -tloc, 350)
  vt.setheading(270)
  vt.speed(0)

  turtles.append(vt)
  turtles.append(ht)
  
  

  # change the position of the next turtle
  tloc += 50

# TODO: move turtles across and down screen, stopping for collisions
  
# function for colliding turtles
def collide(turtle):
  # set to collision color
  turtle.shape("square")
  turtle.color("red")

  #set the turtle back
  turtle.back(random.randint(5, 40))

  if turtle.heading() == 270:
    i = vert_turtles.index(turtle)
    vert_speeds.remove(vert_speeds[i])
    vert_speeds.insert(i, 0)
  else: 
    i = horiz_turtles.index(turtle)
    horiz_speeds.remove(horiz_speeds[i])
    horiz_speeds.insert(i, 0)
  
# function for deactivating turtles
def deactivate(turtle):

  turtle.fillcolor("gray")

  if turtle in horiz_turtles:
    horiz_turtles.remove(turtle)
  elif turtle in vert_turtles:
    vert_turtles.remove(turtle)
  



for step in range(50):
	
  # move the horizontal turtles ---------------------------------------------------------------------------------------------------------------------HORIZONTAL
  for hor_turtle in horiz_turtles:

    # Get the speed from the list
    i = horiz_turtles.index(hor_turtle)
    speed = horiz_speeds[i]

    # move the turtle forward
    hor_turtle.forward(speed)

    # reset turtle shape/colors when they are back from a collision (get from starting list)
    if hor_turtle.shape() == "square" and (speed > 2):

      # set new colors and shapes for after collisions
      old_turtle_shapes = ["arrow", "turtle", "circle", "triangle", "classic"]
      old_horiz_colors = ["blue", "green", "orange", "purple", "gold"]

      j = horiz_turtles.index(hor_turtle)
      print(i)
      old_color = old_horiz_colors[j]
      old_shape = old_turtle_shapes[j]

      hor_turtle.shape(old_shape)
      hor_turtle.fillcolor(old_color)
      hor_turtle.pencolor("black")

    # set up a new speed, and reset it if it is greater than max
    newSpeed = speed + 1
    if newSpeed > horiz_max_speeds[i]:
      newSpeed = random.randint(1, 15)
      
    # change speed to new speed
    horiz_speeds.remove(speed)
    horiz_speeds.insert(i, newSpeed)

    # check for collisions, if so remove from list so they no longer move
    for ver_turtle in vert_turtles:

      # pythagorean theorem to get distance
      distx = abs(ver_turtle.ycor() - hor_turtle.ycor())
      disty = abs(ver_turtle.xcor() - hor_turtle.xcor())
      dist = math.sqrt((distx * distx) + (disty * disty))

      win_edge = ((wn.window_width() / 2) - 50)

      # remove if they go too close to edge of screen
      if hor_turtle.xcor() > win_edge and hor_turtle in horiz_turtles:
        hor_turtle.goto(win_edge, hor_turtle.ycor())
        deactivate(hor_turtle)
        
        
      # delete if too close to another turtle
      elif dist < 20:
        if ver_turtle in vert_turtles:
          collide(ver_turtle)
        collide(hor_turtle)
      

  # move the vertical turtles  --------------------------------------------------------------------------------------------------------VERTICAL
  for ver_turtle in vert_turtles:

    # Get the speed from the list
    i = vert_turtles.index(ver_turtle)
    speed = vert_speeds[i]

    # move the turtle forward
    ver_turtle.forward(speed)

    # reset turtle shape/colors when they are back from a collision (get from starting list)
    if ver_turtle.shape() == "square" and (speed > 2):

      # set new colors and shapes for after collisions
      old_turtle_shapes = ["arrow", "turtle", "circle", "triangle", "classic"]
      old_vert_colors = ["darkblue", "lime", "salmon", "indigo", "brown"]

      j = vert_turtles.index(ver_turtle)
      print(i)
      old_color = old_vert_colors[j]
      old_shape = old_turtle_shapes[j]

      ver_turtle.shape(old_shape)
      ver_turtle.fillcolor(old_color)
      ver_turtle.pencolor("black")

    # set up a new speed, and reset it if it is greater than max
    newSpeed = speed + 1
    if newSpeed > vert_max_speeds[i]:
      newSpeed = random.randint(1, 15)
      
    # change speed to new speed
    vert_speeds.remove(speed)
    vert_speeds.insert(i, newSpeed)

    # check for collisions
    for hor_turtle in horiz_turtles:

      distx = abs(ver_turtle.ycor() - hor_turtle.ycor())
      disty = abs(ver_turtle.xcor() - hor_turtle.xcor())
      dist = math.sqrt((distx * distx) + (disty * disty))

      win_edge = (-1 * (wn.window_height() / 2) + 50)

      # delete if they reach the edge of the screen
      if ver_turtle.ycor() < win_edge and ver_turtle in vert_turtles:
        ver_turtle.goto(ver_turtle.xcor(), win_edge)
        deactivate(ver_turtle)

      # delete if too close to another turtle
      elif dist < 20:
        collide(ver_turtle)
        if hor_turtle in horiz_turtles: 
          collide(hor_turtle)

# deactivate all the turtles
for turtle in turtles:
  deactivate(turtle)


wn.mainloop()





  
