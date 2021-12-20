# Task 1.3

# Import smbus and time libraries
import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C Address of the device
HTU21D_DEFAULT_ADDRESS = 0x40

# HTU21D Command Set
HTU21D_MEAS_RH_HOLD = 0xE5  # Measure Relative Humidity, Hold Master Mode
HTU21D_MEAS_RH_NOHOLD = 0xF5  # Measure Relative Humidity, No Hold Master Mode
HTU21D_MEAS_TEMP_HOLD = 0xE3  # Measure Temperature, Hold Master Mode
HTU21D_MEAS_TEMP_NOHOLD = 0xF3  # Measure Temperature, No Hold Master Mode
HTU21D_READ_PREV_TEMP = 0xE0  # Read Temperature Value from Previous RH Measurement
HTU21D_RESET = 0xFE  # Reset
HTU21D_WRITERHT_REG = 0xE6  # Write RH/T User Register 1
HTU21D_READRHT_REG = 0xE7  # Read RH/T User Register 1
HTU21D_WRITEHEATER_REG = 0x51  # Write Heater Control Register
HTU21D_READHEATER_REG = 0x11  # Read Heater Control Register


# Write functions for writing values to the HTU21 registers and for reading values from registers
class HTU21D():
    def __init__(self):
        self.writetemperature()
        self.writehumidity()

    def writetemperature(self):
        """Select the temperature command from the given provided values"""
        bus.write_byte(HTU21D_DEFAULT_ADDRESS, HTU21D_MEAS_TEMP_NOHOLD)

    def readtemperature(self):
        """Read data back from the device address, 2 bytes, temperature MSB, temperature LSB"""
        d0 = bus.read_byte(HTU21D_DEFAULT_ADDRESS)
        d1 = bus.read_byte(HTU21D_DEFAULT_ADDRESS)

        # Convert the data
        cTemp = ((d0 * 256 + d1) * 175.72 / 65536.0) - 46.85

        return {'c': cTemp}

    def writehumidity(self):
        """Select the relative humidity command from the given provided values"""
        bus.write_byte(HTU21D_DEFAULT_ADDRESS, HTU21D_MEAS_RH_NOHOLD)

    def readhumidity(self):
        """Read data back from the device address, 2 bytes, humidity MSB, humidity LSB"""
        d0 = bus.read_byte(HTU21D_DEFAULT_ADDRESS)
        d1 = bus.read_byte(HTU21D_DEFAULT_ADDRESS)

        # Convert the data
        humidity = ((d0 * 256 + d1) * 125 / 65536.0) - 6

        return {'h': humidity}


from HTU21D import HTU21D

HTU21D = HTU21D()

# Open a file and write the results in it
while True:
    file1 = open("HTU21results.txt", "w")
    HTU21D.writehumidity()
    hum = HTU21D.readhumidity()
    file1.write("%.2f\n" % (hum['h']))
    HTU21D.writetemperature()
    temp = HTU21D.readtemperature()
    file1.write("%.2f\n" % (temp['c']))
    file1.close()