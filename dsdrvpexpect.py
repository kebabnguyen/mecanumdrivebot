import pexpect
import math
import time
import serial

def truncate(number, digits) -> float: #truncates number to digits decimal places
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

class DS4Parser:
    def __init__(self):
        self.serialopen = 0
        try:
            self.ser = serial.Serial('/dev/ttyACM0', 9600)
            self.serialopen = 1
        except: 
            print('close the arduino port you muppet')
        self.inputs = (
                        'left_analog_x: ', 
                        'left_analog_y: ',
                        'right_analog_y: ',
                        'right_analog_y: ',
                        'l2_analog: ',
                        'r2_analog: ',
                        'dpad_up: ',
                        'dpad_down: ',
                        'dpad_left: ',
                        'dpad_right: ',
                        'button_cross: ',
                        'button_circle: ',
                        'button_square: ',
                        'button_triangle: ',
                        'button_l1: ',
                        'button_l2: ',
                        'button_l3: ',
                        'button_r1: ',
                        'button_r2: ',
                        'button_r3: ',
                        'button_share: ',
                        'button_options: ',
                        'button_trackpad: ',
                        'button_ps: '
                    )
        self.analogs = ('left_analog_x: ', 
                        'left_analog_y: ', 
                        'l2_analog: ',
                        'r2_analog: ',)
        self.values = [0, 0, 0, 0]
        self.connected = 0
        self.active = 0
        shellcmd = 'ds4drv --dump-reports'
        self.ds4drv = pexpect.spawn('/bin/bash', ['-c', shellcmd]) 
       
    def connect(self): #if it doesnt connect in 30s then it gives timeout and tries again,
        try:           #but it seems that the child process will connect fine while this function doesn't update correctly and thinks its not connected
            if self.ds4drv.expect('Scanning for devices') == 0:
                print('please connect controller')           
            if self.ds4drv.expect('Connected to Bluetooth Controller') == 0:
                print('controller connected') 
                self.connected = 1
            if self.ds4drv.expect('Battery: ', timeout=60) == 0:
                print('all set') 
                self.active = 1
        except pexpect.TIMEOUT:
            print('it aint working, retrying')
            self.connected = 0
         
    def storevals(self, buttons):
        iterator = 0
        for buttonname in buttons: #for each button grabs the value and stores it
            if self.ds4drv.expect(buttonname) == 0:
                readin = int(self.ds4drv.readline())
                self.values[iterator] = readin
                iterator += 1
        return self.values #this list probably could be attached to a dictionary

    def normalize(self, vals): #math according to mecanummath spreadsheet
        normvals = [0, 0, 0, 0] #vals[0] and vals[1] go from -1 to 1
        normvals[0] = (vals[0] / 127) - 1 #these are the analog x and y
        normvals[1] = (vals[1] / -127) + 1 
        normvals[2] = vals[2] / 255 #l2
        normvals[3] = vals[3] / 255 #r2
        return normvals

    def radius(self, x, y):
        return math.sqrt( math.pow(x,2) + math.pow(y,2))

    def radians(self, x, y): #gets angle from the vertical axis going CCW
        return math.atan2(x, y)

    def calculate_polar(self, vals): #returns polar form of lstick values
        radius = self.radius(vals[0], vals[1])
        radians = self.radians(vals[0], vals[1])
        if radians < 0:
            radians += (2*math.pi)
        radius = radius / 1.2
        radius = truncate(radius, 2)
        if radius < 0.1: #10% deadzone to stick, adjust as needed
            radius = 0
        polar = (radius, radians)
        return polar

    def calculate_motorvals(self, vals, coords): #returns the esc values to be sent to ard
        mag = coords[0]
        motoFL = 1500 + 250*mag*math.cos(coords[1]) + 250*mag*math.sin(coords[1]) + 250* vals[3] - 250* vals[2]
        motoFR = 1500 + 250*mag*math.cos(coords[1]) - 250*mag*math.sin(coords[1]) - 250* vals[3] + 250* vals[2] 
        motoBR = 1500 + 250*mag*math.cos(coords[1]) + 250*mag*math.sin(coords[1]) - 250* vals[3] + 250* vals[2]
        motoBL = 1500 + 250*mag*math.cos(coords[1]) - 250*mag*math.sin(coords[1]) + 250* vals[3] - 250 * vals[2]
        motorvals = (motoFL, motoFR, motoBR, motoBL)
        return motorvals

    def is_active(self):
        try: #try fiddling around with timeout and seeing if that does anything
            if self.ds4drv.expect('Report dump', timeout = 1.25) == 0:
                return 1
        except:
            return 0

    def controller_on(self):
        try:
            if self.ds4drv.expect('delete this you muppet', timeout = .1) == 0:
                print('goodbye')
                return 0
        except:
            return 1

    def __del__(self):
        self.ds4drv.terminate()

def main():
    parser = DS4Parser()
    while parser.connected != 1: #make sure controller is connected
        parser.connect()
    while parser.controller_on() == 1:
        if parser.is_active() == 1:   #if light green
            normvals = parser.normalize(parser.storevals(parser.analogs))
            polarcoords = parser.calculate_polar(normvals)
            print(parser.calculate_motorvals(normvals, polarcoords))
        elif parser.is_active() == 0: #light yellow, but still on
            print('in idle')
            pass

    del parser

if __name__ == "__main__":
    main()