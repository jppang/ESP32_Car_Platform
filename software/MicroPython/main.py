from machine import Pin
from ble import BLE

RightFrontFWD = 26
RightFrontBWD = 25
RightBackFWD = 32
RightBackBWD = 33

LeftFrontFWD = 4
LeftFrontBWD = 27
LeftBackFWD = 12
LeftBackBWD = 13

#Dabble App message is consisted of 8 bytes, and those commands associated with GamePad are in the combination of
#6th and 7th bytes of this message.
UP = b'\x00\x01'
DOWN = b'\x00\x02'
LEFT = b'\x00\x04'
RIGHT = b'\x00\x08'
TRIANGLE = b'\x04\x00'
CROSS = b'\x10\x00'
SQUARE = b' \x00'
CIRCLE = b'\x08\x00'
SELECT = b'\x02\x00'
START = b'\x01\x00'

mode = bytearray()

rfFWD = Pin(RightFrontFWD, Pin.OUT)
rfBWD = Pin(RightFrontBWD, Pin.OUT)
rbFWD = Pin(RightBackFWD, Pin.OUT)
rbBWD = Pin(RightBackBWD, Pin.OUT)
lfFWD = Pin(LeftFrontFWD, Pin.OUT)
lfBWD = Pin(LeftFrontBWD, Pin.OUT)
lbFWD = Pin(LeftBackFWD, Pin.OUT)
lbBWD = Pin(LeftBackBWD, Pin.OUT)

def moveForward():
    rfFWD.on()
    rfBWD.off()
    rbFWD.on()
    rbBWD.off()

    lfFWD.on()
    lfBWD.off()
    lbFWD.on()
    lbBWD.off()

def moveBackward():
    rfFWD.off()
    rfBWD.on()
    rbFWD.off()
    rbBWD.on()

    lfFWD.off()
    lfBWD.on()
    lbFWD.off()
    lbBWD.on()

def rotateRight():
    rfFWD.off()
    rfBWD.on()
    rbFWD.off()
    rbBWD.on()

    lfFWD.on()
    lfBWD.off()
    lbFWD.on()
    lbBWD.off()

def rotateLeft():
    rfFWD.on()
    rfBWD.off()
    rbFWD.on()
    rbBWD.off()

    lfFWD.off()
    lfBWD.on()
    lbFWD.off()
    lbBWD.on()

def moveSidewaysRight():
    rfFWD.off()
    rfBWD.on()
    rbFWD.on()
    rbBWD.off()

    lfFWD.on()
    lfBWD.off()
    lbFWD.off()
    lbBWD.on()

def moveSidewaysLeft():
    rfFWD.on()
    rfBWD.off()
    rbFWD.off()
    rbBWD.on()

    lfFWD.off()
    lfBWD.on()
    lbFWD.on()
    lbBWD.off()

def moveRightForward():
    rfFWD.off()
    rfBWD.off()
    rbFWD.on()
    rbBWD.off()

    lfFWD.on()
    lfBWD.off()
    lbFWD.off()
    lbBWD.off()

def moveLeftForward():
    rfFWD.on()
    rfBWD.off()
    rbFWD.off()
    rbBWD.off()

    lfFWD.off()
    lfBWD.off()
    lbFWD.on()
    lbBWD.off()

def stopMoving():
    rfFWD.off()
    rfBWD.off()
    rbFWD.off()
    rbBWD.off()

    lfFWD.off()
    lfBWD.off()
    lbFWD.off()
    lbBWD.off()

ble = BLE()

while(True):
    if ble.flag == True:
        mode = ble.message[5:7]
        print(mode)
        ble.flag = False

        if mode == UP:
            print("UP is pressed.")
            moveForward()
        elif mode == DOWN:
            print("DOWN is pressed.")
            moveBackward()
        elif mode == LEFT:
            print("LEFT is pressed.")
            rotateLeft()
        elif mode == RIGHT:
            print("RIGHT is pressed.")
            rotateRight()
        elif mode == TRIANGLE:
            print("TRIANGLE is pressed.")
            moveLeftForward()
        elif mode == CROSS:
            print("CROSS is pressed.")
            moveRightForward()
        elif mode == SQUARE:
            print("SQUARE is pressed.")
            moveSidewaysLeft()
        elif mode == CIRCLE:
            print("CIRCLE is pressed.")
            moveSidewaysRight()
        elif mode == SELECT:
            print("SELECT is pressed.")
        elif mode == START:
            print("START is pressed.")
        else:
            stopMoving()