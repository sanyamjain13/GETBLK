from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager
from Buffer import Buffer
from SleepQueue import SleepQueue
import multiprocessing, os, random
import time, sys
import BufferManagement
import BufferRelease

def performOperation(blockNo, bufferHead, lock):
    '''
    Random Operation
    1 : Normal read operation
    2 : Write operation which marks it for delayed write
    3 : Mark buffer invalid to simulate error
    '''


    #Because after bread every buffer is valid
    bufferHead.setValidBit(blockNo)
    
    randOperation = random.randint(1,3)
    if randOperation == 1:
        print("Process",os.getpid(), ": Read buffer with blockNo", blockNo)
        bufferHead.setValidBit(blockNo)
        
    elif randOperation == 2:
        print("Process",os.getpid(), ": Delayed write buffer with blockNo", blockNo)
        bufferHead.setDelayedWriteBit(blockNo)

    else:
        print("Process",os.getpid(), ": Error while reading buffer with", blockNo,". Marking buffer content as invalid")
        bufferHead.clearValidBit(blockNo)

    

def processWork(i,bufferHead, sleepQueue, lock):
	
    startStr = "Process {} :".format(os.getpid())
    sys.stdout = open("file"+str(i),'w')
    print(startStr, "is running...")

    blockNo = random.randint(1, 32)
    print(startStr, "Wants blockNo", blockNo)
    
    lockedBuffer = BufferManagement.getBlk(blockNo, bufferHead, sleepQueue, lock)
    lockedBuffer.setValidStatus(True)
    
    print(startStr, "Acquired blockNo", lockedBuffer.getBlockNum())
    performOperation(blockNo, bufferHead, lock)

    lock.acquire()
    bufferHead.printHashQ()
    bufferHead.printFreeList()
    sleepQueue.printSQ()
    lock.release()
    
    time.sleep(5)
    
    BufferRelease.brelse(lockedBuffer, bufferHead, lock, sleepQueue)
    
    print(startStr, 'Finished execution...')


if __name__ == '__main__':
    BaseManager.register('Buffer', Buffer)
    BaseManager.register('SleepQueue', SleepQueue)
    BaseManager.register('BufferHeader')
    lock = multiprocessing.Lock()

    manager = BaseManager()
    manager.start()

    buffer = manager.Buffer()
    sleepQueue = manager.SleepQueue()

    buffer.printFreeList()


    NO_OF_PROCESSES = 3

    processes = []
    for i in range(NO_OF_PROCESSES):
        p = Process(target=processWork, args=[i,buffer, sleepQueue, lock])
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
        