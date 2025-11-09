if __name__ == "__main__":
    quit("не запускай меня, запускай main.py")

import socket
import pygame

is_server = False
use_lan = True
biba_port = 31000 # порт игрока
boba_port = None # порт клиента узнаем при подключении
biba_ip = None
boba_ip = None
biba_sock = None
boba_sock = None
MAX_PACKET = 1000 # сколько данных ожидать при приёме

# настройки сетевой игры
def init():
    global is_server
    global use_lan

    mode = input("Режим игры: 1 - одиночная игра, 2 - сервер, 3 - клиент >> ")
    match mode:
        case '2': 
            is_server = True
            use_lan = True
        case '3': 
            is_server = False
            use_lan = True
        case _: 
            use_lan = False

    if not use_lan:        
        print("ты в одиночке")
    else: # сетевая:
        print("ты в не одиночке")
        print(f"это сервер? {'да' if is_server else 'нет'}")
        if is_server:
            init_server()
        else:
            init_client()

def init_server():
    global biba_sock, boba_sock, boba_ip
    print("запуск сервера")
    biba_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    biba_sock.bind(('0.0.0.0', biba_port))
    biba_sock.listen(1)
    print("Жду входящий...")
    boba_sock, boba_ip = biba_sock.accept()
    print(f'IP клиента: {boba_ip}')

def init_client():
    global biba_sock, biba_ip
    print("запуск клиента")
    biba_ip = input("IP адрес сервера ")
    biba_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("подключение к серверу...")
    biba_sock.connect((biba_ip, biba_port))
    print("подключился")

def send_data(text):
    if not use_lan:
        return
    
    text += '%'
    try:
        if is_server:
            # Сервер отправляет через клиентский сокет
            boba_sock.sendall(text.encode('utf-8'))
        else:
            # Клиент отправляет через свой сокет
            biba_sock.sendall(text.encode('utf-8'))
    except Exception as e:
        print(f"Ошибка отправки: {e}")

def upload_data():  # Исправлено имя функции (было upload_date)
    if not use_lan:
        return

    try:
        if is_server:
            data = boba_sock.recv(MAX_PACKET)
        else:
            data = biba_sock.recv(MAX_PACKET)
        
        if data:
            message = data.decode('utf-8')
            return message
    except BlockingIOError:
        # Нет данных для чтения - это нормально
        return None
    except Exception as e:
        print(f"Ошибка получения: {e}")
        return None
    
    return None
