import tkinter as tk
import math
import time
from random import randrange as rnd, choice

root = tk.Tk()
root.geometry('800x600')
canv = tk.Canvas(root)
canv.pack(fill="both", expand=1)


def mine():
    global balls, bullet
    while target.target_life:
        for b in balls:
            b.movie()
            if not b.hit_test(target):
                target.target_life = False
                print(target.target_life)
                canv.bind('<ButtonPress-1>', '')
                canv.bind('<ButtonRelease-1>', '')
                canv.itemconfig(screen, text="Вы уничтожили цель за " + str(bullet) + " выстрелов")
        g1.get_mouse_coord()

        canv.update()
        time.sleep(0.03)
    canv.delete(g1)
    canv.delete(ball)
    canv.update()


class Gun:
    def __init__(self):
        self.id = canv.create_line(40, 500, 70, 500, width=7, smooth=1)  # Просто линия
        self.tension_variable = 10  # Стартовая длина линии
        self.push_on = None  # Маркер зажатой левой кнопки
        self.mouse_x = 41
        self.mouse_y = 500
        self.bullet_count = 0

    def get_mouse_coord(self, event=0):  # Обновляю координаты мыши при событии и запускаю наведение.
        if event:
            self.mouse_x = event.x
            self.mouse_y = event.y
            # print(self.mouse_x, self.mouse_y)
            self.targeting()
        else:
            self.targeting()

    def push_start(self, event=0):
        if event:
            self.push_on = True

    def push_stop(self, event):
        global balls, bullet
        self.push_on = False
        new_ball = Ball()
        # Создал шар
        ball_dx = self.mouse_x - 40
        ball_dy = self.mouse_y - 500
        # Нашел расстояние, вектор от центра мяча до курсора
        angle = math.atan((event.y - new_ball.y) / (event.x - new_ball.x))
        # Узнал угол между двумя векторами
        # Направил шар на найденный угол
        new_ball.vx = self.tension_variable * math.cos(angle)
        new_ball.vy = - self.tension_variable * math.sin(angle)
        # print(new_ball.vx, new_ball.vy)
        balls += [new_ball]
        # Список с выпущенными шарами
        self.tension_variable = 10
        bullet += 1

    def targeting(self):  # Наведение
        # Шаг 1. Узнать расстояние между координатами начала линии и мыши.
        """Расстояние между точками плоскости равно корню квадратному из
        суммы квадратов разностей одноименных координат этих точек."""

        dlina = math.sqrt((self.mouse_x - 40) ** 2 + (self.mouse_y - 500) ** 2)

        # Шаг 2. Нормальзовать полученный вектор.
        """В первом шаге линия от точек 40, 500 (13 строка) до координат мыши. Нужно укоротить её до 
        желаемой величины, НО! сохранить направление. Итак, нормализация вектора - получение из некоторого вектора n 
        другого вектора с одинаковым направлением, но длинной, равной 1,0. Нормализованный вектор это исходный вектор, 
        деленный на свою длину"""

        delta_x = (self.mouse_x - 40) / dlina
        delta_y = (self.mouse_y - 500) / dlina

        """Получились координаты вектора длиной в 1,0, но с сохранением направления. Теперь умножим их на заданную 
         длину линии (14 строка) и перенесём к началу линии (13 строка)"""

        delta_x = delta_x * self.tension_variable + 40
        delta_y = delta_y * self.tension_variable + 500

        # Шаг 3. Отдаём координаты в функцию рисования.

        self.draw_line(delta_x, delta_y)

    def draw_line(self, delta_x, delta_y):
        if self.push_on:
            canv.itemconfig(self.id, fill='orange')
            if self.tension_variable < 60:
                self.tension_variable += 1
                time.sleep(0.03)
            canv.coords(self.id, 40, 500, delta_x, delta_y)
        else:
            canv.itemconfig(self.id, fill='black')
            canv.coords(self.id, 40, 500, delta_x, delta_y)


class Target:
    def __init__(self):
        self.r = rnd(15, 40)
        self.x = rnd(450, 750)
        self.y = rnd(50, 550)
        self.target_life = True

    def new_target(self):
        self.target_size = rnd(15, 40)
        self.target_x = rnd(450, 750)
        self.target_y = rnd(50, 550)

        canv.create_oval(self.x - self.r, self.y - self.r,
                         self.x + self.r, self.y + self.r, fill='red')

    def hit_test(self, obj):
        delta_ball_and_target = math.sqrt((obj.x - self.x) ** 2 + (obj.y - self.y) ** 2)
        if delta_ball_and_target >= obj.r + self.r:
            self.target_life = False
            print(self.target_life)
        else:
            self.target_life = True


class Ball:
    def __init__(self):
        self.x = 40
        self.y = 500
        self.r = 10
        self.vx = 5
        self.vy = 5
        self.color = choice(['blue', 'orange', 'yellow', 'green', 'brown'])
        self.id = canv.create_oval(self.x - self.r, self.y - self.r, self.x + self.r,
                                   self.y + self.r, fill=self.color)

    def rewrite_coords(self):
        canv.coords(self.id,
                    self.x - self.r, self.y - self.r,
                    self.x + self.r, self.y + self.r)

    def movie(self):
        if self.vx >= 1 or self.vy >= 1:
            if self.x >= 800 - self.r * 2 or self.x < 0 + self.r * 2:
                self.vy //= 2
                self.vx //= 2
                self.vx = + self.vx
                if self.vx <= 0.1:
                    self.vx = 0

            if self.y >= 600 - self.r * 2 or self.y < 0 + self.r * 2:
                self.vy //= 2
                self.vx //= 2
                self.vy = - self.vy
                if self.vy <= 0.1:
                    self.vy = 0

            self.x += self.vx
            self.y -= self.vy

            self.vy -= 1

        self.rewrite_coords()

    def hit_test(self, obj):
        distance = math.sqrt((obj.x - self.x) ** 2 + (obj.y - self.y) ** 2)
        if distance <= obj.r + self.r:
            return False
        else:
            return True


g1 = Gun()
target = Target()
ball = Ball

root.bind('<ButtonPress-1>', g1.push_start)
root.bind('<ButtonRelease-1>', g1.push_stop)
root.bind('<Motion>', g1.targeting)
root.bind('<Motion>', g1.get_mouse_coord)

balls = []
screen = canv.create_text(400, 300, text="", font=28)
bullet = 0
target.new_target()

mine()

tk.mainloop()
