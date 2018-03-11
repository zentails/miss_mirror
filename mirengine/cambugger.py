import multiprocessing
from io import BytesIO

import cv2
import numpy
import requests
from PIL import Image

import mirtools


class CameraDebugger:
    def start_debugger(self):
        p = multiprocessing.Process(target=self.debug)
        p.start()
        return p

    def debug(self):
        print("Camera debugger in.")
        url_text = mirtools.get_face_cam_url()
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
    CameraDebugger().start_debugger().join()
