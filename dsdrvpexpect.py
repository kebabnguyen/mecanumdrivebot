import pexpect
import time

class DS4Parser:
    def __init__(self):
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
        self.connected = -1
        self.active = 1
        shellcmd = 'ds4drv --dump-reports'
        self.ds4drv = pexpect.spawn('/bin/bash', ['-c', shellcmd]) 
       
    def connect(self):
        try:
            if self.ds4drv.expect('Scanning for devices') == 0:
                print('please connect controller')           
                if self.ds4drv.expect('Connected to Bluetooth Controller') == 0:
                    print('controller connected') 
                    self.connected = 1
        except pexpect.TIMEOUT:
            print('it aint working, retrying')
            self.connected = -1

    def checkstatus(self):
        try:
            if self.ds4drv.expect('profile: idle', 1) == 0:
                return -1
        except pexpect.TIMEOUT:
            return 1
         
    def checkval(self):
        for buttonname in self.inputs:
            if self.ds4drv.expect(buttonname) == 0:
                print(self.ds4drv.readline())
    def sanitycheck(self):
        if self.ds4drv.expect('Report dump: ', timeout = .5) == 0:
            #if self.ds4drv.expect('trackpad_touch0_id: ', timeout = .15) == 0:
            print(self.ds4drv.read(80))
    def __del__(self):
        self.ds4drv.terminate()

def main():
    parser = DS4Parser()
    while parser.connected != 1:
        parser.connect()
    while parser.checkstatus() == 1:
        parser.sanitycheck()
        while parser.checkstatus() != 1:
            break
    del parser

if __name__ == "__main__":
    main()