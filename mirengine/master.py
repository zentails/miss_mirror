import multiprocessing
import threading

import time

import mirtools
import recogniser


def printMan(m, t):
    while True:
        print("{}_{}".format(t, m))
        time.sleep(m)


def printWhenGetCurrent(q):
    print(">>printManCurrent in")
    # a = 1
    while True:
        # t = time.time()
        print("--##________{}________________".format(q.get(block=True)))
        # t = a + (time.time() - t)
        # a = t / 2


def printWhenGetProfile(q):
    print(">>printManProfile in")
    while True:
        print("--##------------>{}".format(q.get(block=True)))


if __name__ == '__main__':
    print("________MASTER UP________")
    rec_obj = recogniser.Recogniser()

    reload_face_sig_q = rec_obj.reload_face_sig_q
    profile_change_to_q = rec_obj.profile_change_to_q
    current_front_q = rec_obj.current_front_q

    rec_processes = rec_obj.start_recogniser()
    # print(mirtools.get_photo())

    threading.Thread(target=printWhenGetCurrent, args=(current_front_q,)).start()
    threading.Thread(target=printWhenGetProfile, args=(profile_change_to_q,)).start()
    threading.Thread(target=printMan, args=(2, "____________________________-_______________________")).start()

    # rec_process.start()
    s = input("say")
    if s == "q":
        for rec_process in rec_processes:
            rec_process.terminate()
        multiprocessing.current_process().terminate()
    print("________MASTER DOWN________")
