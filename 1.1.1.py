import turtle as ttl

painter = ttl.Turtle()
pty = 0
ptx = 0

painter.turtlesize(4)
painter.pensize(10)

def paintSquare(startx, starty, color):
  painter.penup()
  painter.goto(startx, starty)
  painter.pencolor(color)
  painter.pendown()

  for i in range(4):
    painter.forward(180)
    painter.right(90)
  painter.penup()
  ptx = painter.xcor()
  pty = painter.ycor()
  painter.goto(ptx + 90, pty - 140)
  painter.pendown()
  painter.circle(50)

paintSquare(0, 0, "red")
paintSquare(-180, 180, "blue")
paintSquare(-180, 0, "yellow")
paintSquare(0, 180, "green")

window = ttl.Screen()
window.mainloop()







