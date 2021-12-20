import time
import Adafruit_HTU21D.HTU21D as HTU21D

# Default constructor will pick a default I2C bus.
# For the Raspberry Pi this means we should hook up to the only exposed I2C bus
# from the main GPIO header and the library will figure out the bus number based on the Pi's revision.


sensor = HTU21D.HTU21D()

# Optionally we can override the bus number:
#sensor = HTU21D.HTU21D(busnum=2)
# HTU21D communication mode can be set to one of HTU21D_HOLDMASTER and HTU21D_NOHOLDMASTER.
# Actually only HTU21D_NOHOLDMASTER is supported.
#sensor = HTU21D.HTU21D(mode=HTU21D.HTU21D_HOLDMASTER)

get_temp = "{0:0.2f}\n".format(sensor.read_temperature())
get_hum = "{0:0.2f}\n".format(sensor.read_humidity())
get_DP="{0:0.2f}\n".format(sensor.read_dewpoint())

while True:
    HTUFile = open("HTU21results3.txt", "w")
    HTUFile.write(get_temp) # \n is missing , explain to Vahe why we need it
    HTUFile.write(get_hum)
    HTUFile.write(get_DP)
    time.sleep(1)
    HTUFile.close()
    sensor.reset()
