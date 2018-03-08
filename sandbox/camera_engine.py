import multiprocessing
import queue
import random
import time
import sys
import os
from io import BytesIO

import numpy
import requests
from PIL import Image

master = os.path.abspath(os.path.join(__file__, '..', '..'))
sys.path.append(master)


from sandbox import camera_ip


def camera_gears(img_queue, kill_queue):
    print("Camera engine's gears rolling.")
    url_text = camera_ip.get_url()
    while True:
        if kill_queue.qsize():
            print("Camera engine out.")
            break
        try:
            response = requests.get(url_text)
            img = Image.open(BytesIO(response.content))
            img = numpy.array(img)
            if img.any():
                # print(" GOT a crispy img")
                img_queue.put(img, timeout=0.1)
        except queue.Full:
            # print("FULL", end="_")
            img_queue.get()
        except:
            print("CAM_ENGINE:isCAmON?".format(random.randint(0, 10)), end="+")
        time.sleep(0.2)
    return


def start_engine(img_queue, kill_queue):
    print("Camera engine in")
    p = multiprocessing.Process(target=camera_gears, args=(img_queue, kill_queue))
    p.start()
    p.join()
