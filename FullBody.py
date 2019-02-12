import numpy as np
import cv2

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

# https://gist.github.com/madhawav/haarcascades
#person_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')
person_cascade = cv2.CascadeClassifier('xmls/haarcascade_fullbody.xml')

cap = cv2.VideoCapture(0)

while True:
    r, frame = cap.read()
    if r:
        frame = cv2.resize(frame, (240, 160))  # Downscale to improve frame rate
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Haar-cascade classifier needs a grayscale image
        rects = person_cascade.detectMultiScale(gray_frame)

        for (x, y, w, h) in rects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            print(x,y)

        cv2.imshow("preview", frame)

    if cv2.waitKey(1) == 27:
        frameID = cap.get(0)
        filename = "images/" + str(int(frameID)) + ".jpg"
        cv2.imwrite(filename, frame)
        break
