# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
from adafruit_htu21d import HTU21D

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = HTU21D(i2c)

while True:
    my_file = open("HTU21results2.txt", "w")
    my_file.write("%0.1f" % sensor.temperature)
    my_file.write("%0.1f" % sensor.relative_humidity)
    my_file.close()


