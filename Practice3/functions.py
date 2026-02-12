# A function is a block of code which only runs when it is called.
def my_function():
    print("hello ma friend!")

my_function()

# call multiple times
my_function()
my_function()
my_function()

# functions substitute repetetive code like this
temp1 = 34
celsius1 = (temp1 - 32) * 5 / 9
print(celsius1)

temp2 = 43
celsius2 = (temp2 - 32) * 5 / 9
print(celsius2)

temp3 = 74
celsius3 = (temp3 - 32) * 5 / 9
print(celsius3)

# instead use

def fahrenheit_to_celsius(fahrenheit):
  return (fahrenheit - 32) * 5 / 9

print(fahrenheit_to_celsius(34))
print(fahrenheit_to_celsius(43))
print(fahrenheit_to_celsius(74))

# func that returns a value
def textfunction():
   return "Function"
message = textfunction()
print(message)
print(textfunction())

#------------------------------------------------------------------------

# Arguments
def func(name): #name is a parameter
   print("Hello " + name)

func("Ilya") # "Ilya" is an argument

# if your function expects 2 arg, you must call it with exactly 2 arg
def two_arg_func(name, age):
   print(f"{name} is {age} years old")

two_arg_func("Ilya", 18)
# You can assign default values to parameters. If the function is called without an argument, it uses the default value:
def def_func(name = "Ilya"):
   print(f"Hello, {name}")

def_func() # no arg, - takes def para "Ilya"
def_func("Stepa") # arg, name = "Stepa"

#key = value syntax
def animals_func(animal, name):
   print(f"I have a {animal}. Her/his name is {name}")

animals_func(animal = "Cat", name = "Kiki")

#arguments without using keywords - Positional Arguments
#order matters

def n_animal_f(animal, name):
   print(f"My {animal}'s name is {name}")

n_animal_f("Bear", "Stepka")
n_animal_f("Stepka", "Bear") # incorrect order

# mixed

n_animal_f("Bear", name = "Stepa")

# Different data types
def my_veggies(veggies): # list
  for veggies in veggies:
    print(veggies)

maveggies = ["tomato", "cucumber", "potato"]
my_veggies(maveggies)

def my_function1(person): # dictionary
  print("Name:", person["name"])
  print("Age:", person["age"])

my_person = {"name": "Emil", "age": 25}
my_function1(my_person)

# return values
def mi_math(x, y):
  return x + y

result = mi_math(6, 7)
print(result)

#Positional-Only Arguments
def miname(name, /): #, / is used
  print("Hello", name)

miname("Ilya")

#Keyword-Only Arguments
def miname2(*, name): #*, is used
  print("Hello", name)

miname2(name = "Ilya")

#-------------------------------------------------------------------------
#Python *args and **kwargs
#*args and **kwargs allow functions to accept a unknown number of arguments

def my_kids(*kids):
#*args parameter allows a function to accept 
# any number of positional arguments
  print("The youngest child is " + kids[2])

my_kids("Ilya", "Dema", "Stepa")
# inside the function args becomes a tuple

def mykids2(*kids):
   print(f"Type: {type(kids)}")
   print("First argument:", kids[0])
   print("Second argument:", kids[1])
   print("All arguments:", kids)

mykids2("Ilya", "Dema", "Stepa" )

def greetings_func(greeting, *names):
   for name in names:
      print(f"{greeting} {name}")

greetings_func("hello", "Ilya", "Dema", "Stepa")

# finding the minimum value
def min_number(*numbers):
   if len(numbers) == 0: return None
   min_num = numbers[0]
   for number in numbers:
      if number < min_num:
         min_num = number
   return min_num
values = list(map(int, input().split()))
print(min_number(*values))

#**kwargs parameter allows a function to accept 
# any number of keyword arguments
def mkid(**kid):
  print("His last name is " + kid["lname"])

#the function will receive 
#a dictionary of arguments and can access the items accordingly

mkid(fname = "Ilya", lname = "Pak")

def kwargi(**myvar):
  print("Type:", type(myvar))
  print("Name:", myvar["name"])
  print("Age:", myvar["age"])
  print("All data:", myvar)

kwargi(name = "Ilya", age = 18, city = "Almaty")

# If u want to combine default parameters with kwargs
# Just know regular parameters must come before **kwargs

#! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! 
# Combining *args **kwargs
# THE ORDER
"""
1. regular paramters
2. *args
3. **kwargs
"""

def comb(title, *args, **kwargs):
  print("Title:", title)
  print("Positional arguments:", args)
  print("Keyword arguments:", kwargs)

comb("User Info", "Ilya", "Dema", age = 18, city = "Tokyo")
#reg = "User Info"
#*args(pos arg) = "Ilya", "Dema"
#**kwargs(keyword arg) = age = 18, city = "Tokyo"

# If you have values stored in a list
# you can use * to unpack them into individual arguments:
def mathematics(*values):
   total = 0
   for value in values:
      total += value
   return total

numbers = list(x for x in range(6))
print(mathematics(*numbers))

# If you have values stored in a dictionary
# you can use ** to unpack them into keyword arguments:

def emaill(fname, lname):
  print("Hi", fname, lname)

person = {"fname": "Ilya", "lname": "Pak"}
emaill(**person) # Same as: emaill(fname="Ilya", lname="Pak")
