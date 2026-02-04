a = 2
b = 7
print(a + b) # Addition
print(a - b) # Subtraction
print(a * b) # multiplication
print(a / b) # division (returns a float)
print(a // b) # floor division (целочисленное) (returns an integer)
print(a % b) # ostatok ot deleniya
print(a ** b) # power of

# assigning values to variables
a += b
a -= b
a *= b
a /= b
a //= b
a %= b
a **= b
print(x:= 4) #x = 4; print(x)

numbers = [1,2,3,4,5]
if (count := len(numbers)) > 3:
    print(f"List has {count} elements")

# Comparison
x = 4
y = 3
if x == y:
    print("x = y")
if x != y:
    print("x is not equal to y")
# < less, > greater, <= less or equal, >= greater or equal
if 2 < x < 10:
    print("x underlie between 2 and 10")

# Logical Operators
x = 3
if x > 10 or x < 2:
    print("or returns True if one of the statements is true")
if x > 10 and x % 2 == 0:
    print("and returns True if both statements are true, otherwise false")
if not(x % 2 == 0):
    print("not reverse the result, false turns into true.")

# Identity Operators
# is operator returns True if both variables point to the same object:
x = 12
y = 12
if x is y:
    print("True")

x = [1, 2, 3]
y = [1, 2, 3]

if x is y:
    print("is")
if x == y:
    print("equal")

'''
is - Checks if both variables point to the same object in memory
== - Checks if the values of both variables are equal
'''

x = ["apple", "banana"]
y = ["apple", "banana"]
z = x

print(x is z)
print(x is y)
print(x == y)