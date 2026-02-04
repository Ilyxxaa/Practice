print(7 > 4)
print(6 == 9)
print(11 < 34)
a = 12
b = 6
if a > b:
    print("A is bigger than b")
else:
    print("B is bigger than a")
print(bool("Hi"))
print(bool(15))
print(bool(a))
print(bool(b))

# Any number is True, except 0
# Any str is True, except empty str
# Any list, tuple, set, and dictionary are True, except empty ones.

print(bool("abc"))
print(bool(123))
print(bool(["apple", "cherry", "banana"]))

print(bool(False))
print(bool(None))
print(bool(0))
print(bool(""))
print(bool(()))
print(bool([]))
print(bool({}))

def myFunction() :
  return True

print(myFunction())

def myFunction() :
  return True

if myFunction():
  print("YES!")
else:
  print("NO!")

x = "Hello"
print(isinstance(x, str))
# isinstnce func determine if an object is of a certain data type