import os
import pathlib
import requests
from flask import Flask

app = Flask(__name__)
DEVICE_ID_FILE = "/home/pi/device_id"
pathlib.Path(DEVICE_ID_FILE).touch()

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

def get_device_id():
    return pathlib.Path(DEVICE_ID_FILE).read_text()

@app.route('/')
def api_home():
    linked = f"and linked to {get_device_id()}" if get_device_id() else ""
    return f"AIS online {linked}"


@app.route('/set')
def api_set():
    return set_device_id()


@app.route('/set/<device_id>')
def api_set_id(device_id):
    return set_device_id(device_id)


app.run(host='0.0.0.0', port=80, debug=False)

