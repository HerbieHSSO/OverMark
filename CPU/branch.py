
import time
import multiprocessing as mp
import win32api, win32con, win32process
import random



def SingleThread():
    pid  = win32api.GetCurrentProcessId()
    mask = 1 # core 7
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
    win32process.SetProcessAffinityMask(handle, mask)

    accuracy = 0
    test = 0
    
    percent = 100
    while percent > 0:
        data = []
        y = 0

        for i in range(0, 100000):
            data.append(random.randint(1, 100000))
        start = time.time()

        for j in range(0,100000):
            if data[j] >= 50000:
                y = y + data[j]

        end = time.time()
        diff = end - start
        #print("Unsorted Time:", diff)

        for k in range(0, 100000):
            data.append(random.randint(1,100000))
        data.sort()

        start = time.time()

        for l in range(0,100000):
            if data[l] >= 50000:
                y = y + data[l]
        end = time.time()
        diff1 = end - start
        #print("Sorted time:", diff1)
        
        

        if diff > diff1:
            None
        else:
            accuracy = accuracy + 1
        percent = percent - 1
    
    print(accuracy)
   
