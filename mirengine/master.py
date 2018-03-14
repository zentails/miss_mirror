import multiprocessing
import threading

import time

import mirtools
import recogniser
import reflector


def printMan(m, t):
    while True:
        print("{}_{}".format(t, m))
        time.sleep(m)


def profile_current_man(q, w):
    print(">>Profile Current Man in")
    while True:
        tx = q.get(block=True)
        print("--##------------>{}".format(tx))
        w(tx)


def reflectorRun(widget):
    app = reflector.ReflectorApp(widget)
    reflector_thread = threading.Thread(target=app.run)
    reflector_thread.start()
    return reflector_thread


if __name__ == '__main__':
    print("________MASTER UP________")

    # Faace Reccogniser Part
    rec_obj = recogniser.Recogniser()
    reload_face_sig_q = rec_obj.reload_face_sig_q
    profile_change_to_q = rec_obj.profile_change_to_q
    current_front_q = rec_obj.current_front_q
    rec_processes = rec_obj.start_recogniser()

    # Reflector Part
    reflector_widget = reflector.ReflectorWidget()
    # reflector_widget.set_profiler_text()
    # profiler_text,current_text=reflector_widget.get_profiler_current_text()

    threading.Thread(target=profile_current_man, args=(current_front_q, reflector_widget.set_current_text)).start()
    threading.Thread(target=profile_current_man, args=(profile_change_to_q, reflector_widget.set_profiler_text)).start()
    threading.Thread(target=printMan, args=(2, "____________________________-_______________________")).start()

    reflector.ReflectorApp(reflector_widget).run()
    print("________MASTER DOWN________")
