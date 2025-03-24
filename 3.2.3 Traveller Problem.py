
cities = {
  "a":{"b":7, "c":3, "e":12, "d":11},
  "b":{"a":7, "c":9, "e":8, "d":4},
  "c":{"a":3, "b":9, "d":5, "e":6},
  "d":{"a":11, "b":4, "c":5, "e":10},
  "e":{"a":12, "b":8, "c":6, "d":10}
}

def make_string(set1:set):
  empty = ""
  for item in set1:
    empty += item
  return empty

def find_min(list1:list):
  min_num = 1000
  min_index = 0
  for index in range(len(list1)):
    if list1[index] < min_num:
      min_num = list1[index]
      min_index = index
  return min_num,min_index


routes = []
costs = []
start_city = "a"

def inv_options(city:str, curr_cost:int, gone_to:str):
  global routes
  global costs

  gone_to += city
  options = cities[city]

  # If we have already gone to every city, then return to City A and return the total costs and city order.
  if len(gone_to) == len(cities):
    gone_to += start_city
    new_cost = curr_cost + cities[start_city][city]
    routes.append(gone_to)
    costs.append(new_cost)
  else:
    # Investigate all routes that lead to a new location
    for next_city in options:
      if not next_city in gone_to: #<- Not already been
        new_cost = curr_cost + cities[city][next_city]
        inv_options(next_city, new_cost, gone_to)

inv_options("a", 0, "")

print("Number of Routes: " + str(len(routes)))
for index in range(len(routes)):
  print(make_string(routes[index]) + " " + str(costs[index]))

min_cost, min_index = find_min(costs)
print("Best Route: " + routes[min_index] + " Cost: " + str(min_cost))


