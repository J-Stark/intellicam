from Tkinter import *

root = Tk()
root.title("Note Taker")

root.mainloop()

button1 = Button(root, text="button1")
button2 = Button(root, text="button2")
button3 = Button(root, text="button3")

text = Entry(root)
listbox = Listbox(root)

text.pack()
button1.pack()
button2.pack()
button3.pack()
listbox.pack()
