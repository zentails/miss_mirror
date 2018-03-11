import multiprocessing
import os
import queue
import threading
import traceback
from io import BytesIO

import face_recognition
import time
from PIL import Image
from collections import Counter
from numpy import array as numpy_array
from requests import get as requests_get

import mirtools


def load_faces_from_db():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    directory_string = dir_path + '/faces'
    directory = os.fsencode(directory_string)
    # Load the faces
    decoded_faces = {}
    print("Loading faces from database.")
    for file_ in os.listdir(directory):
        filename = os.fsdecode(file_)
        if filename.endswith(".jpg"):
            img_full_path = directory_string + '/' + filename
            # Load the jpg file into a numpy array
            image = face_recognition.load_image_file(img_full_path)
            image_face_encoding = face_recognition.face_encodings(image)[0]
            decoded_faces[filename[:-4]] = image_face_encoding
    print('[]{} faces from db loaded.'.format(len(decoded_faces)))
    face_names_local = decoded_faces.keys()
    return face_names_local, decoded_faces


class Recogniser:
    def __init__(self):
        self.photo_engine_thread = threading.Thread(target=self.photo_engine)
        self.profiler_thread = threading.Thread(target=self.profiler)
        self.reload_thead = threading.Thread(target=self.reload_faces)
        self.img_for_processing_q = multiprocessing.Queue(maxsize=4)
        self.reload_face_sig_q = multiprocessing.Queue(maxsize=1)
        self.profile_change_to_q = multiprocessing.Queue(maxsize=1)
        self.current_front_q = multiprocessing.Queue(maxsize=1)
        self.names_q = multiprocessing.Queue(maxsize=1)
        self.face_names, self.decoded_faces = load_faces_from_db()

    def photo_engine(self):
        url_text = mirtools.get_face_cam_url()
        i = 0
        while True:
            try:
                response = requests_get(url_text)
                img = Image.open(BytesIO(response.content))
                img = numpy_array(img)
                print("++++++putting img[{}]".format(i))
                time.sleep(2)
                self.img_for_processing_q.put((img, i), timeout=0.1)
                i += 1
            except:
                # traceback.print_exc()
                # print("img_Q_Q_FULL")
                self.img_for_processing_q.get()

    def engine(self):
        # face_names, decoded_faces = load_faces_from_db()
        print(">>{}  in.".format(multiprocessing.current_process().name))
        while True:
            try:
                # print("{}__waiting".format(multiprocessing.current_process().name))
                img, i = self.img_for_processing_q.get(block=True)
                # print("{}__is processing img{}".format(multiprocessing.current_process().name, i))
                face_encodings = face_recognition.face_encodings(img)
                for face_encoding in face_encodings:
                    # print("got Encodeings")
                    res_raw = face_recognition.compare_faces(list(self.decoded_faces.values()), face_encoding)
                    if len(res_raw) > 0:
                        res = zip(res_raw, self.face_names)
                        for i, j in res:
                            if i:
                                # print("__Camera Engine : ", j)
                                self.names_q.put(j)
                        if not any(res_raw):
                            # print("__Camera Engine : Unknown")
                            self.names_q.put(False)
            except:
                traceback.print_exc()
                print("Some problem in recognising process")

    def profiler(self):
        print(">>profiler IN")
        names = []
        last = "Whole"
        while True:
            try:
                new_name = self.names_q.get(block=True)
                self.current_front_q.put(new_name)
                names.append(new_name)
                counter = Counter(names)
                new = max(counter.keys(), key=(lambda key: counter[key]))

                # print(str(counter.keys()) + "\nNames:" + str(names))
                # print("NEW________profile___- {}".format(new))
                if not last == new:
                    self.profile_change_to_q.put(new)
                    last = new
                while len(names) > 3:
                    names = names[1:]
            except:
                pass

    def reload_faces(self):
        while True:
            self.reload_face_sig_q.get(block=True)
            self.face_names, self.decoded_faces = load_faces_from_db()

    def start_recogniser(self):
        """

        :return: rec process
        """
        rec_processes=[]
        for x in range(3):
            rec_process = multiprocessing.Process(target=self.engine, name="Recogniser {} ".format(x))
            rec_process.start()
            rec_processes.append(rec_process)
        self.reload_thead.start()
        self.profiler_thread.start()
        self.photo_engine_thread.start()
        return rec_processes
