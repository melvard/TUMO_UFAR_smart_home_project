# Ani Markosyan Task 2.2  
# GY-521 MPU 6050

#import the time, board 
#import adafruit_mpu6050 library

import time
import board
import adafruit_mpu6050

#create an instance i2c with the help of board()
i2c = board.I2C()   # uses board.SCL and board.SDA


mpu = adafruit_mpu6050.MPU6050(i2c)

#with  the help of "while" loop our programm register all the addresses that we need

while True:
    # Open a file and write the results in it
    file = open("gy521mpu6050.txt" , "w")
    file.write("%.2f, %.2f, %.2f\n" % (mpu.acceleration))
    file.write("%.2f, %.2f, %.2f\n " % (mpu.gyro))
    file.write("%.2f \n" % mpu.temperature)
    file.close()
