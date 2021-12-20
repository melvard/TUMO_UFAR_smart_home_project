# Sergey Boyakhchyan Task 1.11
from datetime import datetime
from RPi import GPIO
import time, sys

# import paho.mqtt.publish as publish


FLOW_SENSOR_GPIO = 13
# MQTT_SERVER = "192.168.1.220"

GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOW_SENSOR_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

global count
count = 0


def countPulse(channel):
    global count
    if start_counter == 1:
        count = count + 1


GPIO.add_event_detect(FLOW_SENSOR_GPIO, GPIO.FALLING, callback=countPulse)



while True:
    try:
        # "flowMeter.txt"
        start_counter = 1
        time.sleep(1)
        start_counter = 0
        m_sum = 0
        counter = 0
        average = 0
        fixed_time = time.time()

        while True:
            if time.time() < (fixed_time + 60):
                flow = (count / 7.5)  # Pulse frequency (Hz) = 7.5Q, Q is flow rate in L/min.
                m_sum += flow
                counter+=1

        average = m_sum / counter
        file = open("flowMeter.txt",'w')
        file.write(str(average))
        file.close()
        # publish.single("/Garden.Pi/WaterFlow", flow, hostname=MQTT_SERVER)
        count = 0
        time.sleep(5)
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit()

# Line 1-13: Imports and definitions
# Lines 15-18: Function that is called when the voltage applied to the GPIO changes
# Line 20: Definition of which function should be called (from HIGH to LOW -> also FALLING)
# Line 22: Infinite loop
# Lines 24-27: First we “activate” the counter (start_counter = 1) and then wait a second. Then we deactivate the counter again and calculate the flow per minute.
# Optional (lines 4, 7, 29): If we want to send the result via MQT
å


