"""
 Python3 CAN Bus Simulator
 Accepts keyboard inputs and 
 Sends signals to a socketcan,
 virtual CAN, vcan0 interface.

 Used for sending simulated vehicular signals
 Such as speed and turn signals.

Created by: savavel
Last Edited: 10 May, 2018
"""

from pynput import keyboard
import socket
import can
import time
import _thread
import json
import ssl

# Can bus configuraation

can.rc['interface'] = 'socketcan'
can.rc['channel'] = 'vcan0'
can.rc['bitrate'] = 1000000

# Declare interface
bus = can.interface.Bus()


"""
 Handle special key presses
 Depending on the key pressed,
 set the appropriate parameter value and
 send the correct message to the CAN Bus
"""
def key_pressed_handler(key):
    if key == keyboard.Key.enter:
        # start the car, otherwise stop it
        stop_car() if get_engine() else start_car()
        check_car_status(keySet)
    elif key == keyboard.Key.right:
        # set right turn signal to on
        set_right_sign(1)
        msg_sign_right()
        check_car_status(keySet)
    elif key == keyboard.Key.left:
        set_left_sign(1)
        msg_sign_left()
        check_car_status(keySet)
    elif key == keyboard.Key.shift_r:
        set_doors(1)
        msg_dr_unlocked()
        check_car_status(keySet)
    elif key == keyboard.Key.shift:
        set_doors(0)
        msg_dr_locked()
        check_car_status(keySet)
    elif key == keyboard.Key.up:
        inc_spd()
        msg_spd()
        check_car_status(keySet)
   # print('Special key {0} pressed'.format(key))

"""
 Handle alphanumeric key presses
 Depending on the key pressed,
 set the appropriate parameter value and
 send the correct message to the CAN Bus
 @throws exception if key is not alphanumeric
"""
def alphanum_key_pressed_handler(key):
    if (key.char == "1" 
            or key.char == "2" or key.char == "3"
            or key.char == "4" or key.char == "5"):
        set_gear(int(key.char))
        msg_gear()
        check_car_status(keySet)
    elif key.char == "p":
        set_park_brake(0) if get_park_brake() else set_park_brake(1)
        msg_park_brake()
        check_car_status(keySet)
    elif key.char == "s":
        set_seatbelt(0) if get_seatbelt() else set_seatbelt(1)
        msg_seatbelt()
        check_car_status(keySet)
    elif key.char == "l":
        set_lights(0) if get_lights() else set_lights(1)
        msg_lights()
        check_car_status(keySet)
    elif key.char == "f":
        # increment fuel and set it to hex
        set_fuel(int(get_fuel(), 16)+1)
        msg_fuel()
        check_car_status(keySet)
    elif key.char == "t":
        # increment temperature and set it to hex
        set_temperature(int(get_temperature(), 16)+1)
        msg_temperature()
        check_car_status(keySet)
    elif key.char == "b":
        # increment battery and set it to hex
        set_battery(int(get_battery(), 16)+1)
        msg_battery()
        check_car_status(keySet)

# Send engine started message
def msg_engine():
    engine = get_engine()
    msgEngine = can.Message(arbitration_id=0x1ff,data=[0, 0, 0, 0, 0, engine],extended_id=False)
    try:
        bus.send(msgEngine)
        print("Engine "+ str(engine) +" sent on {}".format(bus.channel_info))
    except can.CanError:
        print("Message NOT sent")

# Send turn signals are off message
def msg_sign_off():
    msgSignOff = can.Message(arbitration_id=0x188,data=[0, 0, 00, 0, 0, 0],extended_id=False)
    try:
        bus.send(msgSignOff)
        print("Sign off sent on {}".format(bus.channel_info))
    except can.CanError:
        print("Message NOT sent")

# Send turn signal left message
def msg_sign_left():
    msgSignLeft = can.Message(arbitration_id=0x188,data=[0, 0, 0, 0, 0, 1],extended_id=False)
    try:
        bus.send(msgSignLeft)
        print("Sign left sent on {}".format(bus.channel_info))
    except can.CanError:
        print("Message NOT sent")

