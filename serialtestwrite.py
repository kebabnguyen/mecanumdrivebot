import serial
import time
ser = serial.Serial('/dev/ttyACM0', 9600)
print("sending values")
test1 = 1500
time.sleep(2)
ser.write(b'%d' %test1)
print(2000)
ser.write(b'\r')
ser.write(b'2000')
ser.write(b'\r')
print("done")
