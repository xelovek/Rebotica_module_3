import math
import socket
import pygame
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

name=""
color=""

def scroll(event):
    global color
    color = combo.get()
    style.configure("TCombobox", fieldbackground=color, background="white")
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

combo = ttk.Combobox(root, values=colors, textvariable=color)
combo.bind("<<ComboboxSelected>>", scroll)
combo.pack()
name_btn = tk.Button(root, text="Зайти в игру", command=login)
name_btn.pack()
root.mainloop()

pygame.init()
WIDTH = 800
HEIGHT = 600
CC = (WIDTH // 2, HEIGHT // 2)
old = (0, 0)
radius = 50


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

font = pygame.font.SysFont("Arial", 32)
text_surface = font.render(name, True, (255, 255, 255))
text_render = text_surface.get_rect()
text_render.center = CC

def find(vector: str):
    first = None
    for num, sign in enumerate(vector):
        if sign == "<":
            first = num
        if sign == ">" and first is not None:
            second = num
            result = vector[first + 1:second]  # Поменяли
            return result
    return ""

def draw_bacteries(data: list[str]):
    for num, bact in enumerate(data):
        data = bact.split(" ")  # Разбиваем по пробелам подстроку одной бактерии
        x = CC[0] + int(data[0])
        y = CC[1] + int(data[1])
        size = int(data[2])
        color = data[3]
        pygame.draw.circle(screen, color, (x, y), size)

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
            vector = vector[0] / lenv, vector[1] / lenv
            if lenv <= radius:
                vector = 0, 0
            if vector != old:
                old = vector
                msg = f"<{vector[0]},{vector[1]}>"
                sock.send(msg.encode())


    # Получаем
    data = sock.recv(1024).decode()

    print("Получил:", data)
    data = find(data).split(",")  # Разбиваем на шары
    # Рисуем новое поле
    screen.fill('gray')
    pygame.draw.circle(screen, color, CC, radius)
    screen.blit(text_surface, text_render)
    if data != ['']:
        print(data)
        draw_bacteries(data)
    pygame.display.update()



pygame.quit()