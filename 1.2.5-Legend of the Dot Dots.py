#Legend of the Dot Dots: Avoid a bunch of dots that target you and make them crash into each other or the walls/obstacles. Get through as many levels as possible. Use scoreboard if time.

import turtle as turt
import random
import math
import time

#------------------------------------------------------Game Configurations
# Player
player_move_speed = 130
player_shape = "circle"
player_color = "green"
player_size = 1

# Enemies
screen_turtles = []
enemy_types = {
  "basic": {"probability":10, "score":1, "speed":9, "turn_speed":20, "color":"black", "size":1},
  "faster": {"probability":6, "score":1, "speed":15, "turn_speed":20, "color":"gray", "size":1},
  "shooter": {"probability":4, "score":2, "speed":7, "turn_speed":15, "color":"red", "size":1},
  "barrel": {"probability":6, "score":0, "speed":0, "turn_speed":0, "color":"brown", "size":2},
  "bullet": {"probability":0, "score":0, "speed":50, "turn_speed":0, "color":"black", "size":0.5},
  "big": {"probability":3, "score":1, "speed":6, "turn_speed":3, "color":"black", "size":1.5},
  "explosive": {"probability":4, "score":2, "speed":10, "turn_speed":15, "color":"orange", "size":1.25}
}
inner_spawn_margin = 100
outer_spawn_margin = 50
too_close_distance = 20
summoned_displacement_amount = 20
num_enemies = 6
shooter_update_delay = 10
max_projectiles = 4
explosion_radius = 100
explosion_angle = 30
unsolvable_delay = 5

# Collisions
collision_distance = 25

# Enemy destruction
destroy_lines = 3
destroy_angle = 10
destroy_length = 50

# Game and Score
game_over = False
score = 0
score_x = 0
score_y = 0
score_margin = 50
score_font = ("sansserif", 50, "normal")

# Title page
title = "Legend of the Dot Dots"
subtext = "Click Screen to Start"
title_x = 0
title_y = 0
title_gap = 20
title_font = ("Arial", 70, "normal")
subtitle_font = ("Arial", 20, "normal")

# Background
background_colors = ["lightgreen", "white", "cyan"]

#------------------------------------------------------Object Setup
# Player setup
player = turt.Turtle(shape=player_shape)
player.penup()
player.color(player_color)
player.turtlesize(player_size)
screen_turtles.append(player)
player.speed(0)

# Scorewriter setup
score_writer = turt.Turtle()
score_writer.hideturtle()
score_writer.penup()
score_writer.speed(0)

# Screen setup
window = turt.Screen()
window.setup(1.0, 1.0)
window.bgcolor(random.choice(background_colors))

#------------------------------------------------------Function Declarations

# =================================== Returns the number of a type of enemy on the screen
def get_num(variety):
  global screen_turtles
  count = 0
  
  for turtle in screen_turtles:
    if turtle != player:
      if turtle.variety == variety:
        count += 1

  return count

# =========================== Destroys a turtle
def destroy(turtle, show_lines):
  global screen_turtles
  global game_over
  global score

  turtle.hideturtle()

  # If the player was caught, end the game.
  if turtle == player:
    game_over = True

  elif turtle in screen_turtles:
    score += enemy_types.get(turtle.variety).get("score")
    screen_turtles.remove(turtle)

    # If there are no more enemies (not counting projectiles etc.), end the game.
    if len(screen_turtles) - get_num("barrel") - get_num("bullet") <= 1:
      game_over = True

    # Do the destruction lines
    if show_lines:
      turtle.pendown()
      # Do the explosion
      if turtle.variety == "explosive":
        for degrees in range(0, 360, explosion_angle):
          turtle.setheading(degrees)
          turtle.forward(explosion_radius)
          turtle.backward(explosion_radius)
        check_collisions(turtle, explosion_radius)
      else:
        turtle.right(180 + destroy_angle * 0.5 * destroy_lines)
        for line in range(destroy_lines):
          turtle.forward(destroy_length)
          turtle.backward(destroy_length)
          turtle.left(destroy_angle)

    # Do the on-death things
    if turtle.variety == "big":
      summon(turtle, "basic")

