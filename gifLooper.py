import cv2
import sys
import numpy as np
from os import listdir
from os.path import isfile, join
import threading
from queue import Queue
import multiprocessing
import time
import math

num_fetch_threads = 2
queue = Queue(10)
seq = []
images = []
files = []
path =""
minErrorMSE = 50
def mse(imageA, imageB):

    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    return err

def mean(image):
        return image.mean()

def prepareData():

    for i in range(0, len(files)):
        images.append(cv2.imread(path + "/" + files[i]))
                
        

def best(start, originalName):
    compName = ""
    original = images[start]
    print(str(start) + " " + str(len(files)) + " " + str(100*start/(len(files))))
    for j in range(start+30, len(files)):
        comp = images[j]
            
        mseValue = mse(original, comp)
        #print(mseValue)
        compName = path + "/" + files[j]
        diff = abs(start - j)
        if mseValue < minErrorMSE:
            print((originalName ,compName , diff, float(mseValue)))
            seq.append((originalName ,compName , diff, float(mseValue)))

def sequences():
        
    for i  in range(0, len(images) - 1):
        originalName = path +"/"+ files[i]
        queue.put((i, originalName), True)
                
    return seq

def createThreads(numberThreads = multiprocessing.cpu_count() - 1):
    for i in range(numberThreads):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()

def worker():
    while True:
        item = queue.get()
        best(*item)
        queue.task_done()

def readFile(path):
    with open(path, "r") as f:
        myListofTuples = [tuple(line.split(',')) for line in inputFile.readlines()]
        print(myListofTuples)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        startTime = time.time()
        createThreads()
        path = sys.argv[1]
        files = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith(".png")]
        file = open("gif_" + path + ".txt", "w")
        prepareData()
        s = sequences()
        queue.join()
        print("Time " + str(math.ceil(time.time() - startTime)) +"s")
        for t in s:
            file.write(str(t)+"\n")
                
        file.close()

                

