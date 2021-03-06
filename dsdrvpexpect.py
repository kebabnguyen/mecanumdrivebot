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
        self.analogs = ('left_analog_x: ', #format for listening from ds4drv dump
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
        return self.values 

    def normalize(self, vals): #grabs vals and normalize to scale
        normvals = [0, 0, 0, 0] #vals[0] and vals[1] go from -1 to 1
        normvals[0] = (vals[0] / 127) - 1 #these are the analog x and y
        normvals[1] = (vals[1] / -127) + 1 
        normvals[2] = vals[2] / 255 #l2
        normvals[3] = vals[3] / 255 #r2
        return normvals

    def radius(self, x, y):
        return math.sqrt( math.pow(x,2) + math.pow(y,2))

    def radians(self, x, y): #gets angle from the vertical axis going CW
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
        scale = 500 #variable to change how fast it can go, limit 1000 theoretically
        mag = coords[0] #abrupt change before deadzone and after, try scaling it
        motoFL = 1500 + scale* mag*math.cos(coords[1]) + scale* mag*math.sin(coords[1]) + scale* vals[3] - scale* vals[2]
        motoFR = 1500 - scale* mag*math.cos(coords[1]) + scale* mag*math.sin(coords[1]) + scale* vals[3] - scale* vals[2] 
        motoBR = 1500 - scale* mag*math.cos(coords[1]) - scale* mag*math.sin(coords[1]) + scale* vals[3] - scale* vals[2]
        motoBL = 1500 + scale* mag*math.cos(coords[1]) - scale* mag*math.sin(coords[1]) + scale* vals[3] - scale* vals[2]
        motorvals = (math.trunc(motoFL), math.trunc(motoFR), math.trunc(motoBR), math.trunc(motoBL))
        #print(motorvals) debug
        return motorvals

    def send_values(self, vals): #serial sends vals over for arduino to interpret
        for value in vals:
            self.ser.write(b'%d' %value)
            self.ser.flush()
            self.ser.write(b'r')
            self.ser.flush()

    def is_active(self):
        try: #try fiddling around with timeout and seeing if that does anything
            if self.ds4drv.expect('Report dump', timeout = 1.25) == 0:
                return 1
        except:
            return 0

    def controller_on(self): #checks if share button was pressed after going to idle
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
            motorvalues = parser.calculate_motorvals(normvals, polarcoords)
            parser.send_values(motorvalues)
        else: #light yellow, but still on
            parser.send_values((1500, 1500, 1500, 1500))
    del parser

if __name__ == "__main__":
    main()