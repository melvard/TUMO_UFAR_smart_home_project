import Rpi.GPIO as GPIO
import time

# GPIO setup

channel = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change


def callback(channel):
	file = open('sw420aht801s.txt', 'w')
	if GPIO.input(channel):
		file.write("1")
	else:
		file.write('0')
	file.close()




