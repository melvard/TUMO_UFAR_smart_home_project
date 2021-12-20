import random
while True:
    # Open a file and write the results in it
    file = open("gy521mpu6050.txt" , "w")
    file.write("{}, {}, {} | {}, {}, {}".format(random.randint(-100,100), random.randint(-100,100), random.randint(-100,100),  random.randint(-100,100), random.randint(-100,100), random.randint(-100,100)))
    file.close()
