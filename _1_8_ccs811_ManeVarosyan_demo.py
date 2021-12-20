#We import I2C library which we can find in machine library
import random

while True:
  file1 = open("CCS811.txt", "w")
  data = random.choices([13,14,15,12,16, 24, 22], [10,10,10,10,10,1,1])[0]
  file1.write(str(data))
  file1.close()