# Send turn signal right message
def msg_sign_right():
    msgSignRight = can.Message(arbitration_id=0x188,data=[0, 0, 0, 0, 0, 2],extended_id=False)
    try:
        bus.send(msgSignRight)
        print("Sign right sent on {}".format(bus.channel_info))
    except can.CanError:
        print("Message NOT sent")

# Send doors locked message
def msg_dr_locked():
    msgDrLocked = can.Message(arbitration_id=0x19b,data=[0, 0, 15, 0, 0, 0],extended_id=False)
    try:
        bus.send(msgDrLocked)
        print("Door Locked sent on {}".format(bus.channel_info))
    except can.CanError:
        print("Message NOT sent")

# Send door unlocked message
def msg_dr_unlocked():
    msgDrUnLocked = can.Message(arbitration_id=0x19b,data=[0, 0, 0, 0, 0, 0],extended_id=False)
    try:
        bus.send(msgDrUnLocked)
        print("Door Unlocked sent on {}".format(bus.channel_info))
    except can.CanError:
        print("Message NOT sent")

# Send speed message
def msg_spd():
    spd = get_spd()
    hex_int = int(spd,16)
    new_int = hex_int + 0x0
    print(hex(new_int))
    msgSpdUp = can.Message(arbitration_id=0x244,data=[0, 0, 0, new_int, 0, 0],extended_id=False)
    try:
        bus.send(msgSpdUp)
        print("Speed "+ str(int(get_spd(),0)) +" sent on {}".format(bus.channel_info))
    except can.CanError:
        print("Message NOT sent")

# Send gear message
def msg_gear():
    gear = get_gear()
    print(gear)
    msgGear = can.Message(arbitration_id=0x1f5,data=[0, 0, 0, gear, 0, 0],extended_id=False)
    try:
        bus.send(msgGear)
        print("Gear "+ str(get_gear()) +" sent on {}".format(bus.channel_info))
    except can.CanError:
        print("Message NOT sent")


# Send park brake message
def msg_park_brake():
    park_brake = get_park_brake()
    msgParkBrake = can.Message(arbitration_id=0x1f7,data=[0, 0, 0, 0, 0, park_brake],extended_id=False)
    try:
        bus.send(msgParkBrake)
        print("Park Brake "+ str(park_brake) +" sent on {}".format(bus.channel_info))
    except can.CanError:
        print("Message NOT sent")

# Send seatbelt message
def msg_seatbelt():
    seatbelt = get_seatbelt()
    msgSeatBelt = can.Message(arbitration_id=0x1fb,data=[0, 0, 0, 0, 0, seatbelt],extended_id=False)
    try:
        bus.send(msgSeatBelt)
        print("Seat Belt "+ str(seatbelt) +" sent on {}".format(bus.channel_info))
    except can.CanError:
        print("Message NOT sent")

# Send lights message
def msg_lights():
    lights = get_lights()
    msgLights = can.Message(arbitration_id=0x1f8,data=[0, 0, 0, 0, 0, lights],extended_id=False)
    try:
        bus.send(msgLights)
        print("Lights "+ str(lights) +" sent on {}".format(bus.channel_info))
    except can.CanError:
        print("Message NOT sent")

# Send fuel level message
def msg_fuel():
    fuel = get_fuel()
    hex_int = int(fuel, 16)
    fuel = hex_int + 0x0
    print(hex(fuel))
    msgFuel = can.Message(arbitration_id=0x1fc,data=[0, 0, 0, 0, 0, fuel],extended_id=False)
    try:
        bus.send(msgFuel)
        print("Fuel "+ str(int(get_fuel(),0)) +" sent on {}".format(bus.channel_info))
    except can.CanError:
        print("Message NOT sent")

