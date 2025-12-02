import socket
import time
from db import *
import pygame

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

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

pygame.init()

WIDHT_ROOM, HEIGHT_ROOM = 4000, 4000
WIDHT_SERVER, HEIGHT_SERVER = 300, 300
FPS = 60

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
        player = Player('Имя', addr)
        s.merge(player)
        s.commit()
        addr = f'({addr[0]},{addr[1]})'
        data = s.query(Player).filter(Player.address == addr)
        for user in data:
            player = LocalPlayer(user.id, "Имя", new_socket, addr)
            players[user.id] = player
    except BlockingIOError:
        pass

    for id in players:  # Пробегаемся по списку игроков
        try:
            data = players[id].sock.recv(1024).decode()  # Получаеми сообщения от клиентов игроков
            print("Получил", data)
        except:
            pass

    # Отправка статус игрового поля
    for id in players: # пробегаемся по списку игроков, берем их сокеты в sock
        try: # пробуем исполнить код
            players[id].sock.send("LOL".encode())
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
        pygame.draw.circle(screen, "yellow2", (x, y), size)

pygame.display.update()

pygame.quit()
main_socket.close()
s.query(Player).delete()
s.commit()