from random import randrange as rnd, choice
import tkinter as tk
import time


root = tk.Tk()
root.geometry('800x600')
canv = tk.Canvas(root)
canv.pack(fill=tk.BOTH, expand=1)


class gun():
    def __init__(self):
        self.id = canv.create_line(40, 500, 80, 500, width = 7)
    def targetting(self, event):
        canv.coords(self.id, 40, 500, event.x, event.y)



g1 = gun()
root.bind('<Motion>', g1.targetting)


tk.mainloop()