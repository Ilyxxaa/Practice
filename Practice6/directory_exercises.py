import os
#creating
os.makedirs("test_dir/subdir1/subdir2", exist_ok=True)

#list of files and folders
files = os.listdir("test_dir")
print(files)

#finding files by their domains
for file in os.listdir("."):
    if file.endswith(".txt"):
        print(file)

#transporting the file
import shutil

shutil.move("sample.txt", "test_dir/sample.txt")

#copying to folder
shutil.copy("test_dir/sample.txt", "test_dir/subdir1/")