import  pylinux.pylinux as pylinux

from collections import OrderedDict
from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route("/plot")
def memory():
    data={}

    freemem=str(float(pylinux.freemem().split()[0])/1024.0)
    data['freemem'] = freemem

    nfiles = pylinux.lsof()
    data['nfiles']= nfiles

    nprocs=len(pylinux.processes())
    data['nprocs']= nprocs

    return json.dumps(data)

@app.route("/dynamic")
def dynamic():
    dynamic_info = OrderedDict({'Uptime':str(pylinux.uptime())+' hours',
                                #'Number of Processes':len(pylinux.processes()),
                                #'Open Files':pylinux.lsof(),
                                #'Free Memory':str(float(pylinux.freemem().split()[0])/1024.0) + ' MB',
                                'Network Stats':pylinux.netdevs(),
                                'Load':pylinux.avg_load()
                                })
    return render_template('dynamic.html',dynamic_info=dynamic_info)

@app.route("/")
def index():

    static_info = OrderedDict({'FQDN':pylinux.hostname(),
                               'Linux Distribution':pylinux.distro_name(),
                               'Release': pylinux.distro_release() + '(' +pylinux.distro_nickname() + ')',
                               'Arch': pylinux.arch(),
                               'Processing Units':pylinux.nprocs(),
                               'Total Memory': str(float(pylinux.totalmem().split()[0])/1024.0) + ' MB',
                               'Kernel':pylinux.kernel()
                   })
    return render_template('index.html',static_info=static_info)
                      
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
