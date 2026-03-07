#1
import re
s = input()
x = re.findall(r"ab*", s)
print(*x)
#2
s = input()
x = re.findall(r"ab{2,3}", s)
print(*x)
#3
s = input()
x = re.findall(r"[a-z]+_[a-z]+", s)
print(*x)
#4
s = input()
x = re.findall(r"[A-Z]{1}[a-z]+", s)
print(*x)
#5
s = input()
x = re.findall(r"a.*b\b", s)
print(*x)
#6
s = input()
x = re.sub(r"\.|\s|,", "|", s)
print(x)
#7
s = input()
x = re.sub(r'_([a-zA-Z0-9]+)', lambda m: m.group(1).capitalize(), s)
print(x)
#8
s = input()
x = re.split(r"(?=[A-Z])", s)
print(x)
#9
s = input()
res = re.sub(r"([A-Z])", r" \1", s)
print(res.strip())
#10
text = input()
res = re.sub(r"([A-Z])", r"_\1", text).lower()
print(res)
