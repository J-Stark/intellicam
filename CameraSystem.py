import cv2

class Camera():


    #https://docs.opencv.org/3.4/d7/dfc/group__highgui.html
    #https://docs.opencv.org/3.2.0/dc/d46/group__highgui__qt.html
    #
    def __init__(self, ID):
        self.__cameraID = ID
        self.__cameraName = 'Intelligent Camera ' + str(self.__cameraID)
        self.__cam = cv2.VideoCapture(self.__cameraID)

    def getName(self):
        return self.__cameraName
    def getImg(self):
        ret_val, img = self.__cam.read()
        img = cv2.flip(img, 1)
        return img

class ServoCamera(Camera):
    def __init__(self, ID, arduino):
        Camera.__init__(self, ID)
        self.__arduino = arduino
    def move(self,command):
        self.__arduino.serial.write(command)
    def panTo(self, position):
        command = 'panTo;' + str(position) + ';'
        self.move(command.encode())
    def tiltTo(self, position):
        command = 'tiltTo;' + str(position) + ';'
        self.move(command.encode())
    def tilt(self, position):
        command = 'tilt;' + str(position) + ';'
        self.move(command.encode())
    def pan(self, position):
        command = 'pan;' + str(position) + ';'
        self.move(command.encode())
    def readPan(self):
        command = 'readP;'
        firstLine = self.__arduino.serial.read()
        print(firstLine)
    def readTilt(self):
        command = 'readT;'
        firstLine = self.__arduino.serial.read()
        print(firstLine)
