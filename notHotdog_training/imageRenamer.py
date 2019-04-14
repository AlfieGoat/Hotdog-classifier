import os
from os import rename, listdir
import random
path = 'C:/Users/alfre/Desktop/notHotdog/nothotdog/'
counter=0
fname = listdir(path)
print(fname)
for j in fname:
    if(".jpg" not in j):
        os.remove(path+j)
fname = listdir(path)
for i in fname:
    rename((path+str(i)),(path+str(counter)+str(random.randint(10000,901247091247017240))+".jpg"))
    counter+=1
counter=0
fname = listdir(path)
for i in fname:
    rename((path+str(i)),(path+str(counter)+".jpg"))
    counter+=1


#+str(random.randint(10000,901247091247017240)) use to randomize first