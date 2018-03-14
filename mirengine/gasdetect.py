import time, sys
import RPi.GPIO as GPIO

class GasDetector:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
 
    def action(self,pin):
        print('Pin={}\nGas is detected and Alert is displayed by calling function!'.format(pin))
        return

    def detect(self):
        GPIO.add_event_detect(7, GPIO.RISING)
        GPIO.add_event_callback(7, self.action)
        while True:
            print('Detection on')
            time.sleep(0.5)

    def run_detector(self):
        while True:
            state=GPIO.input(7)
            if not state:
                print("Dafaq[{}]".format(state))
            else:
                print("cool[{}]".format(state))
            # print("{}->{} || ".format(7,))
            # state=GPIO.input(7)
            # print(state)
            time.sleep(1)


if __name__ == '__main__':
    GasDetector().run_detector()
