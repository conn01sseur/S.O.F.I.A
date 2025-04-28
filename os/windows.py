import socket

host = "185.255.135.212"
port = 7778

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

while True:
    try:
        data = client_socket.recv(1024)
        if not data:
            break;
        print(data.decode())
    except:
        pass