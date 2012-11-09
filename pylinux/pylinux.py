import subprocess
import os
import platform
import socket
from collections import namedtuple

import readproc

## static information

def hostname():
    return subprocess.check_output(['hostname','-f'])

def ipaddr():
    # Recipe: http://stackoverflow.com/a/166589/59634
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("gmail.com",80))
    ipaddr = s.getsockname()[0]
    s.close()
        
    return ipaddr

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
    return os.uname()[4]

def totalmem():
    return readproc.meminfo()['MemTotal']

def num_disks():
    pass

def disk_stats():
    pass


## dynamic information

def last_boot():
    return subprocess.check_output(['who','-b']).\
        strip().split()[2:3]

def uptime():
    return readproc.uptime()

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

def netdevs():
    with open('/proc/net/dev') as f:
        net_dump = f.readlines()
    
    device_data={}
    data = namedtuple('data',['rx','tx'])
    for line in net_dump[2:]:
        line = line.split(':')
        if line[0].strip() != 'lo':
            device_data[line[0].strip()] = data(line[1].split()[0], 
                                                line[1].split()[8])
    return device_data
