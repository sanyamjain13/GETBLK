import os, signal, random
from Buffer import Buffer



def brelse(buffer, bufferHead, lock, sleepQueue):

    '''
    Implementation of BRELSE algorithm.
    Buffer is released after kernel on behalf of the process finishes using it.
    '''

    lock.acquire()

    if buffer==None:
        print("\nUnexpected behaviour")
        return
    
    if bufferHead.checkValidBit(buffer.getBlockNum()):
        print("Adding at the end")
        bufferHead.addToFreeList(buffer, False)
    else:
        print("Adding at the front")
        bufferHead.addToFreeList(buffer, True)

    bufferHead.clearLockedBit(buffer.getBlockNum())
    print("Process ",os.getpid(),": Unlocked buffer ",buffer.getBlockNum(),"            Lock status:",buffer.getLockedStatus())
    bufferHead.printFreeList()
    wakeUp(buffer.getBlockNum(),lock,sleepQueue)
    
    lock.release()



def wakeUp(blockNo, lock, sleepQueue):

    '''
    Wakes up a process randomly, waiting for specific buffer or any buffer.
	'''

    toss = random.randint(1, 10)
    
    if toss % 2 == 0:
        anyPid = sleepQueue.getRandomProcess(-1)
        if anyPid != None:
            print("Process waiting for any buffer woke up")
            wakeUpHelper(-1, lock, sleepQueue, anyPid)
            sleepQueue.printSQ()
            return
    
    particularPid = sleepQueue.getRandomProcess(blockNo)

    if particularPid != None:
        print("Process waiting for specific buffer woke up")
        wakeUpHelper(blockNo, lock, sleepQueue, particularPid)
        sleepQueue.printSQ()
        return
    else:
        anyPid = sleepQueue.getRandomProcess(-1)
        if anyPid != None:
            print("Process waiting for any buffer woke up")
            wakeUpHelper(-1, lock, sleepQueue, anyPid)
            return
    print("No process to wake up")
    sleepQueue.printSQ()


def wakeUpHelper(blockNo, lock, sleepQueue, pid):

    '''
    Helper function for implementing wakeUp().
	'''

    if blockNo == -1:
        sleepQueue.remove(pid)
        os.kill(pid, signal.SIGHUP)
    else:
        sleepQueue.remove(pid)
        os.kill(pid, signal.SIGINT)
