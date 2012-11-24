import subprocess
import os
import platform

import readproc

## static information

def hostname():
    return os.uname()[1]

def distro_name():
    return platform.linux_distribution()[0]

def distro_release():
    return platform.linux_distribution()[1]

def distro_nickname():
    return platform.linux_distribution()[2]

def kernel():
    return os.uname()[2]

def cpuinfo():
    return readproc.cpuinfo()

def arch():
    return os.uname()[3]

def totalmem():
    return readproc.meminfo()['MemTotal']

def num_disks():
    pass

def disk_stats():
    pass

## dynamic information

def last_boot():
    return subprocess.check_output(['who','-b']).strip().split()[2:3]

def uptime():
    pass

def users():
    return subprocess.check_output(['who','-q']).splitlines()[0]

def freemem():
    return readproc.meminfo()['MemFree']

def nprocs():
    return readproc.nprocs()

def processes():
    return [readproc.process_name(proc) for proc in readproc.process_list()]

def lsof():
    files=subprocess.check_output(['lsof'])
    return len(files.split('\n')) 

def avg_load():
    return os.getloadavg()
