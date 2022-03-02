import sys
import requests
import logging
import pathlib
import json
import time
import yaml
import board
import neopixel

assert len(sys.argv) == 2, "Usage: python3 frame.py TOKEN"
TOKEN = sys.argv[1]
DEVICE_ID = pathlib.Path('/home/pi/device_id').read_text()
URL = f"https://thesis.romanpeters.nl/api/{DEVICE_ID}"
FRAME_PATH = "./last_frame"


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# TODO dynamic brightness configuration
with open('/home/pi/config.yml', 'r') as f:
    config = yaml.safe_load(f)

pixels = neopixel.NeoPixel(board.D18, 50, brightness=config['brightness'], auto_write=False)


def get_frame(url):
    headers = {"Authorization": TOKEN}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        j = response.json()
    else:
        # couple of retries
        n = 0
        while not response.status_code == 200:
            logger.warning(f"Website status code={response.status_code}")
            n += 1
            if n == 7:  # fatal
                return ""

            retry_timer = pow(n+1, 2) # 4s, 9s, 16s, 25s, 36s, 49s
            logger.debug(f"Retrying in {retry_timer} seconds")
            time.sleep(retry_timer)
            response = requests.get(url, headers=headers)
    return ' '.join(j['frame'])


def save_frame(frame, path):
    with open(path, 'w+') as f:
        f.write(frame)

def set_led(path):
    frame = pathlib.Path(path).read_text().split()
    logger.debug(f'loaded frame={frame}')
    for n, rgb in enumerate(frame):
        pixels[n] = tuple(map(float, rgb.split(':')))
    pixels.show()



if __name__=="__main__":
    # pull frame
    frame = get_frame(URL)

    # persistent storage if new frame
    if frame:
        save_frame(frame, FRAME_PATH)

    # update AIS
    set_led(FRAME_PATH)

    print("done!")


