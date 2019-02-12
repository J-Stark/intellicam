import cv2
import random
import numpy
import arduinoHandler
import CameraSystem

cameraList = []

def run():
    arduino = arduinoHandler.Arduino('ACM0', 9600)
    Camera1 = CameraSystem.Camera(0)
    #Camera2 = CameraSystem.ServoCamera(1, arduino)

    cameraList.append(Camera1)
    #cameraList.append(Camera2)
    activateCamera(0,True)

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

def activateCamera(ID, Active):
    camera = cameraList[ID]
    while Active:
        cv2.imshow(camera.getName(), camera.getImg())
        if cv2.waitKey(1) == 27:
            break
    cv2.destroyWindow(camera.getName())

run()
