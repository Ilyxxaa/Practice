x = int(1) #immutable
x = str("hello") #immutable
x = float(2.1) #immutable
x = complex(2j)
x = list(["a", "b", "c"]) #mutable
x = tuple(("a", "b", "c")) #immutable
x = bool(True) #immutable
x = dict({"name" : "Ilya", "age" : 18}) #mutable
x = dict(name="John", age=36) #mutable
x = set(("tomato", "potato", "chili")) #mutable
x = frozenset(("tomato", "potato", "chili")) #immutable
x = bytes(2)
x = bytearray(2) #mutable
x = memoryview(bytes(2))