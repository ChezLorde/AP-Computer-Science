import turtle as ttl
import random

painter = ttl.Turtle()

def CreateTile(posx, posy, tiletype, color):

  painter.penup()
  painter.pencolor("black")
  painter.goto(posx, posy)
  painter.pendown()
  painter.fillcolor("white")

  if tiletype == "water":
   painter.fillcolor("blue")
  if tiletype == "field" or tiletype == "house":
    painter.fillcolor("green")
  if tiletype == "castle":
    painter.fillcolor("gray")

  painter.begin_fill()

  for i in range(4):
   painter.forward(100)
   painter.right(90)

  painter.end_fill()
  painter.penup()

  if tiletype == "house":
    painter.goto(posx + random.randint(0, 100-15), posy - random.randint(15, 100))
    painter.pendown()
    painter.fillcolor(color)
    painter.begin_fill()
    painter.circle(7, 360, 4)
    painter.end_fill()
  if tiletype == "castle":
    painter.goto(posx + 50, posy - 50)
    painter.pendown()
    painter.fillcolor(color)
    painter.begin_fill()
    painter.circle(25, 360, 4)
    painter.end_fill()
  

print("running")


for y in range(300, -200, -100):
  print("outer")
  for x in range(-350, 250, 100):
    print("inner")
    selectedType = str(input("Select Tile Type: "))
    selectedColor = "white"

    if selectedType == "house" or selectedType == "castle":
      selectedColor = str(input("Select Tile Color: "))
    
    CreateTile(x, y, selectedType, selectedColor)

window = ttl.Screen()
window.mainloop()

