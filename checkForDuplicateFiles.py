import os
import hashlib
from collections import Counter

drives = [
    r""
]

filesChecked = {}

print("Scanning drives...")
for drive in drives:
    print(f"Checking {drive}")
    for root, subFolders, files in os.walk(drive):
        for file in files:
            if file in filesChecked:
                array = filesChecked[file]
                array.append(f"{root}/{file}")
                filesChecked[file] = array
            else:
                filesChecked[file] = [f"{root}/{file}"]

print("""Done scanning drives.
Saving progress...""")

with open("filesCheckedDict.txt","w") as file:
    file.write(str(filesChecked))

print("""Saved.
Scanning files with duplicate names...""")

duplicates = {}
hashes = {}
for entry in filesChecked:
    if len(filesChecked[entry]) > 1:
        for path in filesChecked[entry]:
            with open(path, "rb") as f:
                digest = hashlib.file_digest(f, "sha256")
            hashes[path] = digest.hexdigest()
count_dict = Counter(hashes.values())
for key,value in hashes.items():
    if count_dict[value] > 1:
        duplicates[key] = value

print("Saving progress...")

with open("duplicatesDict.txt","w") as file:
    file.write(str(duplicates))

print("""Saved.
Sorting into duplicated files...""")

sorted_duplicates = {}
for path,fileHash in duplicates.items():
    if fileHash in sorted_duplicates:
        continue
    hashDuplicate = [path]
    for subPath,subFileHash in duplicates.items():
        if subPath != path and fileHash == subFileHash:
            hashDuplicate.append(subPath)
    sorted_duplicates[fileHash] = hashDuplicate

print("""Done.
Writing results to file...""")

file_contents = """"""
for key,value in sorted_duplicates.items():
    print("\n"+str(key)+"\n==============================\n"+str('\n'.join(value)))
    file_contents += str(key)+f"\n==============================\n"+str('\n'.join(value))+"\n\n"

with open("Duplicate Files.txt",'w') as file:
    file.write(file_contents.strip())

print("\nWriten to Duplicate Files.txt")
