import signal
import os


def anyBuffer(sig, frame):

    '''
    Signal handler for process waiting for any buffer.
    '''
    
    print("Process",os.getpid(),": Woke up as it was sleeping for a any buffer" )

def specificBuffer(sig, frame):
    
    '''
    Signal handler for process waiting for specific buffer.
    '''
    
    print("Process",os.getpid(),": Woke up as it was sleeping for a particular buffer" )
