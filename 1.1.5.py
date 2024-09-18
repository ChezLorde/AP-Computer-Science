#   a115_robot_maze.py
import turtle as trtl

#----- maze and turtle config variables
screen_h = 400
screen_w = 420
startx = -100
starty = -100
turtle_scale = 1.5

#------ robot commands
def move():
  robot.dot(10)
  robot.fd(50)

def turn_left():
  robot.speed(0)
  robot.lt(90)
  robot.speed(2)

#----- init screen
wn = trtl.Screen()
wn.setup(width=screen_w, height=screen_h)
robot_image = "1.1.5-robot.gif"
wn.addshape(robot_image)

#----- init robot
robot = trtl.Turtle(shape=robot_image)
robot.hideturtle()
robot.color("darkorchid")
robot.pencolor("darkorchid")
robot.penup()
robot.setheading(90)
robot.turtlesize(turtle_scale, turtle_scale)
robot.goto(startx, starty)
robot.speed(2)
robot.showturtle()

#---- TODO: change maze here
wn.bgpic("1.1.5-maze3.png") # other file names should be maze2.png, maze3.png

#---- TODO: begin robot movement here
# move robot forward with move()
# turn robot left with turn_left()
# sample for loop:
'''
for step in range(3): # forward 3
  move()
'''
print(wn.bgpic())
if wn.bgpic() == "1.1.5-maze1.png":

  print("Running Maze1")

  #forward 4
  for step in range(4):
    move()

  #Turn right
  for turn in range(3):
    turn_left()

  #forward 4
  for step in range(4):
    move()

elif wn.bgpic() == "1.1.5-maze2.png":

  #Route 1
  for step in range(3):
    move()
  for turn in range(3):
    turn_left()
  for step in range(2):
    move()

  #Reset for Route 2
  robot.goto(startx, starty)

  #Route 2
  for side in range(2):
    for step in range(3):
      move()
    turn_left()
  move()

elif wn.bgpic() == "1.1.5-maze3.png":
  for diag in range(4):
    move()
    for turn in range(3):
      turn_left()
    move()
    turn_left()
    if diag >= 1:
      robot.pencolor("green")

#---- end robot movement 

wn.mainloop()
