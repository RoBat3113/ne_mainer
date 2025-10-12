if __name__ == "__main__":
    quit("не запускай меня, запускай main.py")

import socket
import pygame

'''
пример кнопки
KEY|up

клиент вышел
CLIENT_EXIT

рисование текста
TXT|x|y|text|font_size
TXT|100|200|санс заценил|60


это для клиента:
KEYDOWN:w          - нажата клавиша W
KEYUP:w            - отпущена клавиша W
MOUSE_MOVE:100:200 - движение мыши на координаты x=100, y=200  
MOUSE_DOWN:left    - нажата левая кнопка мыши
MOUSE_UP:right     - отпущена правая кнопка мыши

это для сервера:
PLAYER_HP:75       - у игрока 75 HP
PLAYER_AMMO:30     - осталось 30 патронов
PLAYER_SCORE:1500  - счет игрока 1500
GAME_TIME:120      - прошло 120 секунд игры
ENEMY_COUNT:5      - осталось 5 врагов
SPRITE_HIDE:enemy  - скрыть спрайт
SPRITE_SHOW:bullet - показать спрайт
SPRITE_RENDER:x:y:name:angle
'''
def wait_message():
    if im_server:
        data = sock.recv(MAX_PACKET)
        if data:
            message = data.decode('utf-8')
            print(f"С клиента пришло это: {message}")
    else:
        pass


server_port = 31000 # порт игрока
client_port = None # порт клиента узнаем при подключении
client_ip = None
server_ip = None
sock = None
client_sock = None
im_server = False # режим сервер/клиент
use_lan = False # True - сетевая игра запущена
MAX_PACKET = 1000 # сколько данных ожидать при приёме

def server_start():
    global sock
    global client_ip
    global im_server
    global client_sock
    print("запуск сервера")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', server_port))
    sock.listen(1) # <-- сколько игроков максимум может подключиться

    print("Жду входящий...")
    client_sock, client_ip = sock.accept()
    print(f'IP клиента: {client_ip}')
    im_server = True

def client_start():
    global sock
    global im_server
    global server_ip
    print("запуск клиента")
    server_ip = input("IP адрес сервера ")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, server_port))
    im_server = False
    print("подключено к серверу")

    while True:
        data = sock.recv(MAX_PACKET)
        if data:
            message = data.decode('utf-8')
            print(f"С сервера пришло это: {message}")

# настройки сетевой игры
def init():
    mode = input("Режим игры: 1 - одиночная игра, 2 - сервер, 3 - клиент >> ")
    match mode:
        case '2': server_start()
        case '3': client_start()
        case _: return # одиночная игра

def send_text(text):
    if not use_lan:
        return
    text += '%'
    if im_server:
        print("я сервер")
        #sock.sendto(text.encode('utf-8'), client_ip)
        client_sock.sendall(text.encode('utf-8'))
    else:
        sock.sendall(text.encode('utf-8'))

def send_to_client(keys):
    if not im_server:
        return

    if (keys[pygame.K_LEFT]  or keys[pygame.K_a]): send_text( "KEYDOWN:L")
    if (keys[pygame.K_UP]    or keys[pygame.K_w]): send_text( "KEYDOWN:U")
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]): send_text( "KEYDOWN:R")
    if (keys[pygame.K_DOWN]  or keys[pygame.K_s]): send_text( "KEYDOWN:D")
    if (keys[pygame.K_SPACE]): send_text("KEYDOWN:SHOT")

def close_from_game():
    pass