#This one will contain a few subtopics
#Creating a variable
a = 12
b = "Danila"
print(a)
print(b)
x = 2
x = "Simon" #Now x is "Simon"
print(x)
#Casting
a = str(13)
b = int(13)
c = float(13) 
print(a, b, c)
print(type(a), type(b), type(c)) #getting the type of a variable

#Variables names
a_s = 1 #correct
as2 = 2 #correct
_a_s = 3 #correct
AS = 4 #correct
#incorrect names 2as, a-s, a s
#useful tip
MyNameAsAVariable = "Ilya"
my_name_as_a_variable = "Ilya"

#Asiigning multivariables
a, b, c = 1, 2, 3
print(a)
print(b)
print(c)
a = b = c = 1
print(a)
print(b)
print(c)
veiggies = ["cucumber", "tomato", "potato"]
x, y, z = veiggies
print(x)
print(y)
print(z)
#Output as variables
x = "C++"
y = "is"
z = "good"
print(x, y, z)
x = "I "
y = "like "
z = "eating"
print(x + y + z)
x, y = 5, 6
print(x + y)
#Global variables
x = "great" #global var

def myfunc():
  x = "oustanding" #local var (in function)
  print("Python is " + x)

myfunc()

print("Python is " + x)

def myfunc2():
  global x #we can use global to make our local var global
  x = "good"

myfunc2()

print("Python is " + x)
#also we can change our previous global variable with local var in function
