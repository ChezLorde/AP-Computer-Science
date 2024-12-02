# Text Adventure Game
import os
import math
import string
import random

# Rooms with stats: Doors that lead to other rooms, items to pick up, locked doors, text of anything else so say about the room
rooms = []
all_doors = []
all_items = []

# Player's items
items = []
to_get = []

# Text to use in names
adjectives = ["brown", "red", "gray", "blue", "teal", "orange", "yellow", "green", "small", "large", "old", "new", "glass", "wood", "steel", "brass", "iron", "plastic"]
descriptions = ["There is a stain on the wall.", "There is a potted plant in the corner.", "There is a bricked in window on the left wall.", "The room is cold.", "The room is warm.", "There is a puddle on the ground.", "There is a table in the corner.", "There is a chair in the center of the room."]
objects = ["vase", "shoe", "cup", "box", "bucket", "frog", "elephant", "bottle"]

# Room configurations
num_rooms = 20
items_to_find = 3
lock_prob = 0.4 #<- Probability of adding a key or a locked door to a room
new_door_prob = 0.2 #<- Probability of adding a new door to a room
new_item_prob = 0.4

# Special Room stuff
code_len = 3
notebook_page_len = 6

# Generation lists
to_lock = []
key_adj_left = adjectives

# Messages
help_message = "Commands:\n - pickup <adj> <item>\n - drop <adj> <item>\n - use <adj> <item>\n - enter <adj> <door> \n - back\n - items\n - help\n - goals\n - endgame"
line_max_length = 30 # <- Determines where and if a string should have newline characters added.

# Stored room data
previous_rooms_numbers = [0]

# -------------------------------------------------- Class setup

# Item class
class item:
  def __init__(self, name, adj, description):
    self.name = name
    self.description = description
    self.adj = adj
    all_items.append(self)

  # Notebook subclass
  def make_notebook(self, pages):
    self.pages = pages
    self.current_page = 0
    return self

  def set_page(self, page_num):
      if page_num >= 0 and page_num < len(self.pages):
          self.current_page = page_num

  def open_page(self):
    page_text = self.pages[self.current_page]
    page_lines = get_num_lines(page_text)
        
    clear()
    print("=============================")
    print(page_text)
    # Fill in any missing lines in the page so it is always the same length
    for i in range(notebook_page_len - page_lines):
        print("")
    print("=============================")
    command = input("'next', 'previous' or 'close'  -->    ").rstrip()

    if command == "next":
        self.set_page(self.current_page + 1)
        self.open_page()
    elif command == "previous":
        self.set_page(self.current_page - 1)
        self.open_page()
  
  # Lockbox subclass
  def make_lockbox(self, passcode, contents):
    self.locked = True
    self.passcode = passcode
    self.contents = contents
    return self
    
  def try_unlock(self):
    entry = input("Enter Passcode:  -->    ")
      
    if entry == self.passcode:
        print("The lockbox was unlocked.")
        self.locked = False
        return True
    else:
        print("The lockbox will not unlock.")
        return False

  def on_use(self):
    global items

    if self.locked:
        self.try_unlock()
    
    if not self.locked:
        # Print a list of contents
        print("Lockbox contents: ")
        for item in self.contents:
            print(" - " + item.adj + " " + item.name)
            
        # Enter commands
        commands = input("'pickup <adj> <item>' or 'close'  -->    ").rstrip().split(" ")
            
        if commands[0] == "pickup":
            for item in self.contents:
                if item.adj == commands[1] and item.name == commands[2]:
                    self.contents.remove(item)
                    items.append(item)
                    print("Picked up " + item.adj + " " + item.name)
                    break       

# Door class
class door:
  def __init__(self, dest, adj, locked=False):
    self.dest = dest
    self.locked = locked
    self.adj = adj
    all_doors.append(self)

  # Unlocks the door if the player has a key that matches
  def unlock(self, key):
    if self.locked == True:
      # Go through the player's items and see if they have a key with a matching adjective.
      if key.name == "key" and key.adj == self.adj:
        self.locked = False
        items.remove(key)
      
      # Determine the return message
      if self.locked == True:
        return "You do not have the correct key."
      else:
        return "The " + self.adj + " door was unlocked."
    else:
      return "This door is already unlocked."
    
