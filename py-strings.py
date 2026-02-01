#Multiline strings
a = """qwerty[apsod[pas
als;kd;lask]]fdgkljdf
alskfjhlksjdfpo"""
print(a)

x = "Hello! How are you doing?"
print(x[2])
print(x[4])

#String loop
for x in "Hello":
    print(x)
for x in "How are you?":
    print(x)
#Length
a = "myname"
print(len(a)) #6
a = "mynameisabitlonger"
print(len(a)) #18

name = "Ilya Park"
if "Ilya" in name:
    print("True")
if "Park" in name:
    print("True")
if "Stepa" not in name:
    print("Stepa is not my name")
if "Tyan" not in name:
    print("Tyan is not my second name")

# Slicing
# a[begining:end:step(or reverse if negative)]
b = "Hello, World!"
print(b[2:5]) #from index 2 to 5 (5 is not included)
b = "qweerty"
print(b[1:6])
print(b[:6]) #from the start
print(b[2:]) #from 2 to the end
print(b[::-1]) #reverse

b = "Hello, World!"
print(b[-6:-3]) #from reversed position to reversed pos(not included)

# Modify Strings
b = "Hello ma bro!"
print(b.upper()) #making and printing uppercase letters
print(b.lower()) #making and printing lowercase letter
a = "      to much spaces          "
print(a.strip()) #removes all the spaces from the begining to the end 
print(b.replace("ma bro", "Hello")) #replace "ma bro" to "Hello"
print(b.split()) #splits the string into substrings if its find inctances of the separator

#Concatenate strings
a = "Hi"
b = "Mate"
c = a + " " + b
print(c)

# Formating string
age = 18
text = f"My age is {age}" #using variable without errors
print(text) 

name = "Ilya"
print(f"My name is {name}")

price = 13
txt = f"The price is {price:.2f} dollars" #:.2f adding fixed point number with 2 decimals
print(txt)
print(f"the price is {12*2} dollars")

txt = "We are the so-called \"Vikings\" from the north." #\" message \" allows to use double quotes
print(txt)
print("Hello\nworld") #\n adds a new line

#useful string methods
a = "this is a word"
if a.isalpha():
    print("all the characters are in the alphabet")

if a.isdigit():
    print("all the characters are digits")

if a.islower():
    print("all the characters are lowercase")

if a.isupper():
    print("all the characters are uppercase")

print(a.count("s")) #Returns the number of times "s" occurs in a string 
print(a.find("s")) #returns an index of the first occuring "s" (substring), if not returns -1