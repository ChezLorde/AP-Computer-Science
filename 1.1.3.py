import turtle 

painter = turtle.Turtle()



#Make a square function
def square(sideLength):
  for i in range(4):
    painter.forward(sideLength)
    painter.right(90)

#Make an octagon function
def octagon(sideLength):
  for i in range(8):
    painter.forward(sideLength)
    painter.right(45)

#Make a circle of circles function
def circleCircle():
  for i in range(18):
    painter.shape("circle")
    painter.forward(20)
    painter.right(20)
    painter.stamp()

#Draw a flower
def flower(petalNumber, size):
  # stem
  painter.color("green")
  painter.pensize(15)
  painter.goto(0, -150)
  painter.setheading(90)
  painter.forward(100)
  #  leaf
  painter.setheading(270)
  painter.circle(20, 120, 20)
  painter.setheading(90)
  painter.goto(0, -60)
  # rest of stem
  painter.forward(60)
  painter.setheading(0)

  # change pen
  painter.penup()
  painter.shape("circle")
  painter.turtlesize(size)

  # draw flower
  painter.color("darkorchid")
  painter.goto(20,180)

  petalColorsOperator = 0

  for petal in range(petalNumber):
    petalColors = [["darkorchid", "blue"], ["teal", "green"], ["yellow", "orange"], ["firebrick", "red"]]
    painter.right(360 / petalNumber)
    painter.forward(30 / (petalNumber / 18))
    altRem = petal % 2
    swtRem = petal % 4
    if swtRem == 0:
      petalColorsOperator = petalColorsOperator + 1
      colorSet = petalColors[petalColorsOperator]
    if petalColorsOperator > 2:
      petalColorsOperator = 0
    if altRem == 0:
      painter.color(colorSet[1])
    else:
      painter.color(colorSet[0])
    painter.stamp()

# ring 2 of flower
''' painter.goto(20,160)
painter.color("blue")
newPetalNumber = int((2/3) * petalNumber)

for petal in range(newPetalNumber):
  painter.right(360 / newPetalNumber)
  painter.forward(20 / (newPetalNumber / 18))
  painter.stamp()'''

def moduloTest():
  for count in range(10):
    rem = count % 4
    print(rem)
    if (rem == 0):
      print("The number ", count, " with rem ", rem, " is even.")
    if (rem == 1):
      print("The number ", count, " with rem ", rem, " is odd.")

def tower(x, y, floors):
  #set tower base y
  ogy = y
  #set floor colors
  floorColors = [["gray", "blue", "steelblue"], ["teal", "green", "mediumspringgreen"], ["red", "purple", "fuchsia"]]
  #set color set used in that building
  towerColors = floorColors[0]
  fcoloroperator = 0
  color = "black"

  #set painter settings
  painter.speed(0)
  painter.pensize(5)

  #build the towers
  for floor in range(floors):
    print(floor % 21)
    color = towerColors[0]
    painter.penup()
    painter.goto(x, y)
    #print(floor % 6)

    #Change colors for each set of 3 floors
    if floor % 9 > 2:
      color = towerColors[1]
    if floor % 9 > 5:
      color = towerColors[2]
    painter.color(color)

    #set height of next floor
    y = y + 5

    #Build new tower if over 21 floors
    if floor % 21 == 20 and floor > 5:
      x = x + 100
      y = ogy
      fcoloroperator = fcoloroperator + 1
      towerColors = floorColors[fcoloroperator % 3]

    painter.pendown()
    painter.forward(50)

#circleCircle()
#flower(18, 2)
#octagon(100)
#moduloTest()
tower(-150, -150, 500)

window = turtle.Screen()
window.mainloop()