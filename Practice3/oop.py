#Object-Oriented Programming.
#Python is an object-oriented language, allowing you to structure your code 
#using classes and objects for better organization and reusability.

# Classes and Objects
class MyClass:
    x = 5
p1 = MyClass()
print(p1.x)
del p1

# Muliple objects with the same class
p1 = MyClass()
p2 = MyClass()
p3 = MyClass()

print(p1.x)
print(p2.x)
print(p3.x)
# each object is independent

# The __init__() Method

#The __init__() method is used to assign values to object properties,
#or to perform operations that are necessary when the object is being created.
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p1 = Person("Ilya", 18)
print(f"{p1.name} {p1.age}")
# easier to create objects with initial values

#Default Values in __init__()
class Person:
  def __init__(self, name, age = 18):
    self.name = name
    self.age = age

p1 = Person("Ilya")
p2 = Person("Dema", 25)

print(p1.name, p1.age)
print(p2.name, p2.age)

#Mupltiple parameters
class Person:
  def __init__(self, name, age, city, country):
    self.name = name
    self.age = age
    self.city = city
    self.country = country

p1 = Person("Ilya", 18,  "Almaty", "Kazakhstan")

print(p1.name, p1.age, p1.city, p1.country)

class animal:
   def __init__(self, name, age):
      self.name = name
      self.age = age
   def bark(self):
      if self.name == "Dog": print(self.name + " says Woof")
      else: print(self.name + " says something")

p1 = animal("Dog", 6)
print(p1.age)
p1.bark()
p2 = animal("Cat", 7)
p2.bark()

#The self parameter is a reference to the current instance of the class.
#It is used to access properties and methods that belong to the class.
#The self parameter must be the first parameter of any method in the class.

#self parameter can be named differently f.g "myobject"
class Person:
   def __init__(object, name, age):
      object.name = name
      object.age = age
   def greetings(object):
      print(f"Hello {object.name}!")
    
p1 = Person("Ilya", 18)
p1.greetings()

#You can access any property of the class using self

class Person1:
   def __init__(self, name, age):
      self.name = name
      self.age = age
   def greetings(self):
      return f"Hello {self.name}!"
   def welcome(self):
      message = self.greetings()
      print(f"{message} Welcome to our website.")
      
p1 = Person1("Ilya", 18)
p1.welcome()

# Methods 
class Calculator:
   def __init__(self, x, y):
      self.x = x
      self.y = y

   def summ(self, a, b): # this method can accept parameters just like regular finctions
      return a * b
   
   def mult(self):
      return f"multiplication of {self.x} and {self.y} = {self.x * self.y}"
      #modify object properties using self

   def upscaler(self):
      self.x += 1
      self.y += 1
      return self.x , self.y
   #Methods can modify the properties of an object
   

calc = Calculator(4,5) #x, y = 4, 5
print(calc.summ(2,3)) #a , b = 2, 3
print(calc.mult())
print(calc.upscaler())

class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

  def greet(self):
     return f"hello {self.name}"

  def __str__(self):
    return f"{self.name} ({self.age})"
  #The __str__() method is a special method 
  #that controls what is returned when the object is printed

p1 = Person("Ilya", 18)
print(p1) # no need to call the method __str__()
print(p1.greet)

# you can delete methods and properties by using del
del Person.greet
del p1.age
"print(p1.greet) - cause an error"
" - cause an error because age no more atribute of p1"