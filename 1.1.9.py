import turtle
import math
import random

painter = turtle.Turtle()
window = turtle.Screen()

wn_height_range = [-1 * (window.window_height() / 2), (window.window_height() / 2)]
wn_width_range = [-1 * (window.window_width() / 2), (window.window_width() / 2)]

margin = 50
max_height = 150
min_height  = 50
max_width = 75
min_width = 20
max_sides = 16
min_sides = 4

border_colors = ["blue", "darkslategrey", "lightslategrey", "darkblue", "navy", "darkgreen", "seagreen", "darkviolet", "black"]
fill_colors = ["palegreen", "paleturquoise", "aliceblue", "royalblue", "skyblue", "violet", "plum", "orange"]

num_crystals = int(input("Please input the number of crystals: "))

if num_crystals == 42:
  border_colors = ["black"]
  fill_colors = ["red"]
  max_height = 50
  min_height = 50
  max_width = 50
  min_width = 50
  max_sides = 4
  min_sides = 4

for crystal in range(num_crystals):

  # randomize the height, width and sides of the crystal
  height = random.randint(min_height, max_height)
  width = random.randint(min_width, max_width)
  sides = 2 * random.randint(min_sides / 2, max_sides / 2)
  width_mod = math.sqrt(sides)

  # set the location within an acceptable range, not offscreen
  locx = random.randint(wn_width_range[0] + (margin + int(width / 2)), wn_width_range[1] - (margin + int(width / 2)))
  locy = random.randint(wn_height_range[0] + margin, wn_height_range[1] - (margin + height))

  # set colors of turtle
  painter.pencolor(border_colors[crystal % len(border_colors)])
  painter.fillcolor(fill_colors[crystal % len(fill_colors)])

  if crystal % 20 == 19:
    painter.fillcolor("red")

  # go to the chosen location
  painter.penup()
  painter.goto(locx, locy)
  painter.pendown()
  painter.begin_fill()

  # draw the crystal - bottom left sides
  print("bottom left")
  for point_num in range(int(sides / 4)):

      left_edge = -1 * (width / 2)
      left_units = left_edge / (sides / 4)
      height_units = height / (sides / 2)

      x = locx + left_units * width_mod * math.sqrt(point_num)
      y = locy + point_num * height_units

      print("going to: ", x, ", ", y)
      painter.goto(x, y)
      

  # top left sides
  print("top left")
  for point_num in range(int(sides / 4), 0, -1):

      left_edge = -1 * (width / 2)
      left_units = left_edge / (sides / 4)
      height_units = height / (sides / 2)

      x = locx + left_units * width_mod * math.sqrt(point_num)
      y = locy + (height - (point_num * height_units))

      print("going to: ", x, ", ", y)
      painter.goto(x, y)
      

  #reset to bottom
  painter.goto(locx, locy + height)
  painter.penup()
  painter.goto(locx, locy)
  painter.pendown()

  #Bottom right
  print("bottom right")
  for point_num in range(int(sides / 4)):

      left_edge = (width / 2)
      left_units = left_edge / (sides / 4)
      height_units = height / (sides / 2)

      x = locx + left_units * width_mod * math.sqrt(point_num)
      y = locy + point_num * height_units

      print("going to: ", x, ", ", y)
      painter.goto(x, y)
      

  # top right sides
  print("top right")
  for point_num in range(int(sides / 4), 0, -1):

      left_edge = (width / 2)
      left_units = left_edge / (sides / 4)
      height_units = height / (sides / 2)

      x = locx + left_units * width_mod * math.sqrt(point_num)
      y = locy + (height - (point_num * height_units))

      print("going to: ", x, ", ", y)
      painter.goto(x, y)
      
  painter.goto(locx, locy + height)
  painter.end_fill()


window.mainloop()

