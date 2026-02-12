# A lambda function is a small anonymous function that u can write in a one sentence
# can take any number of arguments, but can only have one expression
# Syntax lambda arguments : expression
x = lambda a : a + 10
print(x(5))

y = lambda a,b : a * b
print(y(4,5))

x = lambda a, b, c : a + b + c
print(x(6, 7, -2))

# In function
def multiplyer(n):
    return lambda a: a * n
doubler = multiplyer(2)
trripler = multiplyer(3) # 3 as n
print(trripler(11)) # 11 as a
print(doubler(11))

# Lambda with map()
"""numbers = list(map(int, input().split()))"""
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x : x * 2, numbers))
doubled1 = list(x*2 for x in numbers) # same action
print(*doubled)

# The filter() function creates a list of items for which a function returns True:
values = [1, 2, 3, 4, 5, 6]
even_numbers = list(filter(lambda x : x % 2 == 0, values))
print(*even_numbers)

# With sorted()
students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key = lambda x: x[1])
print(sorted_students)

words = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(words, key = lambda x : len(x))
reverse_words = sorted_words[::-1] # slicing to reverse
print(sorted_words) # from shortest to longest
print(reverse_words) # reversed
# sortiong strings by length
