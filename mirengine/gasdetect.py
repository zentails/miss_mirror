import time, sys
import RPi.GPIO as GPIO
 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
 
def action(pin):
    print('Gas is detected and Alert is displayed by calling function!')
    return
 
GPIO.add_event_detect(7, GPIO.RISING)
GPIO.add_event_callback(7, action)
 
try:
    while True:
        print('Detection on')
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()