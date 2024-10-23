import socket
import threading


class ChatClient:
    def __init__(self, host='127.0.0.1', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        print(f"[CONNECTED] Connected to server at {host}:{port}")

    def receive_messages(self):
        while True:
            try:
                # Receive message from server
                message = self.client.recv(1024).decode('utf-8')
                if message:
                    print(f"{message}")
            except:
                print("[ERROR] Connection closed.")
                break

    def send_message(self, message):
        self.client.send(message.encode('utf-8'))

    def start(self):
        # Thread for receiving messages from the server
        thread = threading.Thread(target=self.receive_messages)
        thread.start()

        # Sending messages to server
        while True:
            message = input("You: ")
            self.send_message(message)


client = ChatClient()
client.start()