# Send temperature message
def msg_temperature():
    temp = get_temperature()
    hex_int = int(temp, 16)
    temp = hex_int + 0x0
    print(hex(temp))
    msgTemp = can.Message(arbitration_id=0x1fd,data=[0, 0, 0, 0, 0, temp],extended_id=False)
    try:
        bus.send(msgTemp)
        print("Temperature "+ str(int(get_temperature(),0)) +" sent on {}".format(bus.channel_info))
    except can.CanError:
        print("Message NOT sent")

# Send battery message
def msg_battery():
    battery = get_battery()
    hex_int = int(battery, 16)
    new_int = hex_int + 0x0
    print(hex(new_int))
    msgBattery = can.Message(arbitration_id=0x1fe,data=[0, 0, 0, 0, 0, new_int],extended_id=False)
    try:
        bus.send(msgBattery)
        print("Battery "+ str(int(get_battery(),0)) +" sent on {}".format(bus.channel_info))
    except can.CanError:
        print("Message NOT sent")



# Initialize vehicle status
def init_car_status():
    global Engine
    Engine = 0
    global currSpd
    currSpd = '0x00'
    global LeftSign
    LeftSign = 0
    global RightSign
    RightSign = 0
    global Doors
    Doors = 0
    global SeatBelt
    SeatBelt = 0
    global Gear
    Gear = 0
    global ParkBrake
    ParkBrake = 1
    global Lights
    Lights = 0
    global Fuel
    Fuel = '0x2D'
    global Temperature
    Temperature = 20
    global Battery
    Battery = '0x50'
    global Latitude
    Latitude = 41.2445
    global Longitude
    Longitude = 42.4556
    global Collision
    Collision = 0

"""
 Set parameters and send messages
 when starting the car
 Some values are hardcoded but 
 would be sensor data in reality
"""
def start_car():
    # turn on engine
    set_engine(1)
    msg_engine()
    # set the fuel level
    set_fuel(45)
    msg_fuel()
    # set temperature level
    set_temperature(60)
    msg_temperature()
    # set battery level
    set_battery(80)
    msg_battery()

"""
 Set parameters and send messages
 when stopping the car
 Some values are hardcoded but 
 would be sensor data in reality
"""
def stop_car():
    # turn on engine
    set_engine(0)
    msg_engine()
    # set the fuel level
    set_fuel(0)
    msg_fuel()
    # set battery level
    set_battery(0)
    msg_battery()
    # set speed
    set_spd(0)
    msg_spd()
    # set temperature level
    set_temperature(0)
    msg_temperature()
    # set gear
    set_gear(0)
    msg_gear()

"""
 Series of get and set 
 methods for the car parameters
"""
def get_engine():
    return Engine

def get_spd():
    return currSpd

def get_gear():
    return Gear

def get_park_brake():
    return ParkBrake

def get_lights():
    return Lights

def get_doors():
    return Doors

def get_seatbelt():
    return SeatBelt

def get_left_sign():
    return LeftSign

def get_right_sign():
    return RightSign

def get_fuel():
    return Fuel

def get_temperature():
    return Temperature

def get_battery():
    return Battery

def get_collision():
    return Collision

def set_engine(status):
    global Engine
    Engine = status

def set_spd(status):
    global currSpd
    currSpd = hex(status)

def set_left_sign(status):
    global LeftSign
    LeftSign = status

def set_right_sign(status):
    global RightSign
    RightSign = status

def set_doors(status):
    global Doors
    Doors = status

def set_seatbelt(status):
    global SeatBelt
    SeatBelt = status

def set_gear(nGear):
    global Gear
    Gear = nGear

def set_park_brake(nParkBrake):
    global ParkBrake
    ParkBrake = nParkBrake

def set_lights(nLights):
    global Lights
    Lights = nLights

def set_fuel(nFuel):
    global Fuel
    Fuel = hex(nFuel)

def set_temperature(nTemperature):
    global Temperature
    Temperature = hex(nTemperature)

def set_battery(nBattery):
    global Battery
    Battery = hex(nBattery)

def set_collision(nCollision):
    global Collision
    Collision = nCollision

# Increment speed and convert to hex
def inc_spd():
    oldSpd = get_spd()
    global currSpd
    temp = int(oldSpd, 16)
    temp += 1
    currSpd = hex(temp)

