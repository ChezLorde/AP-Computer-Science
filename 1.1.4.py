import turtle
import random

painter = turtle.Turtle()
window = turtle.Screen()

def a114_nested_loops_2(color1, color2, height):
  painter.speed(0)
  answer = "y"
  while (answer == "y"):
    window.clearscreen()  
    painter.goto(0,0)
    space = 1

    angle = int(input("angle:"))
    seg = int(360/angle)

    while painter.ycor() < height:
      if space % 200 == 100:
          painter.fillcolor(color1)
          painter.color(color1)
      elif space % 100 == 0:
          painter.fillcolor(color2)
          painter.color(color2)
      painter.right(angle)
      painter.forward(2 * space + 10) # experiment
      painter.begin_fill()
      painter.circle(3)
      painter.end_fill()
      space = space + 1

    answer = input("again?")

  window.bye()

def a114_nested_loops_4():
  painter.speed(0)
  painter.penup()
  painter.goto(-200, 0)
  painter.pendown()

  colors = ["red", "orange", "yellow", "green", "blue", "purple", "black"]
  prevcolor = "black"
  x = -200
  y = 0
  move_x = 1
  move_y = 1
  
  while True:

    print(painter.pencolor())
    print(prevcolor)

    #Choose random color for each round
    while painter.pencolor() == prevcolor:
      painter.pencolor(colors[random.randint(0, 6)])

    prevcolor = painter.pencolor()

    #Do the upper chevrons
    painter.penup()
    x = -200
    y = 0
    painter.goto(x, y)
    painter.pendown()
    while (x < 100):

      while (y < 100):
        x = x + move_x
        y = y + move_y
        painter.goto(x,y)
      move_y = -1
      
      while (y > 0):
        x = x + move_x
        y = y + move_y
        painter.goto(x,y)
      move_y = 1

    #Set painter back to the start
    painter.penup()
    x = -200
    y = 0
    painter.goto(x, y)
    painter.pendown()

    #Do the lower chevrons
    while (x < 100):

      while (y > -100):
        x = x + move_x
        y = y - move_y
        
        painter.goto(x,y)
      
      move_y = -1
      
      while (y < 0):
        x = x + move_x
        y = y - move_y
        painter.goto(x,y)
      move_y = 1


def a114_whileguess(color1, color2):
  painter.speed(0)
  painter.color(color1)

  height = window.canvheight
  space = 1
  angle = 65 # experiment with the shape
  seg = int(360/angle)

  while (painter.ycor() < height):
    if (space % 12 < 6):
      painter.fillcolor(color1)
      painter.color(color1)
    elif (space % 12 > 6):
      painter.fillcolor(color2)
      painter.color(color2)

    painter.right(angle)
    painter.forward(2*space + 3) # experiment
    painter.begin_fill()
    painter.circle(3)
    painter.end_fill()
    space += 1

def a114_divisible():
  #Get 2 numbers from user
  num1 = int(input("Choose a number: "))
  num2 = int(input("Choose a number: "))

  #Loop while the numbers are not divisible (remainder is not 0)
  while num1 % num2 != 0:

    #Inform the user of the result
    print(num1, " and ", num2, " are not divisible. The remainder is ", num1 % num2)

    #Gather user input again
    num1 = int(input("Choose a number: "))
    num2 = int(input("Choose a number: "))

  #Inform user of result
  print("Congragulations! ", num1, " and ", num2, "are divisible.")

a114_whileguess("red", "orange")


window.mainloop()