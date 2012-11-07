import  pylinux.pylinux as pylinux

from flask import Flask
import json

app = Flask(__name__)

@app.route("/")
def index():
    return '<p>Hostname:' + pylinux.hostname() + \
        '<p> Distribution: ' + pylinux.distro_name() + \
        '<p> Release: ' + pylinux.distro_release() + \
        '<p> Nickname: ' + pylinux.distro_nickname()
                      
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
