#Inheritance allows us to define a class 
#that inherits all the methods and properties from another class
class Shape: # Parent (main)
    def area(self):
        return 0

class Square(Shape): #Child (inherit properties from parent)
    def __init__(self, length):
        self.length = length
        #When you add the __init__() function
        #the child class will no longer inherit the parent's __init__() function
        #The child's __init__() function overrides the inheritance of the parent's

        #To keep the inheritance of the parent's __init__() function,
        #add a call to the parent's __init__() function
        """Class Square(Shape):
            def __init__(self, length):
                Shape.__init__(self, length)
                or
                super().__init__(self, length)"""
        # super() will make the child class inherit all the methods and properties from its parent
        # for example
    def area(self):
        return f"square area: {self.length * self.length}"

class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return f"rectangle area: {self.length * self.width}"

pi = 3.14159
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius 

    def area(self):
        return self.radius * self.radius * pi

n = int(input())
c = Circle(n)
print(f"circle area: {c.area():.2f}")
    
l, w = (x for x in input().split())
r = Rectangle(int(l) , int(w))
print(r.area()) 

n = int(input())
s = Square(n)
print(s.area())