import time
from frame import set_led, FRAME_PATH

if __name__== "__main__":
    print("Starting frame setter...")
    while True:
        try:
            set_led(FRAME_PATH)
        except Exception as e:
            print(e)
        time.sleep(1)
