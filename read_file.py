	
import os
from os import listdir
from os.path import isfile, join

currentPath = os.getcwd() # current directory 2.7
print(currentPath)

#onlyfiles = [f for f in listdir(currentPath) 
 #               if isfile(join(currentPath, f))
 #               ]
#print(onlyfiles)


files = []
for i in listdir(currentPath):
    if i.endswith('.csv'):
        files.append(join(currentPath, i))
print(files)


f = open(files[0], "r")

for x in f:
    print(x)
    print("***    ***")
