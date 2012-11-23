from  pylinux import *

print hostname()
print distro_name()
print distro_release()
print distro_nickname()
print kernel()
print cpuinfo()
print arch()
print totalmem()
print num_disks()
print disk_stats()

## dynamic information

print last_boot()
print uptime()
print users()
print freemem()
print nprocs()
print processes()
print lsof()
print avg_load()
