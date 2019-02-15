import cv2
from arduinoHandler import *
from CameraSystem import *

cameraList = []
arduino = Arduino('ACM0', 9600)


def run():

    Camera1 = Camera(0, arduino, "stationaryCam")
    Camera2 = ServoCamera(1, arduino, "servoCam")
    cameraList.append(Camera1)
    cameraList.append(Camera2)

    while True:
        arduino.sensor()
        detection = arduino.serial.read()
        if (detection == b'x'):
            while True:
                for cam in cameraList:
                    cv2.imshow(cam.getName(), cam.detectFullFace())
                if cv2.waitKey(1) == 27:
                    break
            cv2.destroyAllWindows()
