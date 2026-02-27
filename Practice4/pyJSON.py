#JSON is a syntax for storing and exchanging data.
#JSON is text, written with JavaScript object notation.
import json
#Convert from JSON to Python
x = '{"name":"Ilya", "age":18, "city":"Almaty"}'
#parse x
y = json.loads(x)
print(y["age"])

#If you have a Python object, you can convert it into 
#a JSON string by using the json.dumps() method.
#Convert from Python to JSON
x = {"name":"Ilya", "age":18, "city":"Almaty"}
y = json.dumps(x)
print(y)
#Convert a Python object containing all the legal data types:
x = {
  "name": "Ilya",
  "age": 18,
  "married": False,
  "divorced": True,
  "friends": ("Dema","Alim"),
  "ability to fly": None,
  "cars": [
    {"model": "BMW 230", "mpg": 27.5},
    {"model": "Ford Edge", "mpg": 24.1}
  ]
}

print(json.dumps(x))
#The json.dumps() method has parameters to make it easier to read the result:
#Use the indent parameter to define the numbers of indents:
#Use the separators parameter to change the default separator:
#default value is (", ", ": ")
print(json.dumps(x, indent=4, separators=(". ", " = ")))
#Use the sort_keys parameter to specify if the result should be sorted or not:
print(json.dumps(x, indent=4, sort_keys=True))