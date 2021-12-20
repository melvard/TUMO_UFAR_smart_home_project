#!/usr/bin/python3
import random

while True:
    file = open("acs712.txt", 'w')
    data = random.randint(100, 200)
    file.write(str(data))
    file.close()
