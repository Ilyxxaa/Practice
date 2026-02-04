a = 120
b = 300
# identation is mandatory 
if a > 0:
    print("a is positive")

# if and else and multiple statments
age = 17
if age >= 18:
    print("You are an adult"); print("You have full legal rights")
else:
    print("You are underage"); print("You do not have full legal rights")

# you can use booleans too
is_ok = True
if is_ok:
    print("Its okay)")

# with boolean operators
year = 2024
if year % 4 == 0 and year % 400 == 0:
    print(f"{year} is leap")

# "if the previous conditions were not true, then try this condition"
# elif

a = 12
b = 12
if b > a:
  print("b is greater than a")
elif a == b:
  print("a and b are equal")

gpa = 3.6
if gpa >= 4:
   print("A")
elif gpa >= 3.67:
   print("A-")
elif gpa >= 3.33:
   print("B+")
elif gpa >= 3.0:
   print("B")
elif gpa >= 2.67:
   print("B-")

day = 5
if day == 1:
  print("Monday")
elif day == 2:
  print("Tuesday")
elif day == 3:
  print("Wednesday")
elif day == 4:
  print("Thursday")
elif day == 5:
  print("Friday")
elif day == 6:
  print("Saturday")
elif day == 7:
  print("Sunday")

# all together
a = 123
b = 45
if b > a:
  print("b is greater than a")
elif a == b:
  print("a and b are equal")
else:
  print("a is greater than b")
# else can be used without the elif
# else must be last and after if or elif
# elif must be after if

mood_perc = 55
if mood_perc >= 85:
   print("Perfect mood")
elif mood_perc >= 65:
   print("Normal mood")
elif mood_perc >= 50:
   print("Mood is kinda okay")
else:
   print("Mood is terrible")

# shorthands

a, b = 2, 30
if a < b: print("b is bigger than a")
print("a is bigger than b") if a > b else print("b is bigger than a")
# One if --- if: print()
# If and Else --- print() if else print()

bigger = a if a > b else b #assigning value using shorthands
print(bigger)

print("a") if a > b else print("b") if b > a else print("they are equal")
# mult conditions in one line
# print() if cond else print() if cond else print()

# nested if
x = input()
if x.isdigit():
   print("okay, its a number")
   x = int(x)
   if x > 0:
      print("and positive")
      if x % 2 == 0:
         print("and even")
      else:
         print("and odd")
   elif x < 0:
      print("and negative")
      if x % 2 == 0:
         print("and even")
      else:
         print("and odd")
   else:
      print("and its equal to 0")
else:
   print("not a number")

points = 90
plus_bonus = True
if points >= 90 and plus_bonus:
   print("Im happy")

# pass
email = "aslasd@gmail.com"
if len(email) > 0:
   print("Enter a password")
else:
   pass #add later

value = 49

if value < 0:
  print("Negative value")
elif value == 0:
  pass # Zero case - no action needed
else:
  print("Positive value")