import string
import random

lowercase_letters = string.ascii_lowercase
uppercase_letters = string.ascii_uppercase
numbers = string.digits
special_characters = string.punctuation

characters = [lowercase_letters, uppercase_letters, numbers, special_characters]

def get_random_character(type):
  type_index = random.randint(0, len(type) - 1)
  new_character = type[type_index]
  return new_character

def generate_password(length):

  if length >= len(characters):
    password = ""

    valid = False

    while not valid:

      valid = True
      password = ""
      checks = {"a":False, "A":False, "0":False, "!":False}

      for index in range(length):

        type = random.choice(characters)
        new_character = get_random_character(type)

        password = password + new_character

        checks.__setitem__(type[0], True)

      for requirement in checks:
        if checks.get(requirement) == False:
          valid = False
          break

    return password
  
  else:
    return "Please select a longer length"
  








length = int(input("Enter password length:   "))
print(generate_password(length))
