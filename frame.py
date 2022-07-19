import sys
import os
import requests
import json
import logging
import pathlib
import json
import time
import datetime
import yaml
import board
import neopixel


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# pairing
DEVICE_ID_PATH = "/home/pi/device_id"
TOKEN = "1234" #sys.argv[1]



def set_device_id():
    url = "https://thesis.romanpeters.nl/api/latest"
    headers = {"Authorization": TOKEN}
    response = requests.get(url, headers=headers)
    print("*"*88)
    if response.status_code == 200 and response.json().get("device_id"):
        with open(DEVICE_ID_PATH, "w+") as f:
            f.write(response.json()["device_id"])
            logger.debug("Set new device id")
    else:
        logger.warning(f"{url} unreachable {response.status_code}")


if not os.path.exists(DEVICE_ID_PATH):
    set_device_id()



#assert len(sys.argv) == 2, "Usage: sudo python3 frame.py TOKEN"
DEVICE_ID = pathlib.Path('/home/pi/device_id').read_text().strip()
URL = f"https://thesis.romanpeters.nl/api/{DEVICE_ID}/"
FRAME_PATH = "./last_frame"
pathlib.Path(FRAME_PATH).touch()


# TODO dynamic brightness configuration
with open('/home/pi/config.yml', 'r') as f:
    config = yaml.safe_load(f)

pixels = neopixel.NeoPixel(board.D18, 50, brightness=config['brightness'], auto_write=False)


def get_frame(url):
    headers = {"Authorization": TOKEN}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        # couple of retries
        n = 0
        while not response.status_code == 200:
            logger.warning(f"Website status code={response.status_code} {url}")
            n += 1
            if n == 7:  # fatal
                return ""

            retry_timer = pow(n+1, 2) # 4s, 9s, 16s, 25s, 36s, 49s
            logger.debug(f"Retrying in {retry_timer} seconds")
            time.sleep(retry_timer)
            response = requests.get(url, headers=headers)
    return  response.json()


def save_frame(frame, path):
    with open(path, 'w+') as f:
        f.write(json.dumps(frame))

def set_led(path, verbose=True):
    frame = json.loads(pathlib.Path(path).read_text())
    if verbose:
        logger.debug(f'loaded frame={frame}')
    else:
        logger.debug(f"setting pixels from frame")
    for window in frame["windows"].values():
        pixels[window["index"]] = tuple(window["pixel"])
        if verbose:
            logger.debug(f"setting pixel {window['index']} to {window['pixel']}")
    pixels.show()



if __name__=="__main__":
    # pull frame
    frame = get_frame(URL)

    # persistent storage if new frame
    if frame:
        save_frame(frame, FRAME_PATH)

    # update AIS
    set_led(FRAME_PATH)

    # continue updating AIS for a minute
    current_minute = datetime.datetime.now().minute
    while datetime.datetime.now().minute == current_minute:
        set_led(FRAME_PATH, verbose=False)
        time.sleep(2)

    print("done!")


