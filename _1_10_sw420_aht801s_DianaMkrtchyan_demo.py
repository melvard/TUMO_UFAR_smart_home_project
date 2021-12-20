import random

while True:
	choice = random.choices([0,1],[10, 1])[0]
	file = open('sw420aht801s.txt', 'w')
	file.write(str(choice))
	file.close()


