#Areg Papyan Task 1.2
import time
from w1thermsensor import W1ThermSensor

sensor = W1ThermSensor()

while True:
    file1 = open("DS18B20_results.txt", "w")
    temperature = sensor.get_temperature()
    file1.write(str(temperature))
    file1.close()