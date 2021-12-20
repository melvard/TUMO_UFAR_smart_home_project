#We import I2C library which we can find in machine library
from machine import I2C
import time

#define our function, i2c bus
i2c = I2C(0)
#define as master
i2c = I2C(0, I2C.MASTER)
#define which pins we are going to use, so we are using P9 for SDA, and P10 for SCL. 
i2c = I2C(0, pins =('P9','P10' ) )
#then, we start the bus init, and we'll use a baudrate of 10000
i2c.init(I2C.MASTER, baudrate = 10000)
#after we can write i2c.scan()
#and in this case we should find the sensor and if we read the documentation of this sensor it can either be 90or91 
 

#for communicating with this sensor we need library
import CCS811
#define ccs 
ccs = CCS811.CCS811(i2c = i2c, addr = 91)

while True:
  file1 = open("CCS811.txt", "w")
  ccs.data_ready()
  # co2 level
  co2 = ccs.eCO2
  voc = ccs.tVOC
  if co2 > 0:
    file1.write(str(co2))
  file1.close()
