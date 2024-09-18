#   a116_buggy_image.py
import turtle as trtl

painter = trtl.Turtle()

# create the spider's body
painter.pensize(40)
painter.circle(20)

# configure spider legs
num_legs = 8
leg_length = 70
leg_angle = 360 / num_legs
painter.pensize(5)
leg_number = 0

#draw spider legs
while (leg_number < num_legs):
  painter.goto(0,20)
  painter.setheading(leg_angle*leg_number)
  painter.forward(leg_length)
  leg_number = leg_number + 1

painter.hideturtle()

wn = trtl.Screen()
wn.mainloop()