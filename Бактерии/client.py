import math
import socket
import pygame
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
from tkinter.colorchooser import *
from tkinter import *

name=""
color=""

def login():
    global name
    name = row.get()
    if name and color:
        root.destroy()
        root.quit()
    else:
        tk.messagebox.showerror("Ошибка", "Ты не выбрал цвет или не ввёл имя!")
root = tk.Tk()
root.title("Логин")
root.geometry("300x200")

style = ttk.Style()
style.theme_use('clam')

name_label = tk.Label(root, text="Введи свой никнейм:")
name_label.pack()
row = tk.Entry(root, width=30, justify="center")
row.pack()
color_label = tk.Label(root, text="Выбери цвет:")
color_label.pack()
colors = ['Maroon', 'DarkRed', 'FireBrick', 'Red', 'Salmon', 'Tomato', 'Coral', 'OrangeRed', 'Chocolate', 'SandyBrown',
          'DarkOrange', 'Orange', 'DarkGoldenrod', 'Goldenrod', 'Gold', 'Olive', 'Yellow', 'YellowGreen', 'GreenYellow',
          'Chartreuse', 'LawnGreen', 'Green', 'Lime', 'SpringGreen', 'MediumSpringGreen', 'Turquoise',
          'LightSeaGreen', 'MediumTurquoise', 'Teal', 'DarkCyan', 'Aqua', 'Cyan', 'DeepSkyBlue',
          'DodgerBlue', 'RoyalBlue', 'Navy', 'DarkBlue', 'MediumBlue']

# combo = ttk.Combobox(root, values=colors, textvariable=color)
# combo.bind("<<ComboboxSelected>>", scroll)
# combo.pack()

def vibor():
    global color
    a=askcolor()
    color=a[1]

viborb=Button(root,text='Выберите цвет', command=vibor)
viborb.pack()

name_btn = tk.Button(root, text="Зайти в игру", command=login)
name_btn.pack()
root.mainloop()

pygame.init()
WIDTH = 800
HEIGHT = 600
CC = (WIDTH // 2, HEIGHT // 2)
old = (0, 0)
radius = 50
buffer = 1024


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Настраиваем сокет
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Отключаем пакетирование
sock.connect(("localhost", 10000))
sock.send(f"color:<{name},{color}>".encode())


text = " У лукоморья дуб зелёный,Златая цепь на дубе том:,И днём и ночью кот учёный,"\
              "Всё ходит по цепи кругом;"\
              "Идёт направо - песнь заводит,"\
              "Налево - сказку говорит."

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Бактерии")
FPS = 100
clock = pygame.time.Clock()



def find(vector: str):
    global buffer
    first = None
    for num, sign in enumerate(vector):
        if sign == "<":
            first = num
        if sign == ">" and first is not None:
            second = num
            result = vector[first + 1:second]  # Поменяли
            return result
    if buffer < 1000000:
        buffer = int(buffer * 1.5)
    return ""

def draw_bacteries(data: list[str]):
    for num, bact in enumerate(data):
        data = bact.split(" ")  # Разбиваем по пробелам подстроку одной бактерии
        x = CC[0] + int(data[0])
        y = CC[1] + int(data[1])
        size = int(data[2])
        color = data[3]
        pygame.draw.circle(screen, color, (x, y), size)
        if len(data)>4:
            draw_text(x,y,size//2,data[4], 'black')

def draw_text(x,y,r,text,color):
    font = pygame.font.Font(None, r)
    text = font.render(text, True, color)
    rect = text.get_rect(center=(x, y))
    screen.blit(text, rect)

class Grid:
    def __init__(self, screen, color):
        self.screen = screen
        self.x = 0
        self.y = 0
        self.start_size = 200
        self.size = self.start_size
        self.color = color

    def update(self, parameters: list[int]):
        x, y, L = parameters
        self.size = self.start_size // L
        self.x = -self.size + (-x) % self.size
        self.y = -self.size + (-y) % self.size

    def draw(self):
        for i in range(WIDTH // self.size + 2):
            pygame.draw.line(self.screen, self.color,
                             (self.x + i * self.size, 0),  # Координаты начала линии
                             (self.x + i * self.size, HEIGHT),  # Координаты конца линии
                             1)
        for i in range(HEIGHT // self.size + 2):
            pygame.draw.line(self.screen, self.color,
                             (0, self.y + i * self.size),  # Координаты начала линии
                             (WIDTH, self.y + i * self.size),  # Координаты конца линии
                             1)



grid = Grid(screen, "seashell4")

run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get(): # цикл пробегает по всех событиям игры и кладет каждое из них в event
        if event.type == pygame.QUIT: # обрабатывает нажатие кнопки закрытия окна
            run = False
        if pygame.mouse.get_focused(): # обрабатываем событие движения мышки
            pos = pygame.mouse.get_pos() # берем координаты мыши
            vector = pos[0] - CC[0], pos[1] - CC[1]
            lenv = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
            if lenv != 0:
                vector = vector[0] / lenv, vector[1] / lenv
            if lenv <= radius:
                vector = 0, 0
            if vector != old:
                old = vector
                msg = f"<{vector[0]},{vector[1]}>"
                sock.send(msg.encode())

    # Получаем
    data = sock.recv(buffer).decode()
    data = find(data).split(",")  # Разбиваем на шары
    # Рисуем новое поле
    screen.fill('gray25')
    if data != ['']:
        parameters = list(map(int, data[0].split(" ")))
        radius = parameters[0]  # Сохраняем размер из сообщения в переменную
        grid.update(parameters[1:])
        grid.draw()
        draw_bacteries(data[1:])  # Срезаем размер, чтобы он не попадал в ф-ию рисования соседейй
    pygame.draw.circle(screen, color, CC, radius)
    draw_text(CC[0],CC[1],radius,name,"black")

    pygame.display.update()



pygame.quit()