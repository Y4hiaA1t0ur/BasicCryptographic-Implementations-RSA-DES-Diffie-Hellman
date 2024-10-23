import socket
import threading


class ChatServer:
    def __init__(self, host='127.0.0.1', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        print(f"[LISTENING] Server is listening on {host}:{port}")

    def handle_client(self, client_socket, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        thread = threading.Thread(target=self.receive_messages, args=(client_socket, addr))
        thread.start()

        # Allow the server to send messages
        while True:
            server_message = input("Server: ")
            self.send_message(client_socket, f"Server: {server_message}")

    def receive_messages(self, client_socket, addr):
        while True:
            try:
                # Receive message from client
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    print(f"[{addr}] {message}")
                else:
                    print(f"[DISCONNECT] {addr} disconnected.")
                    break
            except:
                print(f"[ERROR] Connection with {addr} lost.")
                break

    def send_message(self, client_socket, message):
        client_socket.send(message.encode('utf-8'))

    def start(self):
        print("[STARTING] Server is starting...")
        while True:
            client_socket, addr = self.server.accept()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
            self.handle_client(client_socket, addr)


server = ChatServer()
server.start()
