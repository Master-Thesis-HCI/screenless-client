import requests
import logging
import pathlib
import json
import time
import yaml
import board
import neopixel


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# TODO dynamic brightness configuration

with open('/home/pi/config.yml', 'r') as f:
    config = yaml.safe_load(f)

pixels = neopixel.NeoPixel(board.D18, 50, brightness=config['brightness'], auto_write=False)

TOKEN = pathlib.Path('/home/pi/.token').read_text().strip()
URL = "https://thesis.romanpeters.nl/frame"
FRAME_PATH = "./last_frame"


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

            logger.debug(f"Retrying in {pow(n+1, 2)} seconds")
            time.sleep(pow(n+1, 2))  # 4... 9... 16... 25... 36...
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


