import random

class SleepQueue:
    
    '''
    INSTANCE VARIABLES:\n
        sleepQueue : a dictionary of the form\n\t\t\t {blockNum: list of PIDs of processes waiting for this block }
        revSleepQueue : a dictionary of the form {pid : blockNum} for fast removal 
    '''
    
    def __init__(self):
    
        '''
        Constructor :  Initializes the Sleep Queue
        '''
    
        self.sleepQueue = {}
        self.revSleepQueue = {}
    
    
    def add(self, blockNum, pid):
    
        '''
        Adds the pid of the process waiting for blockNum to get free in the Sleep Queue.\n
        Give blockNum -1 to add pid of a process waiting for any Block Number to get free in the Sleep Queue.
        '''
    
        if blockNum in self.sleepQueue:
            self.sleepQueue[blockNum].append(pid)
        else:
            self.sleepQueue[blockNum] = [pid]

        self.revSleepQueue[pid] = blockNum
        print("Process",pid,"added to the sleep queue")

    
    def remove(self, pid):
    
        '''
        Removes the given pid from Sleep Queue.
        '''
    
        if pid in self.revSleepQueue:
            blockNum = self.revSleepQueue.pop(pid)
            self.sleepQueue[blockNum].remove(pid)

            # if no more processes are waiting for this block, remove blockNum from sleepQueue
            if len(self.sleepQueue[blockNum]) == 0:
                self.sleepQueue.pop(blockNum)

    
    def getRandomProcess(self, blockNum):
    
        '''
        Returns a random pid of a process waiting for given blockNum in the Sleep Queue.\n
        Returns None, if no such pid.
        '''
    
        if blockNum in self.sleepQueue:
            randIndex = random.randrange(len(self.sleepQueue[blockNum]))  # get a random index
            pid = self.sleepQueue[blockNum][randIndex] # pid of process at that index
            return pid 
            
    
    def printSQ(self):
    
        '''
        Prints the contents of the Sleep Queue.
        '''
    
        print("-----SLEEP QUEUE-----")
    
        for blockNo in self.sleepQueue:
            st = "["
            for pid in self.sleepQueue[blockNo]:
                st += str(pid) + ", "
            st += "]"
            print(blockNo, ":", st)
