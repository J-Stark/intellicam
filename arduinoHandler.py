import serial
import time

class Arduino():
    def __init__(self, port, baudrate):
        fullPort = '/dev/tty' + port
        self.serial = serial.Serial(fullPort,baudrate,timeout=0.5)
        time.sleep(1)
    def LED(self):
        self.serial.write(b'LED;')
    def picture(self):
        self.serial.write(b'picture;')
        print("PICTURE");
    def sensor(self):
        self.serial.write(b'sensor;')
    def write(self, command):
        self.serial.write(command)