# Room class
class room:
  def __init__(self, description, doors=list, items=list):
    self.description = description
    self.doors = doors
    self.items = items

  # DOOR FUNCTIONS
  def add_door(self, door):
    self.doors.append(door)

  def get_door(self, adj):
    chosen_door = None
    for door in self.doors:
      if door.adj == adj:
        chosen_door = door
    return chosen_door
  
  def get_locked_doors(self):
    locked_doors = []
    for door in self.doors:
      if door.locked == True:
        locked_doors.append(door)
    return locked_doors

  # ITEM FUNCTIONS
  def add_item(self, item):
    self.items.append(item)

  def remove_item(self, item):
    self.items.remove(item)

  def get_item(self, name, adj):
    chosen_item = None
    for item in self.items:
      if item.name == name:
        chosen_item = item
    return chosen_item

# ----------------------------------------------------- Functions
def clear():
  os.system("cls")

# Has a probability of returning true; a way to make floats into probabilities
def if_prob(probability=float):
  number = random.random()
  if probability > number:
    return True
  else:
    return False

# Should a word be preceded by a or an?
def a_or_an(string):
  vowels = ["a", "e", "i", "o", "u"]
  if string[0] in vowels:
    return "an"
  else:
    return "a"
  
# Find a specific item the player has
def get_item(name, adj):
  chosen_item = None
  for item in items:
    if item.name == name:
      if item.adj == adj:
        chosen_item = item
  return chosen_item


# Splitting up text lines function
def split_lines(text):
  if len(text) > line_max_length and False: #< - Turns this off; wasn't neccessary as the terminals do this themselves better
    times_to_split = math.floor(len(text) / line_max_length)
    words = text.split(" ")
    result_text = ""
    characters_indexed = 0
    
    for word in words:
      characters_indexed += len(word)
      
      # Insert newline whenever we get through enough characters
      if characters_indexed > line_max_length:
        index = words.index(word)
        words.insert(index, "\n")
        characters_indexed = 0
      
    for word in words:
      if word[len(word) - 1] == "\n":
        result_text = result_text + word
      else:
        result_text = result_text + word + " "
      
    return result_text
    
  else:
    return text

# Gets the number of lines in a text
def get_num_lines(text):
    num_lines = 1
    for char in text:
        if char == "\n":
            num_lines += 1
    return num_lines
    
def generate_passcode(length):
  passcode = ""

  for i in range(length):
    passcode = passcode + random.choice(string.ascii_lowercase)
    
  return passcode

# ----------------------------------------------------------------------------------------------Special Items

# Key use protocol
def use_key(room, key):

  clear()
  # If there are any doors to unlock, have the player select which door to unlock.
  if len(room.get_locked_doors()) > 0:

    # Try to get the door that matches the adjective of the key
    selected_door = room.get_door(key.adj)

    if selected_door is not None:
      message = selected_door.unlock(key)
      print(message)
    else:
      print("The key does not fit in any of the doors.")
  else:
    print("There are no doors to unlock in this room.")


# Generates a destination for a door
def nxt_room_num(dont_pick_list): #-------------------------------------------------------------------------------RANDOM GENERATION
  global rooms
  global all_doors
  
  found = None
  
  for list_room in rooms:
    is_empty = True
    #1. Check if there is anything in the room
    if list_room.description == "":
      #2. Check if there are any doors that enter on this room
      for list_door in all_doors:
        if list_door.dest == rooms.index(list_room):
          is_empty = False
    else:
      is_empty = False
      
    if is_empty:
      found = rooms.index(list_room)
      break
  
  # Create a door to a random room if there are no empty rooms left
  if found == None:
    found = random.randint(0, num_rooms - 1)
    while found in dont_pick_list:
      found = random.randint(0, num_rooms - 1)
  return found
          

