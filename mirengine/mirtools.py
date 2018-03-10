import os
import random
import urllib.request

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
    url = 'http://192.168.1.104:8080/shot.jpg'  # home
    # url='http://192.168.43.220:8080/shot.jpg' #home
    # url='http://192.168.20.52:8080/shot.jpg'
    # url='http://192.168.43.1:8080/shot.jpg' #mobile hotspot
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


def get_photo(self):
    url = get_face_cam_url()
    dropbox = dir_path + "/dropbox/"
    unique_name = self.get_a_name("/dropbox/") + '.jpg'
    photo_path = dropbox + unique_name
    print(photo_path + url)
    urllib.request.urlretrieve(url, photo_path)
    return photo_path, unique_name


if __name__ == '__main__':
    # print(get_photo())
    pass
