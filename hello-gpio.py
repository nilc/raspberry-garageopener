# -*- coding: utf-8 -*-
from flask import Flask, render_template
import datetime
import time
import RPi.GPIO as GPIO
import threading
app = Flask(__name__)

servo_pin = 26
start_pos = 9

servolock = threading.Lock()


@app.route("/")
def hello():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title': 'HELLO!',
        'time': timeString
    }
    return render_template('main.html', **templateData)


@app.route("/press/<duty>", methods=["POST"])
def press(duty):
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")

    templateData = {
        'status': u'Redan upptagen med att trycka på knappen',
        'time': timeString
    }
    if servolock.acquire(False):
        pwm_servo.ChangeDutyCycle(float(duty))
        print("setting changeduty to " + duty)
        time.sleep(.20)
        print('setting changedu to ' + str(start_pos))
        pwm_servo.ChangeDutyCycle(start_pos)
        time.sleep(.10)
        pwm_servo.ChangeDutyCycle(0)
        templateData = {
            'status': u'Tryckte på knappen med styrka:' + duty,
            'time': timeString
        }
        servolock.release()
    return render_template('status.html', **templateData)


if __name__ == "__main__":
    print("bajskorv:")
    # Configure the Pi to use pin names (i.e. BCM) and allocate I/O
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servo_pin, GPIO.OUT)
    # Create PWM channel on the servo pin with a frequency of 50Hz
    pwm_servo = GPIO.PWM(servo_pin, 50)
    pwm_servo.start(start_pos)
    time.sleep(0.30)
    pwm_servo.ChangeDutyCycle(0)
    print("started server")

    app.run(host='0.0.0.0', port=80, debug=True)
    print("Cleaning up GPIO...")
    GPIO.cleanup()
