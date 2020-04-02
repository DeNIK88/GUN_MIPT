import tkinter as tk
import math
import time

root = tk.Tk()
root.geometry('800x600')
canv = tk.Canvas(root)
canv.pack(fill="both", expand=1)


class Gun:
    def __init__(self):
        self.id = canv.create_line(40, 500, 80, 500, width=7)  # Просто линия
        self.tension_variable = 30  # Стартовая длина линии
        self.push_on = False  # Маркер зажатой левой кнопки
        self.mouse_x = root.winfo_pointerx() - root.winfo_rootx()  # Определяю координаты мыши относительно окна
        self.mouse_y = root.winfo_pointery() - root.winfo_rooty()

    def get_mouse_coord(self, event=0):  # Обновляю координаты мыши при событии (движение мыши) и запускаю наведение.
        if event:
            self.mouse_x = root.winfo_pointerx() - root.winfo_rootx()
            self.mouse_y = root.winfo_pointery() - root.winfo_rooty()
            self.targeting()
        else:
            self.targeting()

    def push_start(self, event=0):
        if event:
            self.push_on = True

    def push_stop(self, event=0):
        if event:
            self.push_on = False

    def targeting(self):  # Наведение
        # Шаг 1. Узнать расстояние между координатами начала линии и мыши.
        """Расстояние между точками плоскости равно корню квадратному из
        суммы квадратов разностей одноименных координат этих точек."""

        mouse_x = self.mouse_x
        mouse_y = self.mouse_y
        dlina = math.sqrt((mouse_x - 40)**2 + (mouse_y - 500)**2)

        # Шаг 2. Нормальзовать полученный вектор.
        """В первом шаге линия от точек 40, 500 (13 строка) до координат мыши. Нужно укоротить её до 
        желаемой величины, НО! сохранить направление. Итак, нормализация вектора - получение из некоторого вектора n 
        другого вектора с одинаковым направлением, но длинной, равной 1,0. Нормализованный вектор это исходный вектор, 
        деленный на свою длину"""

        delta_x = (mouse_x - 40) / dlina
        delta_y = (mouse_y - 500) / dlina

        """Получились координаты вектора длиной в 1,0, но с сохранением направления. Теперь умножим их на заданную 
         длину линии (14 строка) и перенесём к началу линии (13 строка)"""

        delta_x = delta_x * self.tension_variable + 40
        delta_y = delta_y * self.tension_variable + 500

        # Шаг 3. Отдаём координаты в функцию рисования.

        self.draw_line(delta_x, delta_y)

    def draw_line(self, delta_x, delta_y):
        if self.push_on:
            canv.itemconfig(self.id, fill='orange')
            if self.tension_variable < 100:
                self.tension_variable += 1
                time.sleep(0.03)
            canv.coords(self.id, 40, 500, delta_x, delta_y)
        else:
            canv.itemconfig(self.id, fill='black')
            canv.coords(self.id, 40, 500, delta_x, delta_y)


g1 = Gun()

root.bind('<ButtonPress-1>', g1.push_start)
root.bind('<ButtonRelease-1>', g1.push_stop)
root.bind('<Motion>', g1.targeting)
root.bind('<Motion>', g1.get_mouse_coord)



while True:
    g1.get_mouse_coord()
    canv.update()