# Creates the randomly generated rooms. Or not...
def create_rooms():
  global rooms
  global all_doors

  # Setup numbers for special rooms
  fountain_room_num = random.randint(4, num_rooms - 1)
  theater_room_num = random.randint(6, num_rooms - 1)
  closet_room_num = random.randint(4, num_rooms - 1)
  
  # Create the specified number of rooms
  for room_number in range(num_rooms):
    rooms.append(room("", [], []))
    
  # Set up the rooms in order
  for index in range(len(rooms)):
    if index == fountain_room_num:
        fountain_room(rooms[index])
    elif index == theater_room_num:
        little_theater(rooms[index])
    elif index == closet_room_num:
        closet(rooms[index])
    else:
        setup_room(rooms[index])
    
  # Get rid of any doors that do not open on a room
  for list_room in rooms:
    for list_door in list_room.doors:
      if list_door.dest == None:
        all_doors.remove(list_door)
        list_room.doors.remove(list_door)
  

# Fills out a new room with keys and such
def setup_room(new_room):
  global to_lock
  global rooms
  global key_adj_left

  new_description = ""
  room_items = []
  dont_pick_nums = [rooms.index(new_room)] #<- Room numbers that the doors should not go to, starting with this one.
  room_doors = []

  # Determine room description + add it in: Needed so room finder for door function will not choose the same room
  new_description = random.choice(descriptions)
  new_room.description = new_description

  # Add doors, locked doors and keys IF there are still rooms to be added beyond this one.
  if rooms.index(new_room) < num_rooms - 1:
    # Randomize chance for a key; if so, add to the list of doors to lock.
    if if_prob(lock_prob) and len(key_adj_left) > 0:
      # Get an adjective from the remaining
      key_adj = random.choice(key_adj_left)
      key_adj_left.remove(key_adj)

      # Create the key
      new_key = item("key", key_adj, "on the ground")
      room_items.append(new_key)

      # Save it to the list of doors to add locks to.
      to_lock.append(key_adj)

    # Randomize chance for a locked door; go through each key needing a door and probability it to get a door.
    for adj in to_lock:
      if if_prob(lock_prob):
          dest = nxt_room_num(dont_pick_nums)
          new_door = door(dest, adj, True)
          room_doors.append(new_door)
          dont_pick_nums.append(dest)
          to_lock.remove(adj)

    # Make sure room has at least 1 door
    new_dest = nxt_room_num(dont_pick_nums)
    room_doors.append(door(new_dest, random.choice(adjectives), False))
    dont_pick_nums.append(new_dest)

    # Probability for additional doors
    while if_prob(new_door_prob):
      new_dest = nxt_room_num(dont_pick_nums)
      room_doors.append(door(new_dest, random.choice(adjectives), False))
      dont_pick_nums.append(new_dest)

  # Add in other items
  while if_prob(new_item_prob):
    room_items.append(item(random.choice(objects), random.choice(adjectives), "on the ground"))

  # Add doors and items
  new_room.doors = room_doors
  new_room.items = room_items

  return new_room

# ---------------------------------------------------------------------- Special Room Setups
def fountain_room(new_room):
  
  passcode = generate_passcode(code_len)
  
  notebook = item("notebook", "frayed", "on the marble rim of the fountain")
  notebook.make_notebook(["The passcode is " + passcode])
  
  lockbox = item("lockbox", "army-green", "that requires a 3-letter code, on the floor")
  lockbox.make_lockbox(passcode, [item("key", "ornate", "in the lockbox.")])

  nxt_room_num([rooms.index(new_room)])
  
  new_room.description = split_lines("The room is rather large. Under its fluorescent lights, a ring of planter beds filled with dandelions surrounds the ornate marble fountain in the center of the room. Your attention is immediately drawn to what lays precariously on the rim of the fountain.")
  new_room.add_door(door(nxt_room_num([rooms.index(new_room)]), "ornate", True))
  new_room.add_item(notebook)
  new_room.add_item(lockbox)
  
