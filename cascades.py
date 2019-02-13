import cv2
person_cascade = cv2.CascadeClassifier('xmls/haarcascade_fullbody.xml')
face_cascade = cv2.CascadeClassifier('xmls/haarcascade_frontalface.xml')
eye_cascade = cv2.CascadeClassifier('xmls/haarcascade_eye.xml')
smile_cascase = cv2.CascadeClassifier('xmls/haarcascade_smile.xml')
