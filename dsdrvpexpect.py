import pexpect
import time
import serial

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
         
    def checkvals(self, buttons):
        for buttonname in buttons:
            if self.ds4drv.expect(buttonname) == 0:
                readin = self.ds4drv.readline()
                if self.serialopen == 1:
                    self.ser.write(readin)
                print(readin)

    def is_active(self):
        try:
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
            parser.checkvals(parser.analogs)
        elif parser.is_active() == 0: #light yellow, but still on
            print('in idle')
            pass

    del parser

if __name__ == "__main__":
    main()