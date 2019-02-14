import cv2
import numpy
import cascades
import os
import time
import math


class Camera():

    picture = 0;

    def __init__(self, ID, arduino, imageFolder):
        self.__cameraID = ID
        self.__cameraName = 'Intelligent Camera ' + str(self.__cameraID)
        self.__cam = cv2.VideoCapture(self.__cameraID)
        self.__arduino = arduino
        self.__imageFolder = imageFolder
        self.__arduino.serial.write(b"Q")
        self.__arduino.serial.read()
    def getName(self):
        return self.__cameraName
    def getImg(self):
        return_val, img = self.__cam.read()
        img = cv2.flip(img, 1)
        if return_val:
            return img
    def detectBody(self):
        img = self.getImg()
        img = cv2.resize(img, (240, 160))  # Downscale to improve frame rate
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Haar-cascade classifier needs a grayscale image
        pedestrians = cascades.person_cascade.detectMultiScale(gray)
        for (x, y, w, h) in pedestrians:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return img
    def detectFace(self):
        img = self.getImg()
        img = cv2.resize(img, (240, 160))
        gray = cv2.cvtColor(img, cv2.COLORl_BGR2GRAY)
        faces = cascades.face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
           cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
           roi_gray = gray[y:y + h, x:x + w]
           roi_color = img[y:y + h, x:x + w]
           print(self.findMiddleRect(w,h))
           eyes = cascades.eye_cascade.detectMultiScale(roi_gray)
           for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        return img
    def detectFullBody(self):
        img = self.getImg()
        img = cv2.resize(img, (240, 160))  # Downscale to improve frame rate
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Haar-cascade classifier needs a grayscale image
        pedestrians = cascades.person_cascade.detectMultiScale(gray)
        faces = cascades.face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in pedestrians:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            for (x, y, w, h) in faces:
               cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
               roi_gray = gray[y:y + h, x:x + w]
               roi_color = img[y:y + h, x:x + w]
               eyes = cascades.eye_cascade.detectMultiScale(roi_gray)
               for (ex, ey, ew, eh) in eyes:
                    if cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2):
                        self.takePicture()
        return img

    def takePicture(self):
        path, dirs, files = next(os.walk("./images/"))
        file_count = len(files)
        if (file_count < 20):
            filename = "images/" + self.__imageFolder + str(int(file_count)) + ".jpg"
            cv2.imwrite(filename, self.getImg())
            self.__arduino.picture()


class ServoCamera(Camera):
    def __init__(self, ID, arduino, imageFolder):
        Camera.__init__(self, ID, arduino, imageFolder)
        self.ard = arduino

    def move(self,command):
        self.ard.serial.write(command)
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
    def detectFullFace(self):
        img = self.getImg()
        cameraX, cameraY = 240, 160  # RESOLUTION OF CAMERA
        img = cv2.resize(img, (cameraX, cameraY))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = cascades.face_cascade.detectMultiScale(gray, 1.3, 5)
        i = 0
        for (x, y, w, h) in faces:
           cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
           roi_gray = gray[y:y + h, x:x + w]
           roi_color = img[y:y + h, x:x + w]

           self.adjustCamera(w, h, cameraX, cameraY)

           eyes = cascades.eye_cascade.detectMultiScale(roi_gray)
           smiles = cascades.smile_cascase.detectMultiScale(roi_gray)
           for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
                for (sx, sy, sw, sh) in smiles:
                    cv2.rectangle(roi_color, (sx,sy), (sx+sw,sy+sh),(0, 255, 0), 2)
                    time.sleep(0.3)
                    self.takePicture()
        return img

    def adjustCamera(self, rectX, rectY, camX, camY):
        middleCamX = camX/2
        middleCamY = camY/2

        if rectX > middleCamX:
            # move NE
            self.pan(1)
            self.tilt(-1)
        elif rectX > middleCamX and rectY > middleCamY:
            self.pan(1)
            self.tilt(1)
            # move SE
        elif rectX < middleCamX:
            # move NW
            self.pan(-1)
            self.tilt(-1)
        elif rectX < middleCamX and rectY < middleCamY:
            # move SW
            self.pan(-1)
            self.tilt(1)
        else:
            self.panTo(90)
            self.tiltTo(90)