# Decrement speed and convert to hex
def dec_spd():
    oldSpd = get_spd()
    global currSpd
    if oldSpd != 0:
        temp = int(oldSpd, 16)
        temp -= 1
        currSpd = hex(temp)

"""
 Check parameters of the car after having made
 a change to one of them
"""
def check_car_status(keySet):
    nCurrSpd = int(currSpd,0)
    # Decrement the speed if key is not pressed
    if 0 != nCurrSpd and keyboard.Key.up not in keySet:
        dec_spd()
        msg_spd()
    # Set the turn signals to off if none of them are pressed
    if (1 == LeftSign and keyboard.Key.left not in keySet) or (1 == RightSign and keyboard.Key.right not in keySet):
        set_left_sign(0)
        set_right_sign(0)
        msg_sign_off()
    # Lock the doors if speed is over amount
    if (15 < nCurrSpd and 1 == Doors):
        set_doors(0)
        msg_dr_locked()

    # Select the right gear for the speed
    # the car is moving at
    if (0 == nCurrSpd and 0 != Gear):
        if Gear != 0:
            set_gear(0)
            msg_gear()
    elif (0 != nCurrSpd and 10 > nCurrSpd):
        if Gear != 1:
            set_gear(1)
            msg_gear()
    elif (0 != nCurrSpd and 30 > nCurrSpd):
        if Gear != 2:
            set_gear(2)
            msg_gear()
    elif (0 != nCurrSpd and 50 > nCurrSpd):
        if Gear != 3:
            set_gear(3)
            msg_gear()
    elif (0 != nCurrSpd and 70 > nCurrSpd):
        if Gear != 4:
            set_gear(4)
            msg_gear()
    elif (0 != nCurrSpd and 90 > nCurrSpd):
        if Gear != 5:
            set_gear(5)
            msg_gear()



"""
 Listener Class to override keyboard.Listener
 methods on_press and on_release
 and define a keySet which stores the 
 actively pressed keys
"""
class MyListener(keyboard.Listener):
    def __init__(self):
        super(MyListener, self).__init__(self.on_press, self.on_release)
        self.key_pressed = None
        self.key = None
        self.keySet = set()
    def on_press(self, key):
        self.key_pressed = True
        self.key = key
        if key not in self.keySet:
            self.keySet.add(key)
    def on_release(self,key):
        self.key = key
        if key in self.keySet:
            self.keySet.remove(key)
        if not self.keySet:
            self.key_pressed = False

# Initialize keyboard listener
listener = MyListener()
listener.start()

"""
 A variable used for the defining whether the user
 has begun pressing the key, this is to check
 whether they are holding the key
"""
started_press = False

# Initialize global car parameters
init_car_status()


"""
 Listen for Key presses and handle them
 a time sleep is defined in order for
 the speed of the vehicle to drop gradually
 TODO: a better way to do it is to decrease the speed
 by defining the time elapsed rather 
 than waiting for it to do so
"""
while True:
    try:
        time.sleep(0.1)
        keySet = listener.keySet
        if listener.key_pressed == True and started_press == False:
            started_press = True
            # create a copy of the keySet to prevent the set changing size during iteration
            for key in keySet.copy():
                try:
                    # check whether an alphanumeric character is pressed
                    alphanum_key_pressed_handler(key)
                except AttributeError:
                    # exception is thrown if not
                    key_pressed_handler(key)
        elif listener.key_pressed == True and started_press == True:
            for key in keySet.copy():
                try:
                    alphanum_key_pressed_handler(key)
                except AttributeError:
                    key_pressed_handler(key)
        elif listener.key_pressed == False and started_press == True:
            started_press = False
        elif listener.key_pressed == False and started_press == False:
            """
             Check the car status when nothing is being pressed
             this decreases the speed if it's above 0
             simulating throttle liftoff
            """
            if(0 != int(get_spd(), 0)):
                check_car_status(keySet)
    except KeyboardInterrupt:
        # On CTRL+C
        break
