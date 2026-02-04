# print the sum from 1 to 6 (6 is not included)
n = 1
sum = 0
while n < 6:
    sum += n
    n += 1
print(sum)

# Print i as long as i is less than 4:
i = 1
while i < 4:
  print(i)
  i += 1

# reverse counting until 5
a = int(input())
while a != 0:
    if a == 5:
        break
    print(a)
    a -= 1

# reverse counting without 5
b = int(input()) + 1
while b != 0:
    b -= 1
    if b == 5:
        continue
    print(b)

# else also works with while loop
c = int(input())
while c != 0:
    if c == 5:
        break
    print(c)
    c -= 1
else:
    print("you found 5")