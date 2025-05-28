#   encode.py 6-10-24
#   Note this will not run in the code editor and must be downloaded
import tkinter as tk
import turtle as trtl
from PIL import ImageGrab, Image

# Configuration settings
BLOCK_SIZE = 21 # default turtle size
TRTL_START_LOC = 220 
BLOCK_GAP = 10

# Get the message from the user
message = tk.simpledialog.askstring("Input", "Enter a message to send.")

# Converts the message to its Unicode integer values
characters_as_ints = []
for cha in message:
  characters_as_ints.append(ord(cha))

# Converts the integers to binary
characters_as_bits = []
for integ in characters_as_ints:
  characters_as_bits.append('{0:08b}'.format(integ))

# Turns each one and zero from the binary values into separate integers
bits_as_ints = []
for index in range(0,len(characters_as_bits)):
  for bit in characters_as_bits[index]:
    bits_as_ints.append(bit)

# Screen setup
screen = trtl.getscreen()
screen.setup(1.0, 1.0, startx=0, starty=0)

# Turtle setup; creates the turtle and has it print the initial green square
painter = trtl.Turtle()
painter.penup()
painter.speed(0)
painter.shape("square")
painter.goto(-TRTL_START_LOC, TRTL_START_LOC)
painter.color("red")
painter.stamp()

# Have the turtle print another green square to establish the gap
painter.forward(BLOCK_SIZE + BLOCK_GAP)
painter.stamp()

# Change the x start location to compensate for initial gap
GAP_START_LOC = TRTL_START_LOC + BLOCK_GAP

# Has the turtle print out a grid of blue squares; the turtle will stamp a blue square if that spot corresponds to a "1" in the bits_as_ints list
#painter.color("red")
painter.shape("circle")
index = 0
while index < len(bits_as_ints):
  painter.forward(BLOCK_SIZE + BLOCK_GAP)
  if index % 8 == 0:
    painter.goto(-GAP_START_LOC, painter.ycor()-(BLOCK_SIZE + BLOCK_GAP))
  if bits_as_ints[index] == '1':
    painter.stamp()
  index += 1

# Has the screen be fullscreen
screen.setup(1.0, 1.0)

# Saves the turtle's drawing as an image
def create_image():
  root = trtl.getcanvas().winfo_toplevel()
  x0 = root.winfo_rootx()
  y0 = root.winfo_rooty()
  x1 = x0 + root.winfo_width()
  y1 = y0 + root.winfo_height()
  painter.hideturtle()
  ImageGrab.grab().crop((x0, y0, x1, y1)).save("encrypted_output.png")

# Attempts to capture the image; if the attempt fails, prompt the user to manually screenshot the image.
try:
  create_image()
  tk.messagebox.showinfo(message="Your screenshot was captured in the output.png file.")
except:
  tk.messagebox.showinfo(message="Take a manual sreenshot of the encoding.\nSave/rename the file to \"output\".\nClose the window when done.")
  trtl.mainloop()

# Have the user check if the output is proper, otherwise prompt them to manualy screenshot.
answer = tk.messagebox.askyesno(message="Is your output file correct?")
if not answer: 
  tk.messagebox.showinfo(message="Take a manual sreenshot of the encoding.\nSave/rename the file to \"output.png\".\nClose the window when done.")
  trtl.mainloop()