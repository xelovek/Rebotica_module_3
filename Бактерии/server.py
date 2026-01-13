import socket
import time
from db import *
import pygame

def find(vector: str):
    first = None
    for num, sign in enumerate(vector):
        if sign == "<":
            first = num
        if sign == ">" and first is not None:
            second = num
            result = list(map(float, vector[first + 1:second].split(",")))
            return result
    return ""

def find_color(info: str):
    first = None
    for num, sign in enumerate(info):
        if sign == "<":
            first = num
        if sign == ">" and first is not None:
            second = num
            result = info[first + 1:second].split(",")
            return result
    return ""

# Локальный класс таблицы игроков
class LocalPlayer:
    def __init__(self, id, name, sock, addr):
        self.id = id
        self.db: Player = s.get(Player, self.id)
        self.sock = sock
        self.name = name
        self.address = addr
        self.x = 500
        self.y = 500
        self.size = 50
        self.errors = 0
        self.abs_speed = 1
        self.speed_x = 0
        self.speed_y = 0
        self.color = 'red'
        self.w_vision = 800
        self.h_vision = 600

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def change_speed(self, vector):
        vector = find(vector)
        if vector[0] == 0 and vector[1] == 0:
            self.speed_x = self.speed_y = 0
        else:
            vector = vector[0] * self.abs_speed, vector[1] * self.abs_speed
            self.speed_x = vector[0]
            self.speed_y = vector[1]

    def load(self):
        self.size = self.db.size
        self.abs_speed = self.db.abs_speed
        self.speed_x = self.db.speed_x
        self.speed_y = self.db.speed_y
        self.errors = self.db.errors
        self.x = self.db.x
        self.y = self.db.y
        self.color = self.db.color
        self.w_vision = self.db.w_vision
        self.h_vision = self.db.h_vision
        return self

    def sync(self):
        self.db.size = self.size
        self.db.abs_speed = self.abs_speed
        self.db.speed_x = self.speed_x
        self.db.speed_y = self.speed_y
        self.db.errors = self.errors
        self.db.x = self.x
        self.db.y = self.y
        self.db.color = self.color
        self.db.w_vision = self.w_vision
        self.db.h_vision = self.h_vision
        s.merge(self.db)
        s.commit()

pygame.init()

WIDHT_ROOM, HEIGHT_ROOM = 4000, 4000
WIDHT_SERVER, HEIGHT_SERVER = 300, 300
FPS = 100

# Создание окна сервера
screen = pygame.display.set_mode((WIDHT_SERVER, HEIGHT_SERVER))
pygame.display.set_caption("Сервер")
clock = pygame.time.Clock()

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Создает главный сокет (прихожую)
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) # Отключаем пакетирование, чтобы передавать все каждый кадр игры
main_socket.bind(("localhost", 10000)) # Устанавливаем ip-адрес и порт, localhost - это локальный адрес этого компа

main_socket.setblocking(False) # Отключаем завершение подключения
main_socket.listen(5) # Включаем прослушку юзеров например 5 одновременно
print('Сокет создался')

players = {}
server_works = True
while server_works:
    clock.tick(FPS)
    try:
        # проверяем желающих войти в игру
        new_socket, addr = main_socket.accept()  # принимаем входящие
        print('Подключился', addr)
        new_socket.setblocking(False) # Отключаем завершение подключения для новых игроков
        login = new_socket.recv(1024).decode()
        player = Player('Имя', addr)

        if login.startswith("color"):
            data1 = find_color(login[6:])
            player.name, player.color = data1

        s.merge(player)
        s.commit()

        addr = f'({addr[0]},{addr[1]})'
        data = s.query(Player).filter(Player.address == addr)
        for user in data:
            player = LocalPlayer(user.id, player.name, new_socket, addr).load()
            players[user.id] = player
    except BlockingIOError:
        pass

    for id in list(players):  # Пробегаемся по списку игроков
        try:
            data = players[id].sock.recv(1024).decode()  # Получаеми сообщения от клиентов игроков
            print("Получил", data)
            players[id].change_speed(data)
            players[id].db.sync()
        except:
            pass

    # Определим, что видит каждый игрок
    visible_bacteries = {}
    for id in list(players):
        visible_bacteries[id] = []

    pairs = list(players.items())
    for i in range(0, len(pairs)):
        for j in range(i + 1, len(pairs)):
            # Рассматриваем пару игроков
            hero_1: LocalPlayer = pairs[i][1]
            hero_2: LocalPlayer = pairs[j][1]
            dist_x = hero_2.x - hero_1.x
            dist_y = hero_2.y - hero_1.y

            # i-й игрок видит j-того
            if abs(dist_x) <= hero_1.w_vision // 2 + hero_2.size and abs(dist_y) <= hero_1.h_vision // 2 + hero_2.size:
                # Подготовим данные к добавлению в список
                x_ = str(round(dist_x))
                y_ = str(round(dist_y))  # временные
                size_ = str(round(hero_2.size))
                color_ = hero_2.color

                data = x_ + " " + y_ + " " + size_ + " " + color_
                visible_bacteries[hero_1.id].append(data)

            # j-й игрок видит i-того
            if abs(dist_x) <= hero_2.w_vision // 2 + hero_1.size and abs(dist_y) <= hero_2.h_vision // 2 + hero_1.size:
                # Подготовим данные к добавлению в список
                x_ = str(round(-dist_x))
                y_ = str(round(-dist_y))  # временные
                size_ = str(round(hero_1.size))
                color_ = hero_1.color

                data = x_ + " " + y_ + " " + size_ + " " + color_
                visible_bacteries[hero_2.id].append(data)

    # Формируем ответ каждой бактерии
    for id in list(players):
        visible_bacteries[id] = "<" + ",".join(visible_bacteries[id]) + ">"
        print(visible_bacteries[id])


    # Отправка статус игрового поля
    for id in list(players): # пробегаемся по списку игроков, берем их сокеты в sock
        try: # пробуем исполнить код
            players[id].sock.send(visible_bacteries[id].encode())
        except: # если в теле try ошибка, то
            players[id].sock.close()
            del players[id]
            # Так же удаляем строчку из БД
            s.query(Player).filter(Player.id == id).delete()
            s.commit()
            print("Сокет закрыт")

    # Отрисовываем серверное окно
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            server_works = False

    screen.fill('black')
    for id in list(players):
        player = players[id]
        x = player.x * WIDHT_SERVER // WIDHT_ROOM
        y = player.y * HEIGHT_SERVER // HEIGHT_ROOM
        size = player.size * WIDHT_SERVER // WIDHT_ROOM
        pygame.draw.circle(screen, player.color, (x, y), size)
    for id in list(players):
        player = players[id]
        players[id].update()
    pygame.display.update()




pygame.quit()
main_socket.close()
s.query(Player).delete()
s.commit()