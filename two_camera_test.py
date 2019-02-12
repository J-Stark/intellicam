#import serial
#import time
import cv2
import random
import arduinoHandler
import CameraSystem


def main():
    arduino = arduinoHandler.Arduino('ACM0', 9600)
    cameraList = []
    Camera1 = CameraSystem.Camera(0)
    Camera2 = CameraSystem.ServoCamera(1, arduino)
    cameraList.append(Camera1)
    cameraList.append(Camera2)

    while True:
        arduino.sensor()
        detection = arduino.serial.read()
        if (detection == b'x'):
            while True:
                for cam in cameraList:
                    cv2.imshow(cam.getName(), cam.getImg())
                if cv2.waitKey(1) == 27:
                    break
            cv2.destroyAllWindows()

main()
