import math
import socket
import pygame

pygame.init()
WIDTH = 800
HEIGHT = 600
CC = (WIDTH // 2, HEIGHT // 2)
old = (0, 0)
radius = 50
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Настраиваем сокет
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Отключаем пакетирование
sock.connect(("localhost", 10000))

text = " У лукоморья дуб зелёный,Златая цепь на дубе том:,И днём и ночью кот учёный,"\
              "Всё ходит по цепи кругом;"\
              "Идёт направо - песнь заводит,"\
              "Налево - сказку говорит."

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Бактерии")

run = True
while run:
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

    # Рисуем новое поле
    screen.fill('gray')
    pygame.draw.circle(screen, (255, 0, 0), CC, radius)
    pygame.display.update()



pygame.quit()