from collections import OrderedDict, namedtuple
import sys
import os

def uptime():
    ''' Returns system uptime in hours '''

    with open('/proc/uptime') as f:
        hours= (float(f.read().split()[0]))/(3600.0)
    return hours
              
def nprocs():
    ''' Number of processing units '''

    nprocs=0
    with open('/proc/cpuinfo') as f:
        for line in f:
            if line.rstrip():
                if line.split()[0].lower()=='processor':
                    nprocs = nprocs+1
    return nprocs

def cpuinfo():
    ''' Return the information in /proc/cpuinfo
    as a dictionary in the following format:
    cpu_info['proc0']={...}
    cpu_info['proc1']={...}

    '''

    cpuinfo=OrderedDict()
    procinfo=OrderedDict()
    nprocs = 0

    with open('/proc/cpuinfo') as f:
        for line in f:
            if not line.strip():
                # end of one processor
                cpuinfo['proc%s' % nprocs] = procinfo
                nprocs=nprocs+1
                procinfo={}
            else:
                if len(line.split(':')) == 2:
                    procinfo[line.split(':')[0].strip()] = line.split(':')[1].strip()
                else:
                    procinfo[line.split(':')[0].strip()] = ''
            
    return cpuinfo
    
def meminfo():
    ''' Return the information in /proc/meminfo
    as a dictionary '''
    meminfo={}

    with open('/proc/meminfo') as f:
        for line in f:
            meminfo[line.split(':')[0]] = line.split(':')[1].strip()
    return meminfo

def process_name(pid):
    ''' Given a PID return the process name '''
    try:
        with open('/proc/{0}/comm'.format(pid)) as f:
            cmdline=f.read()
            if cmdline.rstrip():
                process=cmdline.split()[0]
            else:
                process=''
    except IOError:
        process= None
    finally:
        return process

def process_list():
    ''' List of all process IDs currently active '''

    #Idea stolen from psutil: http://code.google.com/p/psutil/
    pids = [subdir for subdir in os.listdir('/proc') if
            subdir.isdigit()]
    return pids

def maps(pid):
    ''' Returns the /proc/<pid>maps data as a machine consumable
    list of dictionary with each item having the following fields:

    address
    permissions
    offset
    dev
    inode
    pathname
    '''

    pidmaps = []
    fields = ['address', 'perms', 'offset', 'dev', 'inode' ,'pathname']
    try:
        with open('/proc/{0}/maps'.format(pid)) as f:
            for line in f:
                pidmap = {}
                for n,field in enumerate(fields):
                    # the pathname may not be present
                    # sometimes
                    if len(line.split()) == 6:
                        pidmap[field] = line.split()[n]
                    else:
                        pidmap[field] = ""
                pidmaps.append(pidmap)
    except IOError:
        pidmaps = None

    return pidmaps

def sharedlibs(pid):
    ''' Shared libraries used by the process with the given 
    PID 
    '''

    pidmap = maps(pid)
    sharedlibs = {}
    if pidmap is not None:        
        for item in pidmap:
            if '.so' in item['pathname']:
                if hash(item['pathname']) not in sharedlibs.keys():
                    sharedlibs[hash(item['pathname'])]= item['pathname']
    else:
        return None
    
    return sharedlibs

def status(pid):
    ''' Returns the state of the process as represented in
        /proc/<pid>status as a machine consumable dictionary
    '''
    status = {}
    try:
        with open('/proc/{0}/status'.format(pid)) as f:
            for line in f:
                status[line.split(':')[0]] = line.split(':')[1].strip()
    except EnvironmentError:
        status = None

    return status

def pstree(pid):

    ''' Find the process tree corresponding to a process
    with PID, pid '''

    if pid != '0':        
        status = status(pid)
        if status is not None:
            ppid = status['ppid']
            pid = ppid
            print status['Name'],status['Pid']            
            pstree(pid)
        else:
            print 'Non-existent process'
            sys.exit()           
    else:
        return

def netdevs():
    ''' RX and TX bytes for each of the network devices '''

    with open('/proc/net/dev') as f:
        net_dump = f.readlines()
    
    device_data={}
    data = namedtuple('data',['rx','tx'])
    for line in net_dump[2:]:
        line = line.split(':')
        if line[0].strip() != 'lo':
            device_data[line[0].strip()] = data(float(line[1].split()[0])/(1024.0*1024.0), 
                                                float(line[1].split()[8])/(1024.0*1024.0))
    
    return device_data