def little_theater(new_room):
  pass1 = generate_passcode(code_len)
  pass2 = generate_passcode(code_len)
  
  notebook = item("notebook", "purple", "in a seat").make_notebook(["\n  SCRIPT", 
                                                                    "Choose Wisely\nRED:  " + pass1 + "\nBLUE:  " + pass2, 
                                                                    "Shall I compare thee to a summer's day?\nThou art more lovely and more temperate;\nRough winds do shake the darling buds of May,\nAnd summer's lease hath all too short a date:\nSometime too hot the eye of heaven shines,\nAnd often is his gold complexion dimm'd;", 
                                                                    "And every fair from fair sometime declines,\nBy chance or nature's changing course untrimm'd;\nBut thy eternal summer shall not fade\nNor lose possession of that fair thou owest;\nNor shall Death brag thou wander’st in his shade,\nWhen in eternal lines to time thou growest:",
                                                                    "So long as men can breathe or eyes can see,\nSo long lives this and this gives life to thee.\n\n– William Shakespeare"
                                                                    ])

  blue_box = item("lockbox", "blue", "on the stage").make_lockbox(pass2, [])
  red_box = item("lockbox", "red", "on the stage").make_lockbox(pass1, [])
  
  key = item("key", "black", "in the lockbox")
  
  room_doors = [door(nxt_room_num([rooms.index(new_room)]), "black", True)]
  room_items = [blue_box, red_box]
  
  random.choice(room_items).contents = [key]

  room_items.append(notebook)
  
  new_room.description = split_lines("The room is rectangular, with a small, curved bank of red velvet seats facing a small wooden stage to the right. The walls are painted black.")
  new_room.doors = room_doors
  new_room.items = room_items
  
def closet(new_room):
  potential_items = [("coat", "mink", "hanging on the bar"),
                    ("coat", "fur", "hanging on the bar"),
                    ("jacket", "ski", "hanging on the bar"),
                    ("jacket", "leather", "hanging on the bar"),
                    ("sweater", "wool", "hanging on the bar"),
                    ("sneakers", "new", "on the ground")]
  room_items = []
  for i in range(random.randint(1, 3)):
    selected_set = random.choice(potential_items)
    new_item = item(selected_set[0], selected_set[1], selected_set[2])
    room_items.append(new_item)
    
  new_room.description = split_lines("The room is more of a closet, and there is a wooden bar extending across its width on which to hang coats of sorts. It is very dusty inside.")
  new_room.items = room_items
  
  
