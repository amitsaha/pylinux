import subprocess
import os
import platform
import socket

import readproc

## static information
def hostname():
    ''' Return the Hostname '''

    return os.uname()[1]

def ipaddr():
    '''IP address used to connect to the world'''

    # Recipe: http://stackoverflow.com/a/166589/59634
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("gmail.com",80))
    except IOError:
        return 'Could not retrieve address'
    else:
        ipaddr = s.getsockname()[0]
        s.close()
        return ipaddr

def distro_name():
    '''Linux distribution Name'''

    return platform.linux_distribution()[0]

def distro_release():
    ''' Release '''

    return platform.linux_distribution()[1]

def distro_nickname():
    ''' Distro Nickname '''

    return platform.linux_distribution()[2]

def kernel():
    ''' Kernel version '''

    return os.uname()[2]

def cpuinfo():
    ''' Return the data in /proc/cpuinfo as a dictionary
    of dictionaries '''

    return readproc.cpuinfo()

def arch():
    ''' Architecture of the OS'''

    return os.uname()[4]

def nprocs():
    ''' Number of processing units '''

    return readproc.nprocs()

def totalmem():
    ''' Total memory in the system '''

    return readproc.meminfo()['MemTotal']


## dynamic information
def last_boot():
    ''' Time of last boot '''

    return str(subprocess.check_output(['who','-b']).\
        strip().split()[2:])

def uptime():
    ''' System uptime '''

    return readproc.uptime()

def users():
    ''' Currently logged in users '''

    return str(subprocess.check_output(['who','-q']).splitlines()[0])

def freemem():
    ''' Free memory '''

    return readproc.meminfo()['MemFree']

def processes():
    ''' Currently running processes '''

    return [readproc.process_name(proc) for proc in readproc.process_list()]

def lsof():
    ''' Number of Open files '''

    files=subprocess.check_output(['lsof'])
    return len(files.split('\n'))

def avg_load():
    ''' Average load '''

    return str(os.getloadavg())

def netdevs():
    ''' Retrieve the Network device information using readproc.py
    module '''

    return readproc.netdevs()

def mounts(nodev=True):
    ''' Return current filesystem usage stats .
    uses df utility command

    nodev=True for getting physical FSs
          False for all
    '''

    # Get the loaded FSs
    loaded_fs=[]
    with open('/proc/filesystems') as f:
        for line in f:
            line=line.split('\n')[0]
            if nodev:
                if line.split('\t')[0]=='':
                    loaded_fs.append(line.split('\t')[1])
            else:
                loaded_fs.append(line.split('\t')[1])

    # build up file system list for df
    df_fs=[]
    for fs in loaded_fs:
        df_fs.extend(['-t',fs])

    # Get the mounted file systems
    df_cmd = ['df','-k','-T']
    df_cmd.extend(df_fs)
    df = subprocess.check_output(df_cmd)

    # TODO: just return a list of mounted partitions for now
    # in the following format:
    # Filesystem     Type 1K-blocks      Used Available Use% Mounted on
    # /dev/sda2      ext4  51614140  14499996  36589880  29% /
    # ..
    # Perhaps group them into a dictionary and return..

    return df
