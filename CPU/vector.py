import os

os.environ["MKL_NUM_THREADS"] = "4" 
os.environ["NUMEXPR_NUM_THREADS"] = "4" 
os.environ["OMP_NUM_THREADS"] = "4"

import numpy as np
import time
import multiprocessing as mp
import win32api, win32con, win32process


def setaffinity(affinity):
    pid  = win32api.GetCurrentProcessId()
    mask = affinity # core 7
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
    win32process.SetProcessAffinityMask(handle, mask)

class SingleThread:
    
    
    def FP16(queue):
        setaffinity(1)
       

        size = int(2048)
        dtype = np.float16

        A = np.random.rand(size, size).astype(dtype)
        B = np.random.rand(size, size).astype(dtype)

        t0 = time.time()
        reps = 1
        for ii in range(reps):
            C = np.dot(A, B)
        t1 = time.time()

        FLOPS = reps * 2 * size ** 3

        queue.put('%.2f GFLOP/s' % float(FLOPS / (1000 ** 3) / (t1 - t0)))
    def FP32(queue):
        setaffinity(1)
       

        size = int(2048)
        dtype = np.float32

        A = np.random.rand(size, size).astype(dtype)
        B = np.random.rand(size, size).astype(dtype)

        t0 = time.time()
        reps = 1
        for ii in range(reps):
            C = np.dot(A, B)
        t1 = time.time()

        FLOPS = reps * 2 * size ** 3

        queue.put('%.2f GFLOP/s' % float(FLOPS / (1000 ** 3) / (t1 - t0)))

    def FP64(queue):
        setaffinity(1)
       

        size = int(2048)
        dtype = np.float64

        A = np.random.rand(size, size).astype(dtype)
        B = np.random.rand(size, size).astype(dtype)

        t0 = time.time()
        reps = 1
        
        for ii in range(reps):
            C = np.dot(A, B)
        t1 = time.time()

        FLOPS = reps * 2 * size ** 3

        queue.put('%.2f GFLOP/s' % float(FLOPS / (1000 ** 3) / (t1 - t0)))

    def INT16(queue):
        setaffinity(1)
       

        size = int(2048)
        dtype = np.int16

        A = np.random.rand(size, size).astype(dtype)
        B = np.random.rand(size, size).astype(dtype)

        t0 = time.time()
        reps = 1
        
        for ii in range(reps):
            C = np.dot(A, B)
        t1 = time.time()

        FLOPS = reps * 2 * size ** 3

        queue.put('%.2f GIOPS/s' % float(FLOPS / (1000 ** 3) / (t1 - t0)))
    def INT32(queue):
        setaffinity(1)
       

        size = int(2048)
        dtype = np.int32

        A = np.random.rand(size, size).astype(dtype)
        B = np.random.rand(size, size).astype(dtype)

        t0 = time.time()
        reps = 1
        
        for ii in range(reps):
            C = np.dot(A, B)
        t1 = time.time()

        FLOPS = reps * 2 * size ** 3

        queue.put('%.2f GIOPS/s' % float(FLOPS / (1000 ** 3) / (t1 - t0)))
    def INT64(queue):
        setaffinity(1)
       

        size = int(2048)
        dtype = np.int64

        A = np.random.rand(size, size).astype(dtype)
        B = np.random.rand(size, size).astype(dtype)

        t0 = time.time()
        reps = 1
        
        for ii in range(reps):
            C = np.dot(A, B)
        t1 = time.time()

        FLOPS = reps * 2 * size ** 3

        queue.put('%.2f GIOPS/s' % float(FLOPS / (1000 ** 3) / (t1 - t0)))
class MultiThread:

    pid  = win32api.GetCurrentProcessId()

    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
    global originalaffinity
    originalaffinity = win32process.GetProcessAffinityMask(handle)[1]

    
    def FP16(queue):

        print(originalaffinity)
        setaffinity(int(originalaffinity))
       

        size = int(2048)
        dtype = np.float16

        A = np.random.rand(size, size).astype(dtype)
        B = np.random.rand(size, size).astype(dtype)

        t0 = time.time()
        reps = 1
        for ii in range(reps):
            C = np.dot(A, B)
        t1 = time.time()

        FLOPS = reps * 2 * size ** 3

        queue.put('%.2f GFLOP/s' % float(FLOPS / (1000 ** 3) / (t1 - t0)))
    def FP32(queue):
        setaffinity(originalaffinity)
       

        size = int(2048)
        dtype = np.float32

        A = np.random.rand(size, size).astype(dtype)
        B = np.random.rand(size, size).astype(dtype)

        t0 = time.time()
        reps = 10
        for ii in range(reps):
            C = np.dot(A, B)
        t1 = time.time()

        FLOPS = reps * 2 * size ** 3

        queue.put('%.2f GFLOP/s' % float(FLOPS / (1000 ** 3) / (t1 - t0)))

    def FP64(queue):
        setaffinity(originalaffinity)
       

        size = int(2048)
        dtype = np.float64

        A = np.random.rand(size, size).astype(dtype)
        B = np.random.rand(size, size).astype(dtype)

        t0 = time.time()
        reps = 10
        
        for ii in range(reps):
            C = np.dot(A, B)
        t1 = time.time()

        FLOPS = reps * 2 * size ** 3

        queue.put('%.2f GFLOP/s' % float(FLOPS / (1000 ** 3) / (t1 - t0)))










