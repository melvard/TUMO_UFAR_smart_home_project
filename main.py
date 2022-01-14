# This project is to demonstrate how theoretically smart house should work on RaspberryPi
# using sensors and Python as main language to develop whole life cycle.

# This is the main file where whole application will be managed and will work.

# importing all the necessary libraries for controlling all corresponding sensors for further usage

from subprocess import Popen, PIPE, check_output
import threading
import time
import sys

import _1_7_stepperMotor_AndrianaMkrtchyan_demo as StepperMotor
import _1_12_lcd1602_TaronPetrosyan_demo as LCD_Display

interpreter = sys.executable
door_is_open = False
heating_is_on= False
watering_is_on = False

password = ""
password_unlocked = False


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


measurements = {
    "AirPressure": None,
    "Temperature (C)": None,
    "AirHumidity (%%)": None, # here we need only first line (humidity) - %%
    "SoilHumidity (%%)": None, # here we need only first line (humidity) - %%
    "AdditionalHumidity (%%)": None, # here we need only first line (humidity) - %%
    "GyroscopeAccelerometer1 (x,y,z)": None,
    "AirQuality (CO2)": None,
    "WaterCost": None,
    "Current (A)": None,
    "GyroscopeAccelerometer2 (x,y,z)": None,
    "Accelerometer (m/s^-1)": None,
    "Vibration": None, # if vibration is 1 then it is an earthquake, then print warning
    "WindowIsOpen" : door_is_open,
    "HeatingIsOn" : heating_is_on
}

sensors_and_txtFiles = {
    "AirPressure":"bmp280results.txt",
    "Temperature (C)": "DS18B20_results.txt",
    "AirHumidity (%%)": "HTU21results1.txt",
    "SoilHumidity (%%)": "HTU21results2.txt",
    "AdditionalHumidity (%%)": "HTU21results3.txt",
    "GyroscopeAccelerometer1 (x,y,z)": "mpu6050results1.txt",
    "AirQuality (CO2)": "CCS811.txt",
    'Vibration' : "sw420aht801s.txt",
    "WaterCost": "flowMeter.txt",
    "Current (A)": "acs712.txt" ,
    "GyroscopeAccelerometer2 (x,y,z)": "gy521mpu6050.txt",
    "Accelerometer (m/s^-1)": "adxl335.txt"
}


def is_earthquake():
    data = measurements["Vibration"]
    if None != data:
        return float(data) == 1
    return False

def is_hot():
    data = measurements["Temperature (C)"]
    if None != data:
        return float(data) > 30
    return False

def is_temp_normal():
    data = measurements["Temperature (C)"]
    if None != data:
        return 24 < float(data) < 27 # if the temperature is between two limits then turn off heating
    return False

def is_cold():
    data = measurements["Temperature (C)"]
    if None != data:
        return float(data) < 20
    return False


def is_air_clean():
    data = measurements["AirQuality (CO2)"]
    if None != data:
        return float(data) <= 20 # if part of Co2 in air is more than 20%, then conditioning needed
    return True

def is_air_wet():
    data = measurements["AirHumidity (%%)"]
    if None != data:
        return float(data.split('\n')[0]) > 500 # if humidity of air is more than 500%% then heating is needed
    return False

def is_air_dry():
    data = measurements["AirHumidity (%%)"]
    if None != data:
        return float(data.split('\n')[0]) < 200 # if humidity of air is less than 200%%, then air conditioning needed
    return False

def plants_need_watering():
    data = measurements["SoilHumidity (%%)"]
    if None != data:
        return  float(data.split('\n')[0]) < 400 # if the humidity of soil is less than 400 %%, then inform that watrering is  needed
    return False

def plants_are_watered_enough():
    data = measurements["SoilHumidity (%%)"]
    if None != data:
        return float(data.split('\n')[0]) >800  # if the humidity of soil is mote than 800 %%, then stop watering
    return False

def control_sensors():
    global door_is_open
    global heating_is_on
    global password_unlocked
    global watering_is_on

    if is_earthquake():
        print(bcolors.WARNING + "!!! Earthquake detected !!!\n!!! Earthquake detected !!!\n!!! Earthquake detected !!!\n" + bcolors.ENDC)

    if (is_earthquake()  or is_air_dry() or is_hot() or not is_air_clean()) and door_is_open != True:
        door_is_open = True
        StepperMotor.open_door('1/4')

    # if everything is okay then close door
    if not is_earthquake():
        if is_air_clean():
            if not is_hot():
                if not is_air_dry():
                    if door_is_open:
                        StepperMotor.close_door('1/4')
                        door_is_open = False

    if is_cold() or is_air_wet() and not heating_is_on:
        # turn on heating
        print(bcolors.FAIL+"Turning on heating"+bcolors.ENDC)
        heating_is_on = True

    if is_hot() and not is_air_wet() and heating_is_on:
        # turn off heating
        print(bcolors.FAIL+"Turning off heating"+bcolors.ENDC)
        heating_is_on = False

    if plants_need_watering() and not watering_is_on:
        watering_is_on = True
        print(bcolors.OKCYAN+"Turning on plants watering"+bcolors.ENDC)

    if plants_are_watered_enough() and watering_is_on:
        watering_is_on = False
        print(bcolors.OKCYAN+"Turning off plants watering"+bcolors.ENDC)

