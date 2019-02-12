import serial
import time
import cv2

#https://docs.opencv.org/3.4/d7/dfc/group__highgui.html
#https://docs.opencv.org/3.2.0/dc/d46/group__highgui__qt.html
#
#ser = serial.Serial('/dev/ttyACM1',9600,timeout=0.5)
time.sleep(1)

def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        if mirror:
            img = cv2.flip(img, 1)
        cv2.imshow('Intelligent Camera', img)
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()


def main():
    show_webcam(mirror=True)


if __name__ == '__main__':
    main()
