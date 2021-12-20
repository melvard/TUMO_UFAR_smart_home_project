import random
while True:
    file = open("adxl335.txt", 'w')
    file.write("{}, {}, {}".format(random.randint(-100,100), random.randint(-100,100), random.randint(-100,100)))
    file.close()