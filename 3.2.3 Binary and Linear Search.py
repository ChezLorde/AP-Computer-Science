import random

file_name = "100_random_numbers.txt"
target = 16
max = 101
min = 0

# Generates a sorted list of 100 random numbers with only 1 of the target number
def generate_list()->list:
  return list(range(min, max, 1))

# Performs a linear search algorithm on a list, recording the number of comparisons.
def linear_search(list, target_num):
  comparisons = 0
  for value in list:
    comparisons += 1
    if value == target_num:
      break
  return value, comparisons

# Performs a binary search algorithm on a list, recording the number of comparisons
def binary_search(list, target_num, already_comparisons=0):
  length = len(list)

  # Find the middle of the list
  mid = (length/2).__floor__()

  comparisons = already_comparisons

  # If the target is in the greater half of the list, then split and binary search that side.
  if target_num > list[mid]:
    comparisons += 1
    new_list = list[mid:length]
    return binary_search(new_list, target_num, already_comparisons=comparisons)
  
  # If the target is in the lesser half of the list, then split and check that side
  elif target_num < list[mid]:
    comparisons += 2
    new_list = list[0:mid]
    return binary_search(new_list, target_num, already_comparisons=comparisons)
  
  # If the middle item is the target, then return the target
  elif target_num == list[mid]:
    comparisons += 3
    return list[mid], comparisons


new_list = generate_list()

lin_val, lin_comps = linear_search(new_list, target)
print("Linear Search found " + str(lin_val) + " in " + str(lin_comps) + " comparisons.")

bin_val, bin_comps = binary_search(new_list, target)
print("Binary Search found " + str(bin_val) + " in " + str(bin_comps) + " comparisons.")









    

    






