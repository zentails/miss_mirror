import threading

import time

import mirtools
import recogniser


def printWhenGet(q, m):
    print(">>printMan_{} in".format(m))
    while True:
        t = time.time()
        print("--##{}____{}____{}".format(m, time.time() - t, q.get(block=True)))


if __name__ == '__main__':
    print("________MASTER UP________")
    rec_obj = recogniser.Recogniser()

    reload_face_sig_q = rec_obj.reload_face_sig_q
    profile_change_to_q = rec_obj.profile_change_to_q
    current_front_q = rec_obj.current_front_q

    rec_processes = rec_obj.start_recogniser()
    # print(mirtools.get_photo())

    threading.Thread(target=printWhenGet, args=(current_front_q, "current")).start()
    threading.Thread(target=printWhenGet, args=(profile_change_to_q, "profile")).start()

    # rec_process.start()
    s = input("say")
    if s == "q":
        for rec_process in rec_processes:
            rec_process.terminate()
    print("________MASTER DOWN________")
