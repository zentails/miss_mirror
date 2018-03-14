import os
import random
import urllib.request
from io import BytesIO

import face_recognition
import numpy as np
from PIL import Image
from numpy import array as numpy_array
from requests import get as requests_get

dir_path = os.path.dirname(os.path.realpath(__file__))


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def get_face_cam_url():
    """

    :return: returns the link of changing images that'll be used as video
             for our case it's from ipwebcam an android application used as replacement of raspberry cam
    """
    url = 'http://192.168.1.104:8080/shot.jpg'  # robin
    # url = 'http://192.168.1.105:8080/shot.jpg'  # platipus
    # url='http://192.168.43.220:8080/shot.jpg' #home
    # url='http://192.168.20.52:8080/shot.jpg'
    url = 'http://192.168.43.1:8080/shot.jpg'  # robin hotspot
    # url='http://192.168.28.115:8080/shot.jpg' #mobile hotspot shubham
    return url


def get_a_name(directory_name):
    directory_string = dir_path + directory_name
    directory = os.fsencode(directory_string)
    # print("Getting unique id")
    existing_names = []
    for file_ in os.listdir(directory):
        filename = os.fsdecode(file_)
        if filename.endswith(".jpg"):
            existing_names.append(filename[:-4])

    while True:
        rand = random.randint(1000, 99999)
        if str(rand) in existing_names:
            continue
        else:
            break
    return str(rand)


def take_profile_photo(id,reload_face_sig_q):
    url = get_face_cam_url()
    dropbox = dir_path + "/faces/"
    unique_name = id. + ".jpg"
    photo_path = dropbox + unique_name
    print(photo_path + url)

    while True:
        response = requests_get(url)
        img = Image.open(BytesIO(response.content))
        img = numpy_array(img)
        face_encodings = face_recognition.face_encodings(img)
        print(face_encodings)
        if len(face_encodings) > 0:
            data=img
            # Rescale to 0-255 and convert to uint8
            rescaled = (255.0 / data.max() * (data - data.min())).astype(np.uint8)

            im = Image.fromarray(rescaled)
            im.save(photo_path)
            break
    print("Took a photo with a face " + photo_path+"Reloading...faces..")
    reload_face_sig_q.put(1)
    reload_face_sig_q.put(1)
    return photo_path

    # urllib.request.urlretrieve(url, photo_path)
    # return photo_path, unique_name


def get_photo():
    url = get_face_cam_url()
    dropbox = dir_path + "/dropbox/"
    unique_name = get_a_name("/dropbox/") + '.jpg'
    photo_path = dropbox + unique_name
    print(photo_path + url)
    urllib.request.urlretrieve(url, photo_path)
    return photo_path, unique_name


if __name__ == '__main__':
    # print(get_photo())
    take_profile_photo("1")
