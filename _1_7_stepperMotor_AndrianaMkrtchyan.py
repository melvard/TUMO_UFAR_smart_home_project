#task 1.7
import GPIO
from time import sleep
import sys

step = GPIO(21) # step GPIO pin
direction = GPIO(20) # direction GPIO pin
clockwise_rot = 1 # clockwise rotation
counter_clockwise_rot = 0 # counterclockwise rotation
steps_per_circle = 200 # steps per cycle (360 / 1.8)

mode = (14, 15, 18) # Microstep Resolution GPIO pins
GPIO.setup(mode, GPIO.out) # set three mode pins as outputs


resolution = {"Full" : (0, 0, 0),
"Half" : (1, 0, 0),
"1/4"  : (0, 1, 0),
"1/8"  : (1, 1, 0), 
"1/16" : (0, 0, 1),
"1/32" : (1, 0, 1)} # match te microstepy modes to the course by GPIO pin pattern

#////GPIO.output(mode, resolution["Half"]) # set mode to half step////

GPIO.setmode(GPIO.BCM) # set GPIO mode to BCM for Broadcom memory
GPIO.setup(direction, GPIO.out) # set direction pin to output
GPIO.setup(step, GPIO.out) # set the step in as an output


step_count = steps_per_circle # performs just one rotation

delay = 1/steps_per_circle # one over steps per cycle

def open_door(resolution_key):
  """

  :param resolution_key: possible values 'Full', 'Half', '1/4' , '1/8', '1/16', '1/32'
  :return:
  """
  values = resolution[resolution_key]
  GPIO.output(mode, values)  # set mode to half step
  GPIO.output(direction, clockwise_rot) # set the rotation direction to clockwise
  for i in range(step_count):
    GPIO.output(GPIO.high) # toggle the step pen high
    sleep(delay) # delay
    GPIO.output(GPIO.low) # toggle the step pen low
    sleep(delay) # delay

# sleep(0.5) # pause for half a second

def close_door(resolution_key):
  values = resolution[resolution_key]
  GPIO.output(mode, values)  # set mode to half step
  GPIO.output(direction, counter_clockwise_rot) # set the rotation direction to counterclockwise
  for i in range(step_count):
    GPIO.output(GPIO.high) # toggle the step pen high
    sleep(delay) # delay
    GPIO.output(GPIO.low) # toggle the step pen low
    sleep(delay) # delay


if __name__ == "__main__":
  function = sys.argv[0]
  resolution_ = sys.argv[1]

  if function == 1:
    open_window(resolution_)
  else:
    close_window(resolution_)
