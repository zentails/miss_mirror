import multiprocessing
import os
import threading
from io import BytesIO

import face_recognition
from PIL import Image
from numpy import array as numpy_array, collections
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
    print('>>>>{} faces from db loaded.'.format(len(decoded_faces)))
    face_names_local = decoded_faces.keys()
    return face_names_local, decoded_faces


class Recogniser:
    def __init__(self):
        self.reload_face_sig_q = multiprocessing.Queue(maxsize=1)
        self.profile_change_to_q = multiprocessing.Queue(maxsize=1)
        self.current_front_q = multiprocessing.Queue(maxsize=1)
        self.names_q = multiprocessing.Queue(maxsize=1)
        self.face_names, self.decoded_faces = load_faces_from_db()

    def engine(self):
        face_names, decoded_faces = load_faces_from_db()
        print("Recognise engine in.")
        url_text = mirtools.get_face_cam_url()
        while True:
            try:
                response = requests_get(url_text)
                img = Image.open(BytesIO(response.content))
                img = numpy_array(img)
                if img.any():
                    face_encodings = face_recognition.face_encodings(img)
                    for face_encoding in face_encodings:
                        res_raw = face_recognition.compare_faces(list(decoded_faces.values()), face_encoding)
                        if len(res_raw) > 0:
                            res = zip(res_raw, face_names)
                            for i, j in res:
                                if i:
                                    print("Camera Engine : ", j)
                                    self.names_q.put(j)
                            if not any(res_raw):
                                print("Camera Engine : Unknown")
                                self.names_q.put(False)
            except:
                # traceback.print_exc()
                print("Some problem in recognising process")

    def profiler(self):
        names = []
        while True:
            try:
                new_name = self.names_q.get(block=True)
                self.current_front_q.put(new_name)
                names.append(new_name)
                counter = collections.Counter(names)
                new = max(counter.keys(), key=(lambda key: counter[key]))
                print("NEW________profile___- {}".format(new))
                self.profile_change_to_q.put(new)
                while len(names) > 5:
                    names.pop()
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
        threading.Thread(target=self.reload_faces).start()
        threading.Thread(target=self.profiler)
        rec_process = multiprocessing.Process(target=self.engine())
        rec_process.start()
        return rec_process
