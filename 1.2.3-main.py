#   a123_apple_1.py
import turtle as trtl
import random

#-----setup-----
apple_image = "1.2.3-apple.gif" 
pear_image = "1.2.3-pear.gif"
background_image = "1.2.3-background.gif"


# window
wn = trtl.Screen()
wn.setup(width=1.0, height=1.0)
wn.addshape(apple_image) 
wn.addshape(pear_image)
wn.bgpic(background_image)

# letters
letters = "abcdefghijklmnopqrstuvwxyz;"
message = ""
apple_font = ("Arial", 30, "bold")
apple_font_color = "white"

# physics 
falling_apples = []
start_velocity = 10
acceleration = 1.05
ground_offset = -50
timer_delay = 3

# apple
apples = []
num_apples = 5

#-----functions-----

# Takes a turtle, assigns it the apple picture and a specified letter, and writes the letter on the apple
def draw_apple(active_apple, letter, x, y):

  active_apple.letter = letter
  active_apple.shape(apple_image)
  active_apple.color(apple_font_color)

  wn.tracer(False)
  active_apple.goto(x, y - 30)
  active_apple.write(letter.upper(), False, "center", font=apple_font)
  active_apple.goto(x, y)
  wn.tracer(True)
  wn.update()

# Causes an apple to fall from the tree of a specified letter
def fall_apple(letter):
  
  active_apple = 1

  if len(apples) != 0:
    for apple in apples:
      if apple.letter == letter:
        active_apple = apple
        active_apple.clear()
        falling_apples.append(active_apple)
        break
  
    

# Causes all falling apples to accelerate downward
def run_fall():
  if len(apples) > 0:
    if len(falling_apples) > 0:

      for active_apple in falling_apples:
        active_apple.goto(active_apple.xcor(), active_apple.ycor() - active_apple.velocity)
        active_apple.velocity = active_apple.velocity * acceleration
        if (active_apple.ycor() < -0.5 * wn.window_height() + ground_offset):
          active_apple.hideturtle()
          if active_apple in apples:
            apples.remove(active_apple)
          falling_apples.remove(active_apple)

    wn.ontimer(run_fall,timer_delay)
    wn.update()
  #Reset game protocol
  else:
    setup_game()

# Connects pressing a letter key to falling the apple with that letter
def setup_letter_events():
  global message
  for letter in message:
    wn.onkeypress(lambda letter=letter: fall_apple(letter), letter)

# Sets up the game
def setup_game():
  # Creates the list of letters that will be used in the game instance
  global message

  message = ""

  for num in range(num_apples):
    letter = random.choice(letters)
    while letter in message:
      letter = random.choice(letters)
    message = message + letter

  # Creates apples for each letter
  for letter in message:
    new_apple = trtl.Turtle()
    new_apple.speed(0)
    new_apple.penup()
    new_apple.letter = ""
    new_apple.velocity = start_velocity
    apples.append(new_apple)
    newx = random.randint(-200, 200)
    newy = random.randint(-100, 100)
    draw_apple(new_apple, letter, newx, newy)

  # Sets up letter events
  setup_letter_events()

  # Starts the apple acceleration
  run_fall()

#-----function calls-----
setup_game()
wn.listen()
wn.mainloop()