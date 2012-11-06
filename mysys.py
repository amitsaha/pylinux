import subprocess
import os
import readproc

def lsof():
    files=subprocess.check_output(['lsof'])
    return len(files.split('\n'))
    
def uname():
    uname = os.uname()
    return dict({'hostname':uname[1],
                 'Kernel':uname[2],
                 'Arch':uname[3]})

def totalmem():
    return readproc.meminfo()['MemTotal']

def freemem():
    return readproc.meminfo()['MemFree']

def procs():
    return readproc.nprocs()

def processes():
    return [readproc.process_name(proc) for proc in readproc.process_list()]
    
        
    
    




    