# =========================== Deals with collisions between two turtles
def check_collisions(turtle, distance):
  global screen_turtles
  
  x_pos = turtle.xcor()
  y_pos = turtle.ycor()
  max_width = window.window_width() / 2
  min_width = window.window_width() / -2
  max_height = window.window_height() / 2
  min_height = window.window_height() / -2

  # Destroy the turtle if they go offscreen
  if x_pos > max_width or x_pos < min_width or y_pos > max_height or y_pos < min_height:
    destroy(turtle, False)
  
  # Otherwise, see if they are colliding with any turtles
  else:
    for other in screen_turtles:
      other_xpos = other.xcor()
      other_ypos = other.ycor()
      dist_x = other_xpos - x_pos
      dist_y = other_ypos - y_pos
      total_dist = math.sqrt(dist_x ** 2 + dist_y ** 2)
      
      if total_dist < distance and other != turtle:
        destroy(turtle, True)
        destroy(other, True)
        break


# =========================== Makes the enemy move towards the player
def move_towards(turtle, target_x, target_y, speed, turn_speed):
  curr_x = turtle.xcor()
  curr_y = turtle.ycor()
  dist_x = target_x - curr_x
  dist_y = target_y - curr_y
  total_dist = math.sqrt(dist_x ** 2 + dist_y ** 2)

  # Get the angle between the turtle and two points
  target_angle = math.degrees(math.atan2(dist_y, dist_x))

  # Get the total amount the turtle needs to turn to reach the target. 
  total_turn_amount = (turtle.heading() - target_angle) % 360
  
  # Choose the turn direction, and go directly to the player if close enough
  if abs(total_turn_amount) <= turn_speed:
      turtle.setheading(target_angle)
  elif total_turn_amount < 180:
    turtle.right(turn_speed)
  else:
    turtle.left(turn_speed)
    
  turtle.forward(speed)

# =========================== Functions for special enemies (shooting ones etc)
def summon(summoner, summoned_type):
  summoned = create_enemy(summoned_type, summoner.xcor(), summoner.ycor())
  summoned.setheading(summoner.heading())
  summoned.forward(summoned_displacement_amount)
  return summoned
  
  
# =========================== Create an enemy
def create_enemy(type, pos_x, pos_y):

  # Retrieve the information on that type from the dictionary
  enemy_stats = enemy_types.get(type)

  # Create the turtle with the information
  enemy = turt.Turtle(shape="circle")
  enemy.color(enemy_stats.get("color"))
  enemy.turtlesize(enemy_stats.get("size"))
  enemy.penup()
  enemy.speed(0)

  # Set the rest of the stats as new properties
  enemy.velocity = enemy_stats.get("speed")
  enemy.turn_velocity = enemy_stats.get("turn_speed")
  enemy.variety = type

  # Place the enemy on the screen, and have it face towards the player
  enemy.goto(pos_x, pos_y)
  move_towards(enemy, player.xcor(), player.ycor(), 0, 360)

  # Add to the list of turtles
  screen_turtles.append(enemy)
  return enemy

# =========================== Creates enemies on the screen, choosing from each class's probabilities. 
def create_enemies(number):
  options_list = []
  global enemy_types
  global screen_turtles

  #Create a list of types, adjusted for the probability of choosing each type
  for variety in enemy_types:
    for i in range(enemy_types.get(variety).get("probability")):
      options_list.append(variety)

  # Create the specified number of entities, choosing from the probability-adjusted list.
  for i in range(number):
    too_close = False
    new_enemy_type = random.choice(options_list)
    new_x = 0
    new_y = 0

    while abs(new_x) <= inner_spawn_margin or abs(new_y) <= inner_spawn_margin or too_close:
      too_close = False
      new_x = random.randint(int(window.window_width() / -2 + outer_spawn_margin), int(window.window_width() / 2 - outer_spawn_margin))
      new_y = random.randint(int(window.window_height() / -2 + outer_spawn_margin), int(window.window_height() / 2 - outer_spawn_margin))
      for other_enemy in screen_turtles:
        dist_x = other_enemy.xcor() - new_x
        dist_y = other_enemy.ycor() - new_y
        total_dist = math.sqrt(dist_x ** 2 + dist_y ** 2)

        if total_dist <= too_close_distance:
          too_close = True
          break
    
    create_enemy(new_enemy_type, new_x, new_y)

