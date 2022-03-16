import os
import pathlib
import requests
from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False
DEVICE_ID_FILE = "/home/pi/device_id"
BLACKLIST = "/home/pi/blacklist"
pathlib.Path(DEVICE_ID_FILE).touch()
pathlib.Path(BLACKLIST).touch()


import boot_animation
boot_animation.on_per_led()


def set_device_id(device_id=None):
    if device_id == None:
        url = "https://thesis.romanpeters.nl/api/show"
        req = requests.get(url)
        entries = req.json()["entries"]
        if not entries:
            device_id = "Unkown"
        else:
            device_id = entries[0]
    with open(DEVICE_ID_FILE, "w") as f:
        f.write(device_id)
    return f"Device ID: {device_id}"


def ban_device_id(device_id):
    return


def unban_device_id(device_id):
    return


def get_device_id():
    return pathlib.Path(DEVICE_ID_FILE).read_text()


@app.route('/')
def api_home():
    linked = f"and linked to {get_device_id()}" if get_device_id() else ""
    help_text = """
    <a href="/set">set</a>
    <a href="/reset">reset</a>
    <a href="/ban">ban</a>
    """
    return f"AIS online {linked}\n\n{help_text}"


@app.route('/set/')
def api_set():
    return set_device_id()


@app.route('/set/<device_id>/')
def api_set_id(device_id):
    return set_device_id(device_id)


@app.route('/ban/')
def api_ban():
    return pathlib.Path(BLACKLIST).read_text()


@app.route('/ban/<device_id>/')
def api_ban_id(device_id):
    if device_id in pathlib.Path(BLACKLIST).read_text().split("\n"):
        return "Already banned"
    else:
        with open(BLACKLIST, "a") as f:
            f.write(device_id)
    return f"Banned {device_id}"


@app.route('/unban/<device_id>/')
def api_unban_id(device_id):
    blacklist = pathlib.Path(BLACKLIST).read_text().split("\n")
    if device_id not in blacklist:
        return "Already not banned"
    else:
        text = "\n".join([i for i in blacklist if i != device_id])
        with open(BLACKLIST, "w") as f:
            f.write(text)
    return f"Unbanned {device_id}"


if __name__=="__main__":
    app.url_map.strict_slashes = False
    app.run(host='0.0.0.0', port=1234, debug=False)