# def file_is_opened():
#     is_opened = True
#     try:
#         lsout = Popen(['lsof', "a.txt"], stdout=PIPE, shell=False)
#         check_output(["grep", "a.txt"], stdin=lsout.stdout, shell=False)
#     except:
#         is_opened = False
#         return False
#     return  is_opened

passed_iterations_LCD = 0
data_turn = 1

def read_sensors_data():
    sensorDataCheckDelay = 1
    lastTime = time.time()
    delay_to_show_on_lcd_display = 5
    global passed_iterations_LCD
    global data_turn
    pass_count = delay_to_show_on_lcd_display / sensorDataCheckDelay

    while True:
        # non blocking sleep instead of using time.sleep() which will also pause the execution of subprocesses
        while time.time() <= lastTime + sensorDataCheckDelay:
            continue

        count = 0
        for sensor in sensors_and_txtFiles.keys():
            count +=1

            txtFile = sensors_and_txtFiles[sensor]
            try:
                file = open(txtFile, 'r')
            except FileNotFoundError:
                # print(f"File {txtFile} doesn't exist, passing by...")
                continue
            data = file.read()
            if "" !=data:
                measurements[sensor] = data
            file.close()
            print(f"{sensor}: {measurements[sensor]}")
            if passed_iterations_LCD == pass_count and count == data_turn:
                passed_iterations_LCD = 0
                data_turn +=1
                if data_turn >=len(sensors_and_txtFiles):
                    data_turn = 1
                if password_unlocked:  # as password unlocked the LCD display will show data
                    message = f"LCD : {sensor}: {measurements[sensor]}"
                    LCD_Display.send_message(bcolors.OKGREEN + message + bcolors.ENDC)
                # else:
                #     LCD_Display.clear_display()
        print()
        passed_iterations_LCD += 1
        control_sensors()
        lastTime = time.time()



sensorReadThread = threading.Thread(target=read_sensors_data)

def is_password_correct(pswd):
    default_pass = "123567"
    return pswd == default_pass



def start():

    sensorReadThread.start()

    # Here we will create new subprocesses and start them independently for keypad, vibration sensor and stepper motor
    # as the motor is always working independently we will run it in the other process

    # here we are running only the demo versions of sensors, remove '_demo' part to run original files

    AirPressure = Popen([interpreter, '_1_1_bmp280_VarantsAvetisyan_demo.py'])
    Temperature = Popen([interpreter, '_1_2_ds18b20_AregPapyan_demo.py'])
    HumidityTemperature1 = Popen([interpreter, '_1_3_htu21_AgnesaMartirosyan_demo.py'])
    HumidityTemperature2 = Popen([interpreter, '_1_4_hpu21_MilenaArakelyan_demo.py'])
    HumidityTemperature3 = Popen([interpreter, '_1_5_htu21_VaheKhlghatyan_demo.py'])
    GyroscopeAccelerometer1 = Popen([interpreter, '_1_6_gy521_mpu6050_AnnaVarosyan_demo.py'])
    AirQualitySensor = Popen([interpreter, '_1_8_ccs811_ManeVarosyan_demo.py'])
    Keypad = Popen([interpreter, '_1_9_keypad_HaykBadalyan_demo.py'], stdout=PIPE, shell=False)
    Vibration = Popen([interpreter, '_1_10_sw420_aht801s_DianaMkrtchyan_demo.py'])
    FlowMeter = Popen([interpreter, '_1_11_flowMeter_Sergey_Boyakhchyan_demo.py'])
    LCDDisplay = Popen([interpreter, '_1_12_lcd1602_TaronPetrosyan_demo.py'])
    CurrentMeasureSensor = Popen([interpreter, '_2_1_acs712_Arman_Azizyan_demo.py'])
    GyroscopeAccelerometer2 = Popen([interpreter, '_2_2_gy521_mpu6050_AniMarkosyan_demo.py'])
    Accelerometer = Popen([interpreter, '_2_3_adxl335__AstghikBoyajyan_demo.py'])

    global password
    global password_unlocked

    while True:
        # communicate with keypad and print pressed key values
        keyPressed = Keypad.stdout.readline().decode()[0]
        if keyPressed:
            if keyPressed not in ['A', 'B']:
                if keyPressed == 'C':
                    password_unlocked = False
                elif keyPressed == 'D':
                    if is_password_correct(password):
                        print(bcolors.OKGREEN+"Correct Password"+bcolors.ENDC)
                        password_unlocked = True
                    else:
                        print(bcolors.FAIL +"Wrong door password"+bcolors.ENDC)
                    password = ""
                else:
                    # clear inserted password
                    password += keyPressed
            else:
                password = ""
        # end keypad checking

start_thread = threading.Thread(target=start)
start_thread.start()
