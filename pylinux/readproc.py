import sys
import os

# uptime
def uptime():
    with open('/proc/uptime') as f:
        # return uptime in hours
        hours= (float(f.read().split()[0]))/(3600.0)
    return hours
              

# number of processors
def nprocs():
    nprocs=0
    with open('/proc/cpuinfo') as f:
        for line in f:
            if line.rstrip():
                if line.split()[0]=='Processor':
                    nprocs = nprocs+1
    return nprocs

def cpuinfo():
    cpuinfo={}
    procinfo={}
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
                    procinfo[line.split(':')[0]] = line.split(':')[1].strip()
                else:
                    procinfo[line.split(':')[0]] = ''
            
    return cpuinfo
    
def meminfo():
    meminfo={}

    with open('/proc/meminfo') as f:
        for line in f:
            meminfo[line.split(':')[0]] = line.split(':')[1].strip()
    return meminfo

def process_name(pid):
    with open('/proc/{0}/comm'.format(pid)) as f:
        cmdline=f.read()
        if cmdline.rstrip():
            process=cmdline.split()[0]
        else:
            process=''
    return process

def process_list():
    #Idea stolen from psutil: http://code.google.com/p/psutil/
    pids = [subdir for subdir in os.listdir('/proc') if
            subdir.isdigit()]
    return pids

def maps(pid):
    ''' Returns the /proc/<pid>maps data as a machine consumable
    list of dictionary objects'''
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
    except EnvironmentError:
        pidmaps = None

    return pidmaps

def sharedlibs(pid):
    pidmap = maps(pid)
    sharedlibs = {}
    if pidmap is not None:        
        for item in pidmap:
            if '.so' in item['pathname']:
                if hash(item['pathname']) not in sharedlibs.keys():
                    sharedlibs[hash(item['pathname'])]= item['pathname']
                    #print item['pathname']
    else:
        print 'Non-existent process'
    
    return sharedlibs

def sharedlib_stats():
    # sweep /proc for shared libraries being used by processes
    pids = process_list()
    lib_stats = {}
    for pid in pids:
        for lib in sharedlibs(pid).values():
            if lib in lib_stats.keys():
                lib_stats[lib] += 1
            else:
                lib_stats[lib] = 1

    for lib in lib_stats.keys():
        print os.path.split(lib)[1], lib_stats[lib]

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

def ppid(d):
    return d['PPid']

def pstree(pid):

    if pid != '0':        
        status = status(pid)
        if status is not None:
            ppid = ppid(status)
            pid = ppid
            print status['Name'],status['Pid']            
            pstree(pid)
        else:
            print 'Non-existent process'
            sys.exit()           
    else:
        return
        
if __name__=='__main__':

    #pid = sys.argv[1]

    # Usage scenarios

    # Process tree
    #pstree(pid)
    
    # Shared libraries being used by processes
    #sharedlib_stats()
    pass
