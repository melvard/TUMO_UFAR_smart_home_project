import random

while True:
    f = open("mpu6050results1.txt", "w")
    f.write("{}, {}, {}".format(random.randint(-100,100), random.randint(-100,100), random.randint(-100,100)))
    f.close()