#map()
numbers = [1, 2, 3, 4]

squared = list(map(lambda x: x**2, numbers))
print(squared)  # [1, 4, 9, 16]

#filter()
numbers = [1, 2, 3, 4, 5, 6]

even = list(filter(lambda x: x % 2 == 0, numbers))
print(even)  # [2, 4, 6]

#reduce()
from functools import reduce

numbers = [1, 2, 3, 4]

total = reduce(lambda x, y: x + y, numbers)
print(total)  # 10

#enumerate()
fruits = ["apple", "banana", "orange"]

for index, value in enumerate(fruits):
    print(index, value)

#zip()
names = ["Ivan", "Anna"]
ages = [25, 30]

for name, age in zip(names, ages):
    print(name, age)

x = 8

print(type(x))          # class 'int'
print(isinstance(x, int))  # True

a = "123"
b = int(a)

print(b + 1)  # 124