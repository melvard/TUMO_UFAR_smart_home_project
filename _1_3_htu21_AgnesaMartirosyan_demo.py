# Task 1.3
import random

while True:
    file1 = open("HTU21results1.txt", "w")
    humidity = random.choices([100, 190,300,410,440,260,450,500,497], [0.2, 0.2, 0.2,0.2,0.1, 0.1,0.05,0.05, 0.5])[0]
    file1.write(str(humidity))
    file1.close()