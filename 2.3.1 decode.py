#   decode.py 6-10-24
#   Note this will not run in the code editor and must be downloaded
from PIL import Image
import tkinter as tk
from tkinter import filedialog

CHARS_IN_A_ROW = 8
MAX_CHARS_IN_MSG = 20


# Attempt to open the image
try:
  name = filedialog.askopenfile(mode='r').name
  im = Image.open(name) 
except:  
  print("ERROR: could not find output.png. Check it exists in the directory with your python files")
  exit()

# Detect the location of the encrypted message in the image by finding the first red block
block_size = 0
gap_size = 0
upper_pixel_row = 0
left_pixel_col = 0
detected = False
gap_detected = False
end_of_line = False
rgb_im = im.convert('RGB') # <- Convert image to RGB
for i in range(0, rgb_im.height):
  for j in range(0, rgb_im.width):
    r,g,b = rgb_im.getpixel((j,i))
    if not gap_detected and r > 200 and g < 100 and b < 100: 
      if not detected:  # <- If a red block is found for the first time, set the location as the beginning of the code message
        upper_pixel_row = i 
        left_pixel_col = j
      block_size += 1 #< - Keep going until the block size is established
      detected = True
    if not end_of_line and detected and r > 200 and g > 200 and b > 200: #<- After the first white space after the block, start recording gap size until the next block is reached
      gap_detected = True
      gap_size += 1
    if gap_detected and r > 200 and g < 100 and b < 100:
      end_of_line = True
    if end_of_line and r > 200 and g > 200 and b > 200:
      break
      

print(gap_size, block_size)
# Determine the size of the encrypted area using the decoding information
msg_width = left_pixel_col + (block_size + gap_size) * CHARS_IN_A_ROW
msg_height = upper_pixel_row + (block_size + gap_size) * MAX_CHARS_IN_MSG
if (msg_height > rgb_im.height):
  msg_height =  rgb_im.height

# Create an array the length of the message and fill it with placeholder 0s
my_array = []
for letters in range(0, CHARS_IN_A_ROW*(MAX_CHARS_IN_MSG+1)):
  my_array.append(0)

# For each square that is blue in the message area, change the 0 to a 1
pos=0
for i in range(upper_pixel_row, msg_height - gap_size + 5, (block_size + gap_size)):
  mid_i = i + int(block_size/2)
  for j in range(left_pixel_col, msg_width - gap_size + 2, (block_size + gap_size)):
    mid_j = j + int(block_size/2)
    if (mid_j < msg_width and mid_i < msg_height):
      r, g, b = rgb_im.getpixel((mid_j, mid_i))
      rgb_im.putpixel((mid_j, mid_i), (0, 0, 0)) #<- Mark spots we checked
      #if r < 100 and g < 100 and b > 200:
      if r > 200 and g < 100 and b < 100:
        my_array[pos]=1
      pos = pos + 1
      

# Assemble the extracted binary info into a string
message_as_bits = ''
for bit in my_array:
  message_as_bits = message_as_bits + str(bit)

# Turn the binary info into integer values; use modulus to determine the binary place values of each letter. 
# When the right number of integer values are extracted, turn them into a character.
letter = 0
decoded = ''
for n in range(0, len(message_as_bits)):
  if n % 8 == 0:
    if letter != 0:
      decoded = decoded + chr(letter)
      letter = 0
    letter = int(message_as_bits[n]) * 128 + letter 
  elif n % 8 == 1:
    letter = int(message_as_bits[n]) * 64 + letter 
  elif n % 8 == 2:
    letter = int(message_as_bits[n]) * 32 + letter 
  elif n % 8 == 3:
    letter = int(message_as_bits[n]) * 16 + letter 
  elif n % 8 == 4:
    letter = int(message_as_bits[n]) * 8 + letter 
  elif n % 8 == 5:
    letter = int(message_as_bits[n]) * 4 + letter 
  elif n % 8 == 6:
    letter = int(message_as_bits[n]) * 2 + letter 
  elif n % 8 == 7:
    letter = int(message_as_bits[n]) * 1 + letter

# Print the decoded message
print("Decoded:", decoded)

# Crop out the code region and save it
msg_len = len(decoded) + 1
bbox = (left_pixel_col, upper_pixel_row, msg_width, upper_pixel_row+(msg_len*(block_size + gap_size)))
show_code_region = rgb_im.crop(box=bbox)
show_code_region.save("code_region.png")
show_code_region.show()
