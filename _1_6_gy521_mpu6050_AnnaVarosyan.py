"""
Anna Varosyan
Task: [1.6]
GY-521 MPU 6050
(3 axis gyroscope and accelerometer)

"""

# import the time and the smbus2 library

import time 
import smbus2

#assign variables to all the register addresses

PWR_MGT_1 = 0x6B
CONFIG = 0x1A
SAMPLE_RATE = 0x19
GYRO_CONFIG = 0x1B
ACCEL_CONFIG = 0x1C
ACCEL_X_HIGH = 0x3B
ACCEL_Y_HIGH = 0x3D
ACCEL_Z_HIGH = 0x3F
GYRO_X_HIGH = 0x43
GYRO_Y_HIGH = 0x45
GYRO_Z_HIGH = 0x47
TEMP_OUT_HIGH = 0x41

# For writing values to the MPU6050 registers.
# The "bus.write_byte_data()" will take the device address, register address and value to 
# be written as parameters. In this function, we write into all the necessary registers of the MPU6050.

def MPU_initialization():
    bus.write_byte_data(Device_Address, PWR_MGT_1, 1)
    bus.write_byte_data(Device_Address, SAMPLE_RATE, 7)
    bus.write.byte.data(Device_Address, CONFIG, 0)
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)

# read values from the registers
# The second function is used to pass the register address, and will return the value 
# in present in the register. Since both, the accelerometer and gyroscope digitize the 
# output using 16-bit ADC's, the values are stored in a set of 2, 8-bit registers with consecutive addresses.

def Read_data(reg_add):
    high = bus.read_byte_data(Device_Address, reg_add)
    low = bus.read_byte_data(Device_Address, reg_add+1)
    value = (high<<8)|low
    if value>35768:
        value = value-65536
    return value

# REGARDING 65536
# The values stored by these registers is in 2's complement form. 
# So to display the signed value, we subtract the concatenated value with 65536.

#  create an instance called 'bus' using the smbus.SMBus() class.

bus = smbus2.SMBus(1)
Device_Address = 0x68
MPU_initialization()

# Inside the 'while 1' loop, we pass the higher register addresses for accelerometer and 
# gyroscope axis as well as for temperature. The received values are then divided by the 
# respective sensitivity factor based on the full scale setting. The scale factor for accelerometer and 
# gyroscope is 16384 and 131 respectively for full scale setting of �2g and �250�/s as per datasheet.
# For temperature, the value in degrees can be obtained by T = (Register value/340)+36.53

while True:
    ACCEL_X = Read_data(ACCEL_X_HIGH)
    ACCEL_Y = Read_data(ACCEL_Y_HIGH)
    ACCEL_Z = Read_data(ACCEL_Z_HIGH)
    GYRO_X = Read_data(GYRO_X_HIGH)
    GYRO_Y = Read_data(GYRO_Y_HIGH)
    GYRO_Z = Read_data(GYRO_Z_HIGH)
    TEMP = Read_data(TEMP_OUT_HIGH)

    Ax = ACCEL_X/16384.0
    Ay = ACCEL_Y/16384.0
    Az = ACCEL_Z/16384.0

    Gx = GYRO_X/131.0
    Gy = GYRO_Y/131.0
    Gz = GYRO_Z/131.0

    T = (TEMP/340)+36.53

    f = open("mpu6050results1.txt", "w")
    f.write("%.2f" %Ax, "%.2f\t" %Ay, "%.2f"%Az, "\n")
    f.write("%.2f" %Gx, "%.2f\t" %Gy, "%.2f" %Gz, "\n")
    f.write("%.2f" %T, "\n")

    time.sleep(1)
    f.close()