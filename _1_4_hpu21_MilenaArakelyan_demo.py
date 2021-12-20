# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import random

while True:
    my_file = open("HTU21results2.txt", "w")
    humidity = random.choices([300, 390,480,510,440,610,770,850,900], [0.2, 0.2, 0.2,0.2,0.1, 0.1,0.05,0.05, 0.5])[0]
    my_file.write(str(humidity))
    my_file.close()


