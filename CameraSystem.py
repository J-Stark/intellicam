import cv2
import numpy
import cascades

class Camera():

    def __init__(self, ID):
        self.__cameraID = ID
        self.__cameraName = 'Intelligent Camera ' + str(self.__cameraID)
        self.__cam = cv2.VideoCapture(self.__cameraID)

    def getName(self):
        return self.__cameraName
    def getImg(self):
        return_val, img = self.__cam.read()
        print(img)
        img = cv2.flip(img, 1)
        if return_val:
            return img
    def detectBody(self):
        img = self.getImg()
        img = cv2.resize(img, (240, 160))  # Downscale to improve frame rate
        gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Haar-cascade classifier needs a grayscale image
        rects = cascades.person_cascade.detectMultiScale(gray_frame)
        for (x, y, w, h) in rects:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            print(x,y)
        return img
    def detectFace(self):
        img = self.getImg()
        img = cv2.resize(img, (240, 160))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = cascades.face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
           cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
           roi_gray = gray[y:y + h, x:x + w]
           roi_color = img[y:y + h, x:x + w]

           eyes = cascades.eye_cascade.detectMultiScale(roi_gray)
           for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        return img
    def takePicture(self):
        frameID = self.getImg().get(self.__cameraID)
        filename = "images/" + str(int(frameID)) + ".jpg"
        cv2.imwrite(filename, self.getImg())



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
