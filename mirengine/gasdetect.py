import threading
import time, sys
import RPi.GPIO as GPIO


class GasDetector:
    def __init__(self, master_obj):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.master_object = None

    def action(self, pin):
        print('Pin={}\nGas is detected and Alert is displayed by calling function!'.format(pin))
        return

    def detect(self):
        print(">>Smoke Detector IN")
        while True:
            state = GPIO.input(7)
            if not state:
                # print("Dafaq[{}]".format(state))
                print("Warninig : Smoke Sensed")
                if self.master_object:
                    self.master_object.show_log("Warninig : Smoke Sensed", 10, True)
                # print("cool[{}]".format(state))
            # print("{}->{} || ".format(7,))
            # state=GPIO.input(7)
            # print(state)
            time.sleep(1)

    def run_detector(self):
        threading.Thread(target=self.detect).start()


if __name__ == '__main__':
    GasDetector().run_detector()
    # GasDetector().detect()
