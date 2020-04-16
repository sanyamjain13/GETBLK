import BufferHeader

class Buffer:

    '''
    INSTANCE VARIABLES :
        hashQSize, freeListSize, freeListHead, hashQ
    '''

    def __init__(self, freeListSize = 16, hashQSize = 4):

        '''
        Input Parameters:
        
            self : Implicit object of Buffer class
            freeListSize : Total number of free buffers (initially i.e.
                           total number of buffers) with a default value
                           of 16.
            hashQSize : Size of the hashQ with a default value of 4

        '''

        #FREE LIST INITIALIZATION
        ''' IMPLEMENTATION : CIRCULAR DOUBLY LINKED LIST'''
        
        if freeListSize < 1:
            return
        
        self.freeListSize = freeListSize
        self.freeListHead = BufferHeader.BufferHeader(-1)
        prevBuffer = self.freeListHead

        for i in range(freeListSize-1):
            buffer = BufferHeader.BufferHeader(-1)
            prevBuffer.setFreeListNext(buffer)
            buffer.setFreeListPrev(prevBuffer)
            prevBuffer = buffer

        self.freeListHead.setFreeListPrev(prevBuffer)
        prevBuffer.setFreeListNext(self.freeListHead)


        #HASH QUEUE INITIALIZATION
        ''' IMPLEMENTATION : HASH TABLE OF DOUBLY LINKED LIST'''


        self.hashQSize = hashQSize
        self.hashQ = []

        for i in range(hashQSize):
            self.hashQ.append(None)

    
    '''
    Functions to manipulate Free List.
    '''


    def getFreeListHeader(self):
        return self.freeListHead
    

    def findBlockInFreeList(self, blockNum):
        buffer = self.freeListHead

        if buffer.getBlockNum() == blockNum:
            return buffer

        buffer = buffer.getFreeListNext()

        while buffer != self.freeListHead:
            if buffer.getBlockNum() == blockNum:
                return buffer
            buffer = buffer.getFreeListNext()

        return None


    def isEmptyFreeList(self):
        return self.freeListHead == None


    def addToFreeList(self, buffer, atBeg = False):
        
        #if being added to free list then that means it is in hashQ
        

        #adding a buffer to the empty freelist
        if self.freeListHead == None:
            self.freeListHead = buffer
            buffer.setFreeListNext(buffer)
            buffer.setFreeListPrev(buffer)

        else:
            
            lastBlock = self.freeListHead.getFreeListPrev()

            lastBlock.setFreeListNext(buffer)
            buffer.setFreeListPrev(lastBlock)

            buffer.setFreeListNext(self.freeListHead)
            self.freeListHead.setFreeListPrev(buffer)

            #if the buffer was to be added at the front
            if atBeg:
                self.freeListHead = buffer
                
        buffer.setLockedStatus(False)
        self.freeListSize += 1

        
    #get any buffer from the free list    
    def getAnyBuffer(self):
        
        if self.isEmptyFreeList():
            return None
        
        buffer = self.freeListHead
        #self.removeFromFreeList(buffer.getBlockNum())
        return buffer


    def removeFromFreeList(self, blockNo):
        buffer = self.findBlockInFreeList(blockNo)

        #checking if the buffer was on free list, if not then nothing is removed
        if buffer.getFreeListNext() == None or buffer.getFreeListPrev() == None:
            print(blockNo,buffer.getFreeListNext(),buffer.getFreeListPrev())
            return -1

        #if buffer is the only one present in the whole list
        if buffer == self.freeListHead and self.freeListHead.getFreeListNext() == self.freeListHead:
            buffer.removeFreeListNext()
            buffer.removeFreeListPrev()
            self.freeListHead = None
            self.freeListSize -= 1
            return 1 #indicates blockNum removed successfully

        #if block is the head of free list
        elif buffer == self.freeListHead:
            self.freeListHead = buffer.getFreeListNext()
        
        buffer.getFreeListPrev().setFreeListNext(buffer.getFreeListNext())
        buffer.getFreeListNext().setFreeListPrev(buffer.getFreeListPrev())

        buffer.removeFreeListPrev()
        buffer.removeFreeListNext()
        
        self.freeListSize -= 1
        return 1


    def printFreeList(self):

        buffer = self.freeListHead
        if buffer == None:
            print("\nFree List is empty")
            return

        print("\nFree List :")
        print("\nAvailable buffers:",self.freeListSize)
        print("\n",buffer.getBlockNum(), end="")

        buffer = buffer.getFreeListNext()

        while buffer != self.freeListHead:
            print(" -> ", buffer.getBlockNum(),sep = "", end = "")
            buffer = buffer.getFreeListNext()

        print()
    

    '''
    Functions to manipulate Hash Queue.
    '''


    def findBlockInHashQ(self, blockNum):

        #get the possible queue header where block maybe present
        queueHead = queueBuffer = self.hashQ[blockNum % self.hashQSize]

        while queueBuffer != None:
            if queueBuffer.getBlockNum() == blockNum:
                return queueBuffer
            
            queueBuffer = queueBuffer.getHashQNext()
            #if back at the front then break
            if queueBuffer == queueHead :
                break

        return None


    def isPresentInHashQ(self, blockNum):
        
        if self.findBlockInHashQ(blockNum) == None:
            return False

        return True


    def addBlockToHashQ(self, buffer):
        queueHead = self.hashQ[buffer.getBlockNum() % self.hashQSize]

        if queueHead == None:
            self.hashQ[buffer.getBlockNum() % self.hashQSize] = buffer
            buffer.setHashQNext(buffer)
            buffer.setHashQPrev(buffer)
            return 1

        queueEnd = queueHead.getHashQPrev()
        queueEnd.setHashQNext(buffer)
        
        buffer.setHashQPrev(queueEnd)

        buffer.setHashQNext(queueHead)
        queueHead.setHashQPrev(buffer)


    #Before removing add it to the free list
    def removeFromHashQ(self, buffer):
        
        if buffer == None:
            return -1    #indicates block not found in HashQ

        #block not in hashQ(starting case)
        if buffer.getHashQNext() == None and buffer.getHashQPrev == None:
            return 1

        qNum = buffer.getBlockNum() % self.hashQSize
        
        #if only blockNum is present in hashQ
        if buffer.getHashQNext() == buffer:
            buffer.removeHashQNext()
            buffer.removeHashQPrev()
            self.hashQ[qNum] = None
            return 1

        #if blockNum is present at the first Buffer
        if buffer.getBlockNum() == self.hashQ[qNum].getBlockNum():
            self.hashQ[qNum] = self.hashQ[qNum].getHashQNext()

        buffer.getHashQPrev.setHashQNext(buffer.getHashQNext())
        buffer.getHashQNext.setHashQPrev(buffer.getHashQPrev())


    def printHashQ(self):

        for i in range(self.hashQSize):
            buffer = self.hashQ[i]
            if buffer == None:
                print("\nQueue "+ str(i) +" is empty.")
                continue

            print("\nQueue "+ str(i) +":", end="")
            print(buffer.getBlockNum(), end = "")

            buffer = buffer.getHashQNext()

            while buffer != self.hashQ[i]:
                print(" -> ",buffer.getBlockNum(),sep = "", end = "")
                buffer = buffer.getHashQNext()

            print("\n")


    #since before removeBlockFromHashQ we will call addToFreeList we will be able to find the oldBlock
    def setBlockNum(self, oldBlockNum, newBlockNum):
        buffer = self.findBlockInHashQ(oldBlockNum)
        
        if buffer == None:
            buffer = self.findBlockInFreeList(oldBlockNum)

        buffer.setBlockNum(newBlockNum)


    def setLockedBit(self, blockNum):

        buffer = self.findBlockInHashQ(blockNum)

        if buffer == None:
            buffer = self.findBlockInFreeList(blockNum)

        buffer.setLockedStatus(True)


    def clearLockedBit(self, blockNum):

        buffer = self.findBlockInHashQ(blockNum)

        if buffer == None:
            buffer = self.findBlockInFreeList(blockNum)

        buffer.setLockedStatus(False)


    def checkLockedStatus(self, blockNum):

        buffer = self.findBlockInHashQ(blockNum)

        if buffer == None:
            buffer = self.findBlockInFreeList(blockNum)

        return buffer.getLockedStatus()


    def setValidBit(self, blockNum):

        buffer = self.findBlockInHashQ(blockNum)

        if buffer == None:
            buffer = self.findBlockInFreeList(blockNum)

        buffer.setValidStatus(True)


    def clearValidBit(self, blockNum):

        buffer = self.findBlockInHashQ(blockNum)

        if buffer == None:
            buffer = self.findBlockInFreeList(blockNum)

        buffer.setValidStatus(False)


    def checkValidBit(self, blockNum):

        buffer = self.findBlockInHashQ(blockNum)

        if buffer == None:
            buffer = self.findBlockInFreeList(blockNum)

        return buffer.getValidStatus()


    def setDelayedWriteBit(self, blockNum):

        buffer = self.findBlockInHashQ(blockNum)

        if buffer == None:
            buffer = self.findBlockInFreeList(blockNum)

        buffer.setDelayedWrite(True)


    def clearDelayedWriteBit(self, blockNum):

        buffer = self.findBlockInHashQ(blockNum)

        if buffer == None:
            buffer = self.findBlockInFreeList(blockNum)

        buffer.setDelayedWrite(False)


    def checkDelayedWriteBit(self, blockNum):

        buffer = self.findBlockInHashQ(blockNum)

        if buffer == None:
            buffer = self.findBlockInFreeList(blockNum)

        return buffer.getDelayedWrite()
