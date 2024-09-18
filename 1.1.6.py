#   a116_buggy_image.py
import turtle as trtl

painter = trtl.Turtle()

def draw_spider():
  # create the spider's body
  painter.pensize(40)
  painter.circle(20)

  # configure spider legs
  num_legs = 8
  leg_length = 70
  leg_angle = 180 / num_legs
  leg_extent = 180
  leg_min = 140
  painter.pensize(5)
  leg_number = 0

  # draw spider legs
  while (leg_number < num_legs):
    painter.penup()
    painter.goto(0,20)
    painter.pendown()

    #Determine which side
    if (leg_number < (num_legs / 2)):
      painter.setheading(leg_angle*leg_number - 135)
      leg_extent = -1 * (180 - (leg_number % (num_legs / 2)) * 10)
    else:
      painter.setheading(leg_angle*leg_number + 45)
      leg_extent = (leg_min) + ((leg_number % (num_legs / 2)) * 10)

    #Draw the legs
    painter.circle(leg_length, leg_extent)

    leg_number = leg_number + 1
    
  # configure spider eyes
  num_eyes = 2
  eye_angle = 90 / num_eyes
  eye_number = 0

  painter.shape("circle")
  painter.color("white")
  painter.turtlesize(0.5)
  painter.penup()

  # draw spider eyes
  while (eye_number < num_eyes):
    painter.goto(0,20)
    painter.setheading(eye_angle*eye_number - 90)
    painter.forward(20)
    painter.stamp()
    eye_number = eye_number + 1

def draw_ladybug():
  # draw head
  painter.pensize(40)
  painter.circle(5)

  # configure legs
  num_legs = 6
  leg_length = 50
  leg_angle = 180 / num_legs
  painter.pensize(5)
  leg_number = 0

  # draw ladybug legs
  while (leg_number < num_legs):
    painter.goto(0,-35)
    if (leg_number < (num_legs / 2)):
      painter.setheading(leg_angle*leg_number - 45)
    else:
      painter.setheading(leg_angle*leg_number + 65)
    painter.forward(leg_length)
    leg_number = leg_number + 1

  painter.setheading(0)

  # and body
  painter.penup()
  painter.goto(0, -55) 
  painter.color("red")
  painter.pendown()
  painter.pensize(40)
  painter.circle(20)
  painter.setheading(270)
  painter.color("black")
  painter.penup()
  painter.goto(0, 5)
  painter.pensize(2)
  painter.pendown()
  painter.forward(75)

  # config dots
  num_dots = 2
  xpos = -20
  ypos = -55
  painter.pensize(10)

  # draw two sets of dots
  for dot in range(num_dots):
    painter.penup()
    painter.goto(xpos, ypos)
    painter.pendown()
    painter.circle(3)
    painter.penup()
    painter.goto(xpos + 30, ypos + 20)
    painter.pendown()
    painter.circle(2)

    # position next dots
    ypos = ypos + 25
    xpos = xpos + 5

def spiral():
  painter.speed(0)
  for heading in range(0, 360, 10):
    painter.setheading(heading)
    painter.circle(100, heading / 2)
    painter.penup()
    painter.goto(0, 0)
    painter.pendown()

draw_spider()
#spiral()

painter.hideturtle()

wn = trtl.Screen()
wn.mainloop()