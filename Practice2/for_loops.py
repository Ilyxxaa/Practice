# Print each fruit in a fruit list:
fruits = ["watermelon", "banana", "orange"]
for x in fruits:
  print(x)

# prints letters from this word
for x in "banana":
  print(x)

# prints veggies except tomato
veggies = ["cucumber", "tomato", "potato"]
for x in veggies:
  if x == "tomato":
    break
  print(x)

for x in range(4): # values 0 to 3.
  print(x)
else:
  print("DONE!")

for x in range(4): # values 0 to 3.
  if x == 2: break
  print(x)
else: # as 2 is in the range, break statement will stop else block
  print("DONE!")
# prints 0, 1 

for x in range(2, 12, 3):
  print(x)
# values from 2 to 11 with step 3
# 2, 5, 8, 11

# nesting loop
adj = ["tasty", "big", "sweet"]
fruits = ["melon", "pineapple", "cherry"]

for x in adj:
  for y in fruits:
    print(x, y)

# for loops cannot be empty, but if you for some reason have a for loop with no content, put in the pass statement to avoid getting an error.
for x in []:
  pass