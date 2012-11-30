PyLinux: Python Interface to Linux System Information
=====================================================

Static Information
------------------

* Hostname, CPU information and Archictecture, Total Memory.
* Kernel version, Linux Distribution name and release
* Disk Information (TODO)


Dynamic Information
-------------------

* Uptime and time of last boot
* Users logged in
* Free memory
* Running processes
* Open files
* Average load
* Network Info
* disk info.. (TODO)

Usage
-----

* Install using # python setup.py install
* Use away ::

    >>> import pylinux.pylinux as pylinux
    >>> pylinux.distro_name()
    'Fedora remix'
    >>> pylinux.arch()
    'armv6l'
    >>> pylinux.freemem()
    '44356 kB
* See examples/flask_app for a Flask web application using pylinux
