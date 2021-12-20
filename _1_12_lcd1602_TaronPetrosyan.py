import smbus
import time

class LCD:
    def __init__(self, pi_rev = 2, i2c_addr = 0x3F, backlight = True):

        # device constants
        self.I2C_ADDR  = i2c_addr
        self.LCD_WIDTH = 16   # Max. characters per line

        self.LCD_CHR = 1 # Mode - Sending data
        self.LCD_CMD = 0 # Mode - Sending command

        self.LCD_LINE_1 = 0x80 # LCD RAM addr for line one
        self.LCD_LINE_2 = 0xC0 # LCD RAM addr for line two

        if backlight:
            # on
            self.LCD_BACKLIGHT  = 0x08
        else:
            # off
            self.LCD_BACKLIGHT = 0x00

        self.ENABLE = 0b00000100 # Enable bit

        # Timing constants
        self.E_PULSE = 0.0005
        self.E_DELAY = 0.0005

        # Open I2C interface
        if pi_rev == 2:
            # Rev 2 Pi uses 1
            self.bus = smbus.SMBus(1)
        elif pi_rev == 1:
            # Rev 1 Pi uses 0
            self.bus = smbus.SMBus(0)
        else:
            raise ValueError('pi_rev param must be 1 or 2')

        # Initialise display
        self.lcd_byte(0x33, self.LCD_CMD) # 110011 Initialise
        self.lcd_byte(0x32, self.LCD_CMD) # 110010 Initialise
        self.lcd_byte(0x06, self.LCD_CMD) # 000110 Cursor move direction
        self.lcd_byte(0x0C, self.LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
        self.lcd_byte(0x28, self.LCD_CMD) # 101000 Data length, number of lines, font size
        self.lcd_byte(0x01, self.LCD_CMD) # 000001 Clear display

    def lcd_byte(self, bits, mode):
        # Send byte to data pins
        # bits = data
        # mode = 1 for data, 0 for command

        bits_high = mode | (bits & 0xF0) | self.LCD_BACKLIGHT
        bits_low = mode | ((bits<<4) & 0xF0) | self.LCD_BACKLIGHT

        # High bits
        self.bus.write_byte(self.I2C_ADDR, bits_high)
        self.toggle_enable(bits_high)

        # Low bits
        self.bus.write_byte(self.I2C_ADDR, bits_low)
        self.toggle_enable(bits_low)

    def toggle_enable(self, bits):
        time.sleep(self.E_DELAY)
        self.bus.write_byte(self.I2C_ADDR, (bits | self.ENABLE))
        time.sleep(self.E_PULSE)
        self.bus.write_byte(self.I2C_ADDR,(bits & ~self.ENABLE))
        time.sleep(self.E_DELAY)

    def message(self, string, line = 1):
        # display message string on LCD line 1 or 2
        if line == 1:
            lcd_line = self.LCD_LINE_1
        elif line == 2:
            lcd_line = self.LCD_LINE_2
        else:
            raise ValueError('line number must be 1 or 2')

        string = string.ljust(self.LCD_WIDTH," ")

        self.lcd_byte(lcd_line, self.LCD_CMD)

        for i in range(self.LCD_WIDTH):
            self.lcd_byte(ord(string[i]), self.LCD_CHR)

    def clear(self):
        # clear LCD display
        self.lcd_byte(0x01, self.LCD_CMD)

import time

lcd = LCD() # params available for rPi revision, I2C Address, and backlight on/off
            # lcd = LCD(2, 0x3F, True)

lcd.message("Hello World!", 1) # display 'Hello World!' on line 1 of LCD

time.sleep(5) # wait 5 seconds

lcd.clear() # clear LCD displaylcd class
lcd = character_lcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,
                                      lcd_d7, lcd_columns, lcd_rows)

# looking for an active Ethernet or WiFi device
def find_interface():
    find_device = "ip addr show"
    interface_parse = run_cmd(find_device)
    for line in interface_parse.splitlines():
        if "state UP" in line:
            dev_name = line.split(':')[1]
    return dev_name

# find an active IP on the first LIVE network device
def parse_ip():
    find_ip = "ip addr show %s" % interface
    find_ip = "ip addr show %s" % interface
    ip_parse = run_cmd(find_ip)
    for line in ip_parse.splitlines():
        if "inet " in line:
            ip = line.split(' ')[5]
            ip = ip.split('/')[0]
    return ip

# run unix shell command, return as ASCII
def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output.decode('ascii')

# wipe LCD screen before we start
lcd.clear()

# before we start the main loop - detect active network device and ip address
sleep(2)
interface = find_interface()
ip_address = parse_ip()

while True:
    # date and time
    lcd_line_1 = datetime.now().strftime('%b %d  %H:%M:%S\n')
    # current ip address
    lcd_line_2 = "IP " + ip_address
    # combine both lines into one update to the display
    lcd.message = lcd_line_1 + lcd_line_2

