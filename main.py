import tkinter as tk
import math

root = tk.Tk()
root.geometry('800x600')
canv = tk.Canvas(root)
canv.pack(fill="both", expand=1)


class Gun():
    def __init__(self):
        self.coordX = 40
        self.coordY = 500
        self.id = canv.create_line(self.coordX, self.coordY, 80, 500, width = 7)

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""

        # Шаг 1. Находим длину вектора (линия от x, y до курсора мыши).
        mouseX = event.x
        mouseY = event.y
        dlina = math.sqrt((mouseX - self.coordX)**2 + (mouseY - self.coordY)**2)
        # По формуле корень квадратный из суммы квадратов разностей координат

        # Шаг 2. Привожу длину вектора к желаемой.
        """ Нормализация вектора — это преобразование заданного вектора в вектор в том же направлении,
        но с единичной длиной. Для нормализации вектора нужно каждую компоненту поделить на длину вектора. """
        companente1 = (mouseX - self.coordX) / dlina
        compenente2 = (mouseY - self.coordY) / dlina
        # Получится нормализованный вектор длиной в единицу √companente1**2 + compenente2**2

        # Шаг 3. Рисую вектор новой длины (50)
        newCoordX = self.coordX + (companente1 * 50)
        newCoordY = self.coordY + (compenente2 * 50)
        canv.coords(self.id, self.coordX, self.coordY, newCoordX, newCoordY)

    def tension(self):  # tension - натяжение
        all()




g1 = Gun()
root.bind('<Motion>', g1.targetting)
tk.mainloop()
