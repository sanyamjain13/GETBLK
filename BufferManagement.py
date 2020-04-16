import Buffer
import os
import signal
import SignalCatcher
import threading
import time
import random
import BufferRelease


def sleepForBuffer(sleepQueue, blockNo = -1):
    
    '''
    Process sets signal handler accordingly and goes to sleep(event: buffer becomes free).
    SIGNIT: signifies freeing of any buffer.
    SIGHUP: signifies freeing of specific buffer.
    '''

    if blockNo == -1:
        signal.signal(signal.SIGHUP,SignalCatcher.anyBuffer)
    else:
        signal.signal(signal.SIGINT,SignalCatcher.specificBuffer)

    sleepQueue.add(blockNo,os.getpid())

    signal.pause()
    

def asynchronousWrite(buffer, bufferHead, sleepQueue, lock):
    
    '''
    Buffer marked with delayed write is asynchronously written into disk.
    '''

    lock.acquire()
    buffer = bufferHead.findBlockInFreeList(buffer.getBlockNum())
    lock.release()
    
    buffer.setDelayedWrite(False)
    time.sleep(5)
    
    lock.acquire()
    bufferHead.addToFreeList(buffer,True)
    lock.release()
    
    blockNo = buffer.getBlockNum()

    print("Done with async writing of buffer with block number",blockNo)
    bufferHead.printFreeList()



def asyncHelper(blockNo, bufferHead, sleepQueue, lock):
    
    '''
    Helper function for carrying out asynchronousWrite().
    '''

    #remove buffer from the free list
    lock.acquire()
    
    buffer = bufferHead.findBlockInFreeList(blockNo)
    bufferHead.removeFromFreeList(blockNo)

    lock.release()

    print("\nProcess",os.getpid(),": Begin async writing of buffer with block number",blockNo)    
    
    t1 = threading.Thread(target=asynchronousWrite, args=(buffer, bufferHead, sleepQueue, lock))9
    t1.start()




def getBlk(blockNo, bufferHead, sleepQueue, lock):
    
    '''
    Implementation of GETBLK algorithm.

    Input parameter:
        blockNo: disk logical block number
        sleepQueue, bufferHead, lock: Shared memory data structures

    Return Value: locked buffer 
    '''
    
    buffer = None

    while buffer==None:
        print("Process",os.getpid(),": At starting of")
        lock.acquire()

        #find buffer in hashQueue
        buffer = bufferHead.findBlockInHashQ(blockNo)
        if buffer != None:
            
            #find if buffer is busy
            if buffer.getLockedStatus():
    
                print("Process", os.getpid(),": Going for sleep as block number",blockNo,"is present in the HashQ but isn't free")
                lock.release()
                buffer = None
                sleepForBuffer(sleepQueue, blockNo)
                continue

            #else if the buffer is free    
            else:

                if buffer.getValidStatus() == False:
                    print("Process", os.getpid(),": Buffer content invalid... Reading buffer from the disk")
                    buffer.setValidStatus(True)
                    
                #Mark buffer as busy
                buffer.setLockedStatus(True)

                #print("Removing",buffer.getBlockNum(),buffer.getFreeListNext(),buffer.getFreeListPrev())
                bufferHead.printFreeList()

                #Remove from freeList
                bufferHead.removeFromFreeList(buffer.getBlockNum())

                print("Process", os.getpid(),": Got buffer with block number",blockNo," from hashQ")
                bufferHead.printFreeList()

                lock.release()
        
        else:
            
            #Get any buffer from the freeList
            #Check if freeList is empty
            if bufferHead.isEmptyFreeList():
                
                print("Process", os.getpid(),": Going for sleep as no buffer is free")
                lock.release()

                buffer = None
                #sleep for any buffer
                sleepForBuffer(sleepQueue)
                continue

            else:

                #if freeList is not empty get a buffer    
                #buffer = bufferHead.findBlockInFreeList(-1)
                buffer = bufferHead.getAnyBuffer()

                #check if the buffer was marked for delayed write
                if buffer.getDelayedWrite():

                    #process will go for async writing
                    print("Process", os.getpid(),": Got a buffer which was marked with delayedWrite")
                    print("Process", os.getpid(),": Status of freeList before:")
                    bufferHead.printFreeList()

                    lock.release()
                    asyncHelper(buffer.getBlockNum(), bufferHead, sleepQueue, lock)
                    
                    #Asynchronous write will remove the buffer from the freeList
                    #Start writing the buffer into the disk block asynchronously
                    #And then will add the process to the head of freeList

                    lock.acquire()

                    print("Process", os.getpid(),": Status of freeList after:")
                    bufferHead.printFreeList()
                    
                    lock.release()
                    buffer = None
                    continue


                else:
                    
                    #lock the buffer
                    buffer.setLockedStatus(True)
                    
                    #Remove from free list
                    bufferHead.removeFromFreeList(buffer.getBlockNum())
                    print("Process", os.getpid(),": Buffer with block number", buffer.getBlockNum(),"removed from free list")
                    
                    #Update HashQ
                    if bufferHead.findBlockInHashQ(buffer.getBlockNum()) != None:
                        bufferHead.removeFromHashQ(buffer)

                    buffer.setBlockNum(blockNo)
                    bufferHead.addBlockToHashQ(buffer)
                    print("Process", os.getpid(),": Buffer with block number",blockNo,"added to the hash queue")

                    lock.release()

    return buffer        
