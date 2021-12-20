# Varantsov Avetisyan Task 1.1

import random
while True:
	file1 = open("bmp280results.txt", "w")
	data = random.choices([13,14,13.5,15,16,21,22,23,25], [0.2, 0.2, 0.2,0.2,0.1, 0.1,0.05,0.05, 0.5])[0]
	file1.write(str(data))
	file1.close()