# Function for opening a room and accepting player inputs ------------------------------------------------Opening Rooms
def open_room(room_number):
  global items
  global previous_rooms_numbers

  clear()
  print("You enter the room." + str(room_number))

  # Get the information on the room
  room = rooms[room_number]
  room_doors = room.doors
  room_items = room.items

  # Print the room's description
  print(room.description + "\n")

  # Generate text for doors
  if len(room_doors) > 0:

    bullet = ""

    # Procedure for more than 1 door: State the number, and introduce each door with a bullet.
    if len(room_doors) > 1:
      print("There are " + str(len(room_doors)) + " doors. ")
      bullet = " - "

    for door in room_doors:
      # Check if the door is locked. If so, add a locked message
      locked_text = ""
      if door.locked == True:
        locked_text = " It is locked."

      # Print the final message.
      print(bullet + "There is a " + str(door.adj) + " door." + locked_text)

  # Generate text for items
  if len(room_items) > 0:
    for item in room_items:
      print("There is " + a_or_an(item.adj) + " " + item.adj + " "+ item.name + " " + item.description + ".")

  # Ask for inputs
  command = input("-->  ").rstrip().lower()
  commands = command.split(" ")

  # Handles single-word commands
  if len(commands) == 1:
    # Help command: Bring up commands menu list
    if command == "help":
      clear()
      print(help_message)
      input("Type any key to continue -->  ")
      open_room(room_number)

    # Back command: open previous room
    elif command == "back":
      if len(previous_rooms_numbers) > 1:
        # Get the last room from the top of the "stack"
        to_enter_number = previous_rooms_numbers[len(previous_rooms_numbers) - 1]

        # Get rid of the number and open the room
        previous_rooms_numbers.remove(to_enter_number)
        open_room(to_enter_number)
      else:
        open_room(0)

    # Items command: Prints a list of the player's items
    elif command == "items":
      clear()
      print("Your items: ")
      for item in items:
        print(" - " + item.adj + " " + item.name)
      input("Type any key to continue -->  ")
      open_room(room_number)

    elif command == "endgame":
      print("The game has been terminated.")
    
    elif command == "goals":
      clear()
      print("Your goals: ")
      num_req_met = 0

      for item in to_get:
        met = does_player_have(item)

        if met:
          print(" - " + item.adj + " " + item.name + " (Has)")
          num_req_met += 1
        else:
          print(" - " + item.adj + " " + item.name)

      # If player has all 3 items: End game
      if num_req_met == items_to_find:
        print("Congratulations! You have found all 3 items.")
      else:
        input("Type any key to continue -->  ")
        open_room(room_number)

    # If command is illegible, reopen the room
    else:
      open_room(room_number)

  # Handles 3-word commands: Pickup, Drop, Use, Enter
  elif len(commands) == 3:
    action = commands[0]
    adj = commands[1]
    object = commands[2]

    if action == "pickup":
      chosen_item = room.get_item(object, adj)

      if chosen_item is not None:
        room.items.remove(chosen_item)
        items.append(chosen_item)

      open_room(room_number)
  
    # Drops an item in the room
    elif action == "drop":
      chosen_item = get_item(object, adj)
      
      if chosen_item is not None:
        items.remove(chosen_item)
        room.add_item(chosen_item)

      open_room(room_number)

    # Uses an item
    elif action == "use":
      # Make sure the player actually has the requested item
      if get_item(object, adj): 
        # Key function
        if object == "key":
          use_key(room, get_item(object, adj))
        elif object == "notebook":
           get_item(object, adj).open_page()
        elif object == "lockbox":
           get_item(object, adj).on_use()
      elif object == "lockbox" and room.get_item("lockbox", adj):
        room.get_item("lockbox", adj).on_use()
        
      input("Type any key to continue -->    ")
      open_room(room_number)

    # Door-entering protocol
    elif action == "enter" and object == "door":
      # Find the door
      chosen_door = room.get_door(adj)
  
      if chosen_door is not None:
        # Door locked message
        if chosen_door.locked == True:
          clear()
          input("The " + chosen_door.adj + " door is locked. -->    ")
          open_room(room_number)

        # Door is unlocked 
        else:
          # If the room the door is trying to take you to actually exists, open that room.
          if chosen_door.dest >= 0 and chosen_door.dest < len(rooms):
            if previous_rooms_numbers[len(previous_rooms_numbers) - 1] != room_number:
              previous_rooms_numbers.append(room_number)
            open_room(chosen_door.dest)
          else:
            open_room(room_number)
      else:
        open_room(room_number)
    
    # Debugging command to see all the rooms-DEVS ONLY
    elif action == "sudo" and adj == "open":
      open_room(int(object))

    # If command is illegible, reopen the room
    else:
      open_room(room_number)

  # If command is not any useful length, reopen the room.
  else:
    open_room(room_number)

# Determines the 3 items you must find in the Rooms
def get_target_items():
    if len(all_items) >= items_to_find:
      selections = []
      # Choose 3 items THAT ARE NOT IDENTICAL and return them in a list - NO KEYS
      for item_num in range(items_to_find):
        chosen_item = random.choice(all_items)
        while chosen_item in selections or chosen_item.name == "key":
          chosen_item = random.choice(all_items)
        selections.append(chosen_item)

      return selections
    else:
        return None

def does_player_have(item):
  adj = item.adj
  name = item.name

  matches = False

  for item in items:
    if item.name == name:
      if item.adj == adj:
        matches = True
        break
  
  return matches

# Game startup function
def start_game():
  global to_get

  # Game setup
  create_rooms()
  to_get = get_target_items()

  # Start messages
  #clear()
  print("Welcome to the Rooms. You must find: ")
  for target in to_get:
    print(" - " + target.adj + " " + target.name)
  print(help_message)
  input("Type 'start' to start.  -->   ")

  open_room(0)

start_game()



