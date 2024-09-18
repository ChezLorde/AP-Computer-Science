import turtle as trtl

def append_pop():
  flooring = ["hardwood", "tile", "laminate"]
  print(flooring)
  flooring.append("carpet")
  print(flooring)
  flooring.pop()
  print(flooring)

def traversing_turtles():
  #   a117_traversing_turtles.py
  #   Add code to make turtles move in a circle and change colors.

  # create an empty list of turtles
  my_turtles = []

  # use interesting shapes and colors
  turtle_shapes = ["arrow", "turtle", "circle", "square", "triangle", "classic", "arrow", "turtle", "circle", "square", "triangle", "classic", "arrow", "turtle", "circle", "square", "triangle", "classic", "arrow", "turtle", "circle", "square", "triangle", "classic"]
  turtle_colors = ["red", "blue", "green", "orange", "purple", "gold", "red", "blue", "green", "orange", "purple", "gold", "red", "blue", "green", "orange", "purple", "gold", "red", "blue", "green", "orange", "purple", "gold"]

  ''' # clone the lists so they repeat
  for s in range(2):
    new_shapes = turtle_shapes
    for item in new_shapes:
      turtle_shapes.append(item)
  
  for s in range(2):
    new_colors = turtle_colors
    for item in new_colors:
      turtle_colors.append(item)

  print(turtle_shapes)
  print(turtle_colors)'''
 # The list of shapes did not create a turtle for the missing shape, but still ran the program.

  for s in turtle_shapes:
    t = trtl.Turtle(shape=s)
    my_turtles.append(t)
    t.penup()
    color = turtle_colors.pop()
    t.pencolor(color)
    t.color(color)
    

  # set where the turtles begin 
  startx = 0
  starty = 0
  startheading = 90
  addifier = 1

  # send out each turtle
  for t in my_turtles:
    t.goto(startx, starty)
    t.setheading(startheading)
    t.pendown()
    t.right(45)     
    t.forward(50)

  #	move the starting position of the next turtle
    startx = t.xcor() 
    starty = t.ycor()
    startheading = t.heading() + addifier
    addifier += 1

traversing_turtles()

wn = trtl.Screen()
wn.mainloop()