# =================================== Clears screen
def clear_screen():
  player.goto(0, 0)
  for turtle in screen_turtles:
    if turtle != player:
      destroy(turtle, False)

# =================================== Displays score
def display_score(x, y, say_score):
  global score

  pretext = "Score: "
  score_writer.clear()
  score_writer.goto(x, y)
  if not say_score:
    pretext = ""
  score_writer.write(pretext + str(score), False, "center", score_font)

# ==================================== Shows title, waits until the player clicks the screen
def show_title():
  # Create the title
  score_writer.goto(title_x, title_y)
  score_writer.write(title, False, "center", title_font)
  score_writer.goto(title_x, title_y - title_gap)
  score_writer.write(subtext, False, "center", subtitle_font)

  # Set up the game to start on click
  window.onclick(run_game)

  # TODO stuff to happen...

# =================================== Runs the game
def run_game(x, y):
  global game_over

  game_over = False
  index = 0
  prev_score = 0
  updates_since = 0

  score_writer.clear()
  window.onclick(None)
  create_enemies(num_enemies)

  # Iterates over all the turtles and moves them towards the player
  while not game_over:

    speed_mod = 1.0
    # Makes a modifier for speed for the enemies, so that if there are less to iterate over they don't go too fast
    if len(screen_turtles) - get_num("barrel") - get_num("bullet") < 3:
      speed_mod = 0.5

    for enemy in screen_turtles:
      if enemy != player:
        move_towards(enemy, player.xcor(), player.ycor(), enemy.velocity * speed_mod, enemy.turn_velocity)
        check_collisions(enemy, collision_distance)
        if enemy.variety == "shooter" and index % shooter_update_delay == 0 and get_num("bullet") < max_projectiles:
          summon(enemy, "bullet").pencolor(window.bgcolor())

    if prev_score != score:
      display_score(window.window_width() / -2 + score_margin, window.window_height() / 2 - 2 * score_margin, False)
    prev_score = score

    # Creates a new enemy if there is only one left (making the game unsolvable)
    if len(screen_turtles) - get_num("bullet") <= 2 and not game_over:
      if updates_since < unsolvable_delay:
        updates_since += 1
      else:
        create_enemies(1)

    index += 1

  # If player has won (no enemies left), reset the game
  if len(screen_turtles) - get_num("barrel") - get_num("bullet") <= 1:
      clear_screen()
      run_game(0, 0)
  # If the player has lost, end the game and report the score.    
  else:
    display_score(score_x, score_y, True)

# ====================================== Player controls
def player_up():
  if not game_over:
    player.setheading(90)
    player.forward(player_move_speed / len(screen_turtles))

def player_down():
  if not game_over:
    player.setheading(270)
    player.forward(player_move_speed / len(screen_turtles))

def player_left():
  if not game_over:
    player.setheading(180)
    player.forward(player_move_speed / len(screen_turtles))

def player_right():
  if not game_over:
    player.setheading(0)
    player.forward(player_move_speed / len(screen_turtles))

#------------------------------------------------------Function Calls and Events
  
window.onkey(player_up, "w")
window.onkey(player_down, "s")
window.onkey(player_left, "a")
window.onkey(player_right, "d")
window.onkey(clear_screen, "l")

window.listen()

show_title()

window.mainloop()