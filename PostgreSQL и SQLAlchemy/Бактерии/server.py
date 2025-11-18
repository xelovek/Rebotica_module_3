import socket
import time

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Создает главный сокет (прихожую)
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) # Отключаем пакетирование, чтобы передавать все каждый кадр игры
main_socket.bind(("localhost", 10000)) # Устанавливаем ip-адрес и порт, localhost - это локальный адрес этого компа

main_socket.setblocking(False) # Отключаем завершение подключения
main_socket.listen(5) # Включаем прослушку юзеров например 5 одновременно
print('Сокет создался')

players = []

while True:
    try:
        # проверяем желающих войти в игру
        new_socket, addr = main_socket.accept()  # принимаем входящие
        print('Подключился', addr)
        new_socket.setblocking(False) # Отключаем завершение подключения для новых игроков
        players.append(new_socket) # Добавляем игроков в список

        for sock in players: # Пробегаемся по списку игроков
            try:
                data = sock.recv(1024).decode() # Получаеми сообщения от клиентов игроков
                print("Получил", data)
            except:
                pass

    except BlockingIOError:
        pass