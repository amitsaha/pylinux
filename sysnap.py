import mysys

print mysys.uname()
print mysys.procs()
print mysys.totalmem()
print mysys.freemem()
for pro in mysys.processes():
    print pro
