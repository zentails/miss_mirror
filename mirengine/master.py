import threading

import mirtools
import recogniser


def printWhenGet(q, m):
    print(">>printMan_{} in".format(m))
    while True:
        print("--##{}____{}".format(m, q.get(block=True)))


if __name__ == '__main__':
    print("________MASTER UP________")
    rec_obj = recogniser.Recogniser()
    rec_process = rec_obj.start_recogniser()

    reload_face_sig_q = rec_obj.reload_face_sig_q
    profile_change_to_q = rec_obj.profile_change_to_q
    current_front_q = rec_obj.current_front_q

    # print(mirtools.get_photo())

    threading.Thread(target=printWhenGet, args=(current_front_q, "current")).start()
    threading.Thread(target=printWhenGet, args=(profile_change_to_q, "profile")).start()

    rec_process.start()
    rec_process.join()


    while True:
        s = input("say")
        if s=="q":
            rec_process.terminate()
            break
    print("________MASTER DOWN________")
