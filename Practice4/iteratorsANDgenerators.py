#  ITERATORS
# an iterator is an object that contains a countable number of values
# iterator is an object which implements the iterator protocol,
# which consist of the methods __iter__() and __next__().

# Lists, tuples, dictionaries, and sets are all iterable objects. 
# They are iterable containers which you can get an iterator from.
mytuple = ("apple", "watermelon", "banana")
myit = iter(mytuple)

print(next(myit)) 
print(next(myit))
print(next(myit))

mystr = "Ilya"
myit = iter(mystr)

print(next(myit)) 
print(next(myit))
print(next(myit))
print(next(myit)) 

# Looping
mytuple = ("apple", "watermelon", "banana")
for i in mytuple:
    print(i)

mystr = "Ilya"
for x in mystr:
    print(x)

# x OOP
# To create an object/class as an iterator you have to implement the methods
#  __iter__() and __next__() to your object.

class MyNumbers:
    def __iter__(self):
    # must always return the iterator object itself.
        self.a = 1
        return self
    
    def __next__(self):
    # must return the next item in the sequence.
        x = self.a
        self.a += 1
        return x
    
myclass = MyNumbers()
myiter = iter(myclass)

print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))

# Stopping
# stop after 20 iterations
class MyNumbers:
    def __iter__(self):
        self.a = 1
        return self
    
    def __next__(self):
        if self.a <= 20:
            x = self.a
            self.a += 1
            return x
        else: raise StopIteration
    
myclass = MyNumbers()
for x in myclass:
    print(x)

#-------------------------------------------------------------------------------
# GENERATORS
# use yield to produce a series of results over time

# square func with yield
def square(n):
    for x in range(n+1):
        yield x**2
    
sqr = square(5)
print(*sqr)

# list compr
#(expression for item in iterable)
sq = (x**2 for x in range(1,6))
print(*sq)