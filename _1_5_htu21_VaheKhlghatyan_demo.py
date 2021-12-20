import random

while True:
    HTUFile = open("HTU21results3.txt", "w")
    content = random.choices([100, 190,300,410,440,260,450,500,497], [0.2, 0.2, 0.2,0.2,0.1, 0.1,0.05,0.05, 0.5])[0]
    HTUFile.write(str(content))
    HTUFile.close()
