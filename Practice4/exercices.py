#DATE
"""
#1
import datetime
from datetime import timedelta
x = datetime.datetime.now()
print(x - timedelta(days=5))
#2
print("today is:", x.date())
print("yesterday was:", x.date() - timedelta(days=1))
print("tomorrow is:", x.date() + timedelta(days=1))
#3
print(x.replace(microsecond=0))
#4
a = datetime.datetime(2020,8,28,14,50,54)
b = datetime.datetime(2021,8,28,14,50,34)
dif = a - b
totalsec = dif.days * 24 * 60 * 60
print(abs(totalsec))
"""
#--------------------------------------------------------------------------------
#generators
"""
#1
N = int(input())
print(*(x**2 for x in range(1,N+1)))
#2
n = int(input())
print(*range (0, n+1, 2),sep=",")
#3
def thrfor(n):
    for i in range(0,n+1):
        if i % 3 == 0 and i % 4 == 0:
            yield i
n = int(input())
print(*thrfor(n))
#4
def squares(a,b):
    for i in range(a,b+1):
        yield i**2
a, b = map(int, input().split())
print(*squares(a,b))
#5
def rev(n):
    for i in range(n,-1,-1):
        yield i
n = int(input())
print(*rev(n))"""
#--------------------------------------------------------------------------------
#math
"""#1
import math
degree = int(input())
print(degree * math.pi / 180)
#2
height = int(input())
upBase, lowBase = map(int, input().split())
print((upBase + lowBase) / 2 * height)
#3
sides = int(input())
length = int(input())
area = ((sides * pow(length, 2)) / (4*math.tan(math.pi / sides)))
print(int(round(area)))
#4
base = float(input())
height = float(input())
area = base * height
print(area)"""
#--------------------------------------------------------------------------------
#JSON
import json
with open("sample-data.json") as f:
    data = json.load(f)

print("Interface Status")
print("=" * 80)
print(f"{'DN':50} {'Description':20} {'Speed':7} {'MTU':6}")
print("-" * 80)

# проходим по imdata
for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]
    
    dn = attributes["dn"]
    descr = attributes["descr"]
    speed = attributes["speed"]
    mtu = attributes["mtu"]
    
    print(f"{dn:50} {descr:20} {speed:7} {mtu:6}")