# Turtle whack-a-mole game : APCSP 1.2.1/1.2.2

# ---------------------------------------------------------- Import Statements
import turtle
import math
import random
import leaderboard


# ---------------------------------------------------------- Game Configuration
# Leaderboard
leaderboard_file_name = "1.2.2_leaderboard.txt"
player_name = input("Please enter name: ")

# Target
target_color = "green"
target_size = 2
target_shape = "circle"

# Target placement on screen
min_new_distance = 10
margin = 50

# Background
background_color = "lightblue"
background_shapes_colors = ["blue", "lightsteelblue", "steelblue", "cornflowerblue", "azure", "lavender", "lightcyan"]
background_shapes = ["triangle", "square", "circle"]
num_background_shapes = 6
min_shape_size = 10
max_shape_size = 15

# Scoreboard
scoreboard_x_offset = 50
scoreboard_y_offset = 50
score_font = ("Arial", 20, "normal")
score = 0

# Timer
timer_x_offset = 200
timer_y_offset = 50
timer_font = ("Arial", 20, "normal")
start_timer = 30
counter_interval = 1000
timer_up = False
timer = start_timer

# ---------------------------------------------------------- Initialize Turtle Objects
# The screen
screen = turtle.Screen()
screen.bgcolor(background_color)

# The target
target = turtle.Turtle()
target.shape(target_shape)
target.fillcolor(target_color)
target.shapesize(target_size)
target.penup()
target.speed(0)

# The writer for the scoreboard
score_writer = turtle.Turtle()
score_writer.hideturtle()
score_writer.penup()
score_writer.speed(0)

# The writer for the countdown
counter = turtle.Turtle()
counter.hideturtle()
counter.penup()
counter.speed(0)

# The drawer for the background
shaper = turtle.Turtle()
shaper.speed(0)
shaper.penup()
shaper.hideturtle()

# ---------------------------------------------------------- Game Functions
# Manage the leaderboard for the top 5 scorers
def manage_leaderboard():
    # get the names and scores from the leaderboard file
    leader_names_list = leaderboard.get_names(leaderboard_file_name)
    leader_scores_list = leaderboard.get_scores(leaderboard_file_name)

     # show the leaderboard with or without the current player
    if (len(leader_scores_list) < 5 or score >= leader_scores_list[4]):
        leaderboard.update_leaderboard(leaderboard_file_name, leader_names_list, leader_scores_list, player_name, score)
        leaderboard.draw_leaderboard(True, leader_names_list, leader_scores_list, target, score)
    else:
        leaderboard.draw_leaderboard(False, leader_names_list, leader_scores_list, target, score)

# Get the current min/max width/height values of the screen
def get_screen_size(direc, limit):
    value = 0

    if direc == "height":
        value = screen.window_height() / 2
    elif direc == "width":
        value = screen.window_width() / 2

    if limit == "min":
        value *= -1

    return value

# Change the position of the target to a random new one 
def change_position(x, y, turtle):
    turtle.penup()
    turtle.hideturtle()
    turtle.speed(0)

    newx = x
    newy = y

    while math.sqrt(((newx - x) ** 2) + ((newy - y) ** 2)) < min_new_distance:
        xmax = int(get_screen_size("width", "max") - margin)
        xmin = int(get_screen_size("width", "min") + margin)
        ymax = int(get_screen_size("height", "max") - margin)
        ymin = int(get_screen_size("height", "min") + margin)

        newx = random.randint(xmin, xmax)
        newy = random.randint(ymin, ymax)

    turtle.goto(newx, newy)
    turtle.showturtle()

# Increase the score
def update_score():
    global score
    score += 1

    print("Score: ", score)

    scoreboard_x = get_screen_size("width","min") + scoreboard_x_offset 
    scoreboard_y = get_screen_size("height","max") - scoreboard_y_offset 

    score_writer.goto(scoreboard_x, scoreboard_y)
    score_writer.clear()
    score_writer.write(score, font=score_font)

# Decrease the remaining time
def countdown():
    global timer, timer_up
    text = "-null-"
  
    if timer <= 0:
        text = "Out of Time"
        timer_up = True
        manage_leaderboard()
    else:
        text = "Time Left: " + str(timer)
        timer -= 1
        counter.getscreen().ontimer(countdown, counter_interval)

    timer_x = get_screen_size("width","max") - timer_x_offset 
    timer_y = get_screen_size("height","max") - timer_y_offset

    counter.clear()
    counter.goto(timer_x, timer_y)
    counter.write(text, font=timer_font)

# Create the background
def background():
    shaper.clear()
    
    for shape in range(num_background_shapes):
        change_position(shaper.xcor(), shaper.ycor(), shaper)
        shaper.color(random.choice(background_shapes_colors))
        shaper.shape(random.choice(background_shapes))
        shaper.shapesize(random.randint(min_shape_size, max_shape_size))
        shaper.setheading(random.randint(0, 360))
        shaper.stamp()

# Executes when the target is clicked
def target_clicked(x, y):
    global timer_up
    print(timer)

    if not timer_up:
        print("Target Clicked at: ", x, y)
        change_position(x, y, target)
        update_score()
    else:
        target.hideturtle()

#Starts the game
def start_game(x, y):
    global timer, timer_up, score, start_timer

    score = -1
    timer = start_timer
    timer_up = False

    target.showturtle()

    update_score()
    background()
    print(timer)

# ---------------------------------------------------------- Events
start_game(0, 0)
target.onclick(target_clicked)
screen.ontimer(countdown, counter_interval)
screen.mainloop()