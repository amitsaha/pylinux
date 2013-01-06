#!/usr/bin/python

import pylinux.pylinux as pylinux

## Static Information

print 'Distribution:: ', pylinux.distro_name() + ' ' + \
    pylinux.distro_release() + ' ' + \
    pylinux.distro_nickname()

print 'OS Architecture:: ' + pylinux.arch()
print 'Kernel:: ', pylinux.kernel()
print 'Total Memory:: ' + pylinux.totalmem()

# obtain the /proc/cpuinfo information
# as a dictionary
pylinux_cpuinfo = pylinux.cpuinfo()
for i,key in enumerate(pylinux_cpuinfo.keys()):
    print 'Processor: {0} Physical ID: {1}'.format(i,pylinux_cpuinfo[key]['physical id'])

print 'Hostname:: ', pylinux.hostname()
print 'IP Address to connect to external server:: ', pylinux.ipaddr()

## dynamic information

print 'System Uptime:: {0} hours'.format(pylinux.uptime())
print 'Time of Last Boot:: ' + pylinux.last_boot()
print 'Current Users:: ' + pylinux.users()
print 'Free Memory:: ' + pylinux.freemem()
print 'Number of Processes:: ' + str(len(pylinux.processes()))
print 'Number of Open Files:: ' + str(pylinux.lsof())
print 'Average Load:: ' + pylinux.avg_load()

net_devs = pylinux.netdevs()
print 'Network Devices:: '
for dev in net_devs.keys():
    print dev + ': ' + 'Recieved (MB): ' + str(net_devs[dev].rx) +  \
        ' Transmitted (MB): ' + str(net_devs[dev].tx)
    

#mounted file systems
print 'Physical File Systems Mounted::'
print pylinux.mounts()

print 'All File Systems Mounted::'
print pylinux.mounts(nodev=False)

