import socket
import threading
import json
from datetime import datetime

class SocketServer:
    def __init__(self, host='localhost', port=7780):
        self.host = host
        self.port = port
        self.server_socket = None
        self.connected_clients = []
        self.lock = threading.Lock()
        self.running = False
        self.message_handler = None

    def start(self):
        """Запуск сервера для прослушивания подключений"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        
        print(f"[SOCKET] Server started on {self.host}:{self.port}")
        
        accept_thread = threading.Thread(target=self._accept_connections, daemon=True)
        accept_thread.start()

    def stop(self):
        """Остановка сервера"""
        self.running = False
        with self.lock:
            for client in self.connected_clients:
                client.close()
            self.connected_clients = []
        
        if self.server_socket:
            self.server_socket.close()
        
        print("[SOCKET] Server stopped")

    def _accept_connections(self):
        """Принимает новые подключения"""
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                print(f"[SOCKET] New connection from {addr}")
                
                with self.lock:
                    self.connected_clients.append(client_socket)
                
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket, addr),
                    daemon=True
                )
                client_thread.start()
                
            except Exception as e:
                if self.running:
                    print(f"[SOCKET ERROR] Accept error: {e}")
                break

    def _handle_client(self, client_socket, addr):
        """Обрабатывает сообщения от клиента"""
        try:
            while self.running:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                print(f"[SOCKET] Received from {addr}: {data}")
                
                try:
                    message = json.loads(data)
                    self._process_message(message, client_socket, addr)
                    
                except json.JSONDecodeError:
                    print(f"[SOCKET] Invalid JSON from {addr}")
                    response = {"status": "error", "message": "Invalid JSON format"}
                    client_socket.send(json.dumps(response).encode('utf-8'))
                    
        except Exception as e:
            print(f"[SOCKET ERROR] Client {addr} error: {e}")
        finally:
            self._disconnect_client(client_socket, addr)

    def _process_message(self, message, client_socket, addr):
        """Обрабатывает полученное сообщение"""
        try:
            # Пример обработки разных типов сообщений
            if message.get('type') == 'command':
                command = message.get('command')
                params = message.get('params', {})
                
                print(f"[SOCKET] Command from {addr}: {command} {params}")
                
                # Здесь можно добавить обработку конкретных команд
                if command == 'device_status':
                    response = {
                        "status": "success",
                        "data": {
                            "device": "Smart Home Controller",
                            "status": "online",
                            "time": str(datetime.now())
                        }
                    }
                    client_socket.send(json.dumps(response).encode('utf-8'))
                
                elif command == 'notification':
                    if self.message_handler:
                        self.message_handler(message)
                    response = {"status": "success", "message": "Notification processed"}
                    client_socket.send(json.dumps(response).encode('utf-8'))
                
                else:
                    response = {"status": "error", "message": "Unknown command"}
                    client_socket.send(json.dumps(response).encode('utf-8'))
            
            else:
                response = {"status": "error", "message": "Invalid message type"}
                client_socket.send(json.dumps(response).encode('utf-8'))
                
        except Exception as e:
            print(f"[SOCKET ERROR] Message processing error: {e}")
            response = {"status": "error", "message": str(e)}
            client_socket.send(json.dumps(response).encode('utf-8'))

    def _disconnect_client(self, client_socket, addr):
        """Обрабатывает отключение клиента"""
        try:
            with self.lock:
                if client_socket in self.connected_clients:
                    self.connected_clients.remove(client_socket)
            client_socket.close()
            print(f"[SOCKET] Client {addr} disconnected")
        except Exception as e:
            print(f"[SOCKET ERROR] Disconnect error: {e}")

    def broadcast_message(self, message):
        """Отправляет сообщение всем подключенным клиентам"""
        if not isinstance(message, str):
            message = json.dumps(message)
            
        with self.lock:
            disconnected_clients = []
            
            for client in self.connected_clients:
                try:
                    client.send(message.encode('utf-8'))
                except Exception as e:
                    print(f"[SOCKET ERROR] Broadcast failed: {e}")
                    disconnected_clients.append(client)
            
            # Удаляем отключенных клиентов
            for client in disconnected_clients:
                if client in self.connected_clients:
                    self.connected_clients.remove(client)
                    client.close()

    def send_to_client(self, client_socket, message):
        """Отправляет сообщение конкретному клиенту"""
        if not isinstance(message, str):
            message = json.dumps(message)
            
        try:
            with self.lock:
                if client_socket in self.connected_clients:
                    client_socket.send(message.encode('utf-8'))
                    return True
        except Exception as e:
            print(f"[SOCKET ERROR] Send to client failed: {e}")
            self._disconnect_client(client_socket, "unknown")
        
        return False

    def set_message_handler(self, handler):
        """Устанавливает обработчик входящих сообщений"""
        self.message_handler = handler