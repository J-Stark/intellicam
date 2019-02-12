import arduinoHandler
from tkinter import *

root = Tk()
root.title("Intelligent Camera Control")
arduino = arduinoHandler.Arduino('ACM0', 9600)

def LED():
    arduino.LED()

button1 = Button(root, text="LED", command=LED)
button2 = Button(root, text="Run")
button3 = Button(root, text="button3")


button1.pack()
button2.pack()
button3.pack()



root.mainloop()
