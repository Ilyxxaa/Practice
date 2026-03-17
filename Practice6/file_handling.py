#creating and writing in file
with open("sample.txt", "w", encoding="utf-8") as f:
    f.write("Apple\n")
    f.write("Banana\n")
    f.write("Orange\n")

#reading the file
with open("sample.txt", "r", encoding="utf-8") as f:
    content = f.read()

print(content)

#appending
with open("sample.txt", "a", encoding="utf-8") as f:
    f.write("Mango\n")

with open("sample.txt", "r", encoding="utf-8") as f:
    print(f.read())

#copying the file (shutil)
import shutil

shutil.copy("sample.txt", "backup_sample.txt")
print("file copied!")

#deleting the file
import os

file_name = "backup_sample.txt"

if os.path.exists(file_name):
    os.remove(file_name)
    print("file deleted")
else:
    print("file is not found")

