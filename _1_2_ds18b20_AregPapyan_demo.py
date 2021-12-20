import random
import time
import os

while True:
    with open("DS18B20_results.txt", "w") as file:
        temperature = random.randint(10, 40)
        file.write(str(temperature))