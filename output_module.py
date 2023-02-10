import datetime
import importlib.util
import curses
import time

try:
    importlib.util.find_spec('RPi.GPIO')
    import RPi.GPIO as GPIO
    print("GPIO imported")
except ImportError:
    """
    import FakeRPi.GPIO as GPIO
    OR
    import FakeRPi.RPiO as RPiO
    """

    import FakeRPi.GPIO as GPIO
    print("FAKE GPIO imported")


led_waiting_time = 1
last_led_time = False
led_on = False
LED_PIN = 17

win = curses.initscr()

def output_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    print("OUTPUT FOUND")


def test_output():
    print("BLINKING")
    for i in range(10):
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(1)
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(1)
    print("STOPPED BLINKING")


def output_test(b, m):
    global last_led_time, led_waiting_time
    now = datetime.datetime.now()
    if last_led_time:
        if((now - last_led_time).seconds < led_waiting_time):
            win.addstr("WAITING")
            return
        else:
            win.clear()
            if(b):
                last_led_time = now
                win.addstr('\n[★]' + str(m) + "ON")
            else:
                win.addstr('\n[☆]' + str(m) + "OFF")
            win.refresh()
    else:
        win.clear()
        if(b):
            last_led_time = now
            win.addstr('\n[★]' + str(m) + "ON")
        else:
            win.addstr('\n[☆]' + str(m) + "OFF")
        win.refresh()
        

    # if(b):
    #     print("OK")
    # else:
    #     print("NO")
    # # win.refresh()
    # # n = m//TARA
    # win.addstr('Signal: ' + str(m))
    # if(b):
    #         if((now - last_led_time).seconds < led_waiting_time):
    #             # win.addstr("NO")
    #             return
    #         else:
    #             # win.addstr("SI")
    #             last_led_time
    #     win.addstr('\n[★]' + str(m))
    #     win.refresh()
    # else:
    #     win.addstr('\n[☆]' + str(m))
    #     win.refresh()

def output_led(b, m):
    global last_led_time, led_waiting_time, led_on
    print("OUTPUT: TRUE")
    now = datetime.datetime.now()
    if(last_led_time):
        if((now - last_led_time).seconds < led_waiting_time):
            # print("waiting last led animation")
            return
    if(b):
        if(not led_on):
            # print(f'[★]', end='\r')
            GPIO.output(LED_PIN, GPIO.HIGH)
            led_on = True
        last_led_time = now
    else:
        if(led_on):
            # print(f'[☆]', end='\r')
            GPIO.output(LED_PIN, GPIO.LOW)
            led_on = False

print("1/4 OUTPUT MODULE LOADED")