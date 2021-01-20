import pexpect
import time

#spawns ds4drv, so we can listen to its output


class DS4Parser:
    
    def __init___(self):
        shellcmd = 'ds4drv --dump-reports'
        self.ds4drv = pexpect.spawn('/bin/bash', ['-c', shellcmd]) 
        self.connected = -1

    def connect(self):
        try:
            if self.ds4drv.expect('Scanning for devices') == 0:
                print('please connect controller')           
                if self.ds4drv.expect('Found device') == 0:
                    print('found device') 
                    self.connected = 1
        except pexpect.TIMEOUT:
            print('it aint working')
            self.connected = -1

    def checkval(self):
        if self.ds4drv.expect('Report dump') == 0:
            readin = self.ds4drv.read(52)
            return readin

    def __del__(self):
        self.ds4drv.terminate()

def main():
    parser = DS4Parser()
    while connected != 1:
        connect()
    
    if ds4drv.expect('Report dump') == 0:
        print(checkval())
    ds4drv.terminate()

if __name__ == "__main__":
    main()