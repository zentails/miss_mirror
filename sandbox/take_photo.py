import os
import random
import sys
import urllib.request

master = os.path.abspath(os.path.join(__file__, '..', '..'))
sys.path.append(master)


from sandbox import camera_ip


def get_a_name(dir):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    directory_string = dir_path + '/faces'
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


def get_photo():
    url = camera_ip.get_url()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dropbox = dir_path + "/dropbox/"
    unique_name = get_a_name(dropbox) + '.jpg'
    photo_path = dropbox + unique_name
    urllib.request.urlretrieve(url, photo_path)
    return photo_path, unique_name


if __name__ == '__main__':
    print(get_photo())
