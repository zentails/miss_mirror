import collections
import multiprocessing
import os
import sys
import threading
import time

master = os.path.abspath(os.path.join(__file__, '..', '..'))
sys.path.append(master)


from sandbox import camera_engine, recognise_engine


def start_profiler(profiler_kill,current_front, profile_change_to):
    print("Profiler in.")
    img_queue = multiprocessing.Queue(maxsize=1)
    kill_queue = multiprocessing.Queue(maxsize=5)

    # Camera start
    camera_thread = threading.Thread(target=camera_engine.start_engine, args=(img_queue, kill_queue))
    camera_thread.start()

    # Recognizer
    names_queue = multiprocessing.Queue(maxsize=5)
    recogniser_process = multiprocessing.Process(target=recognise_engine.start_engine,
                                                 args=(names_queue, img_queue, kill_queue))
    recogniser_process.start()
    names = []
    while True:
        if profiler_kill.qsize():
            kill_queue.put_nowait(21)
            break
        time.sleep(0.2)
        try:
            new_name=names_queue.get(timeout=4)
            current_front.put(new_name)
            names.append(new_name)
            # print(names)
            counter = collections.Counter(names)
            # print(counter)
            new=max(counter.keys(), key=(lambda key: counter[key]))
            print("NEW________profile___- {}".format(new))
            profile_change_to.put(new)
            if len(names) > 5:
                names.pop()
        except:
            pass

    print("profiler waiting for others to die")

    recogniser_process.join()
    print("recogniser_process out")

    camera_thread.join()
    print("camera_thread out")

    print("Profiler out.")
