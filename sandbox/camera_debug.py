import cv2
import numpy
import requests
import sys
import os
from PIL import Image
from io import BytesIO

master = os.path.abspath(os.path.join(__file__, '..', '..'))
sys.path.append(master)


from sandbox import camera_ip


def start_debugger():
    print("Camera debugger in.")
    url_text = camera_ip.get_url()
    while True:
        response = requests.get(url_text)
        pil_img = Image.open(BytesIO(response.content)).convert('RGB')
        open_cv_image = numpy.array(pil_img)
        # cv2.imshow('Camera num', open_cv_image)
        # Convert RGB to BGR
        final_img = open_cv_image[:, :, ::-1].copy()
        cv2.imshow('Camera Debugger', final_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    print("Camera debugger out.")


if __name__ == '__main__':
    start_debugger()
