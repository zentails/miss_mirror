import threading
import time
import multiprocessing
import sys
import os

master = os.path.abspath(os.path.join(__file__, '..', '..'))
sys.path.append(master)

from sandbox import profiler, reflector

profile_killer = multiprocessing.Queue(maxsize=1)
profile_change_to=multiprocessing.Queue()
current_front=multiprocessing.Queue()

def run_profiler():
    profiler_thread_ln = threading.Thread(target=profiler.start_profiler, args=(profile_killer,current_front,profile_change_to))
    profiler_thread_ln.start()

    return profiler_thread_ln

def run_reflector():
    reflector_thread_ln = threading.Thread(target=reflector.start_reflector, args=(current_front,profile_change_to))
    reflector_thread_ln.start()

    return reflector_thread_ln


def kill_profiler():
    profile_killer.put_nowait(21)
    print("++++++PROFILER KILL SIG SENT+++++")


if __name__ == '__main__':
    print("________MASTER UP________")

    # reflector_thread= run_reflector()
    profiler_thread = run_profiler()

    time.sleep(2000)
    kill_profiler()

    profiler_thread.join()
    # reflector_thread.join()
    print("________MASTER DOWN________")
