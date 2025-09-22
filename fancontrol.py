#! /usr/bin/env python3
import os
import time
import sys
sys.path.append('/storage/.kodi/addons/virtual.rpi-tools/lib')
os.environ['LG_WD'] = '/tmp'
from gpiozero import PWMOutputDevice


# Configuration
FAN_PIN = 14            # BCM pin used to drive PWM fan
WAIT_TIME = 2           # [s] Time to wait between each refresh
PWM_FREQ = 25           # [kHz] 25kHz for Noctua PWM control

# Configurable temperature and fan speed
MIN_TEMP = 42           # under this temp value fan is switched to the FAN_OFF speed
MAX_TEMP = 68           # over this temp value fan is switched to the FAN_MAX speed
FAN_LOW = 30            # lower side of the fan speed range during cooling
FAN_HIGH = 99           # higher side of the fan speed range during cooling
FAN_OFF = 20            # fan speed to set if the detected temp is below MIN_TEMP
FAN_MAX = 100           # fan speed to set if the detected temp is above MAX_TEMP

# Get CPU's temperature
def getCpuTemperature():
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
                return float(f.read()) / 1000

def setFanSpeed(speed):
                pwm_fan.value = speed/100  # divide by 100 to get values from 0 to 1
                return()

# Handle fan speed
def handleFanSpeed():
        temp = float(getCpuTemperature())
        #print("cpu temp: {}".format(temp))
        # Turn off the fan if temperature is below MIN_TEMP
        if temp < MIN_TEMP:
                setFanSpeed(FAN_OFF)
                #print("Fan OFF") # Uncomment for testing
        # Set fan speed to MAXIMUM if the temperature is above MAX_TEMP
        elif temp > MAX_TEMP:
                setFanSpeed(FAN_MAX)
                print("Fan MAX") # Uncomment for testing
        # Caculate dynamic fan speed
        else:
                step = (FAN_HIGH - FAN_LOW)/(MAX_TEMP - MIN_TEMP)
                temp -= MIN_TEMP
                setFanSpeed(FAN_LOW + ( round(temp) * step ))
                #print(FAN_LOW + ( round(temp) * step )) # Uncomment for testing
        return ()


try:
                pwm_fan = PWMOutputDevice(FAN_PIN, initial_value=0,frequency=PWM_FREQ) # initialize FAN_PIN as a pwm output
                setFanSpeed(FAN_OFF) # initially set fan speed to the FAN_OFF value
                while True:
                                handleFanSpeed() # call the function that calculates the target fan speed
                                time.sleep(WAIT_TIME) # wait for WAIT_TIME seconds before recalculate

except KeyboardInterrupt: # trap a CTRL+C keyboard interrupt
                setFanSpeed(FAN_HIGH)

finally:
   pwm_fan.close() # in case of unexpected exit, resets pin status (fan will go full speed after exiting)