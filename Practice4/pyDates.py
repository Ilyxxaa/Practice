# we can import a module named datetime to work with dates as date objects
import datetime

x = datetime.datetime.now()
print(x)
#The date contains year, month, day, hour, minute, second, and microsecond.
print(x.year)
print(x.day)
print(x.month)
print(x.hour)
print(x.strftime("%A")) # name of weekday

#To create a date, 
#we can use the datetime() class (constructor) of the datetime module.
x = datetime.datetime(2020,8,27)
print(x)

#The strftime() Method
print(x.strftime("%A")) #Weekday, full version (%a for short ver)
print(x.strftime("%w")) #Weekday as a number 0-6,
print(x.strftime("%d"))
print(x.strftime("%B")) #Month name, full version (%b for short ver)
print(x.strftime("%p")) #AM/PM