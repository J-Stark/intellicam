#import arduinoHandler
#import main_program
from tkinter import *

root = Tk()
root.title("Intelligent Camera Control")

def LED():
    #main_program.arduino.LED()
    print("T")

def start():
#    main_program.run()
    print("Q")

button1 = Button(root, text="LED", command=LED)
button2 = Button(root, text="Run", command=start)
button1.pack()
button2.pack()

root.mainloop()
