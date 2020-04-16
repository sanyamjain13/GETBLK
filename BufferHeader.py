#CLASS BUFFER HEADER

class BufferHeader:

    '''

    Instance Variables:
    
                    block_num :Block number of data on disk
                    valid_status: Tells if buffer is currently locked or free
                    delayed_write_status:  Tells that kernel must write the buffer contents to disk
                                           before reassigning the buffer or not
                    waiting_process_count: how many proceess are waiting for the current buffer
                    hashq_nextBuf= points to next buffer in the hash queue
                    hashq_prevBuf= points to previous buffer in the hash queue
                    freeList_nextBuf:: points to the next free buffer in the free list
                    freeList_prevBuf:: points to the previous free buffer in the free list
                    
    '''

    def __init__(self, block_num = 0):
        
        self.block_num = block_num
        self.valid_status = False
        self.locked_status = False
        self.delayed_write_status = False
        self.waiting_process_count = 0
        self.hashQ_nextBuf = self
        self.hashQ_prevBuf = self
        self.freeList_nextBuf = None
        self.freeList_prevBuf = None

    '''
    Functions to set the values in the buffer header
    '''

    def setBlockNum(self,bno):
        self.block_num=bno

    def setValidStatus(self,status):
        self.valid_status=status

    def setDelayedWrite(self,status):
        self.delayed_write_status=status

    def addWaitingProcess(self,count):
        self.waiting_process_count=count

    def setLockedStatus(self, status):
        self.locked_status = status

    def setHashQNext(self,buffer):
        self.hashQ_nextBuf=buffer
        
    def setHashQPrev(self,buffer):
        self.hashQ_prevBuf=buffer

    def setFreeListNext(self,buffer):
        self.freeList_nextBuf=buffer
        
    def setFreeListPrev(self,buffer):
        self.freeList_prevBuf=buffer

    def removeFreeListNext(self):
        self.freeList_nextBuf = None

    def removeFreeListPrev(self):
        self.freeList_prevBuf = None

    def removeHashQNext(self):
        self.hashQ_nextBuf = None

    def removeHashQPrev(self):
        self.hashQ_prevBuf = None
    
    '''
    Function to get the values in the buffer header
    '''

    def getBlockNum(self):
        return self.block_num

    def getValidStatus(self):
        return self.valid_status

    def getDelayedWrite(self):
        return self.delayed_write_status

    def getWaitingProcess(self):
        return self.waiting_process_count

    def getLockedStatus(self):
        return self.locked_status

    def getHashQNext(self):
        return self.hashQ_nextBuf
        
    def getHashQPrev(self):
        return self.hashQ_prevBuf

    def getFreeListNext(self):
        return self.freeList_nextBuf
        
    def getFreeListPrev(self):
        return self.freeList_prevBuf