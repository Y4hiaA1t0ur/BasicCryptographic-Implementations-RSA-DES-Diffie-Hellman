import socket
import threading

from MyDiffieHellman.DiffieHellman import MyDeffieHellman
from OneFileHybrid import MessageSignaturePackage


# Server class to handle communication with a single client
class ChatServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.received_messages = []
        self.received_messages_condition = threading.Condition()  # Create a condition variable
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(1)
        print("Server is running... Waiting for a client to connect.")

        # Accepting a client
        self.client_socket, self.client_address = self.server_socket.accept()
        print(f"Client connected: {self.client_address}")

        # Start the server to handle client communication
        threading.Thread(target=self.handle_client, daemon=True).start()

    def send_message(self, message):
        self.client_socket.send(message.encode('utf-8'))

    # Handle communication with the connected client
    def handle_client(self):
        while True:
            try:
                # Receive message from the client
                message = self.client_socket.recv(4096).decode('utf-8')
                if message:
                    with self.received_messages_condition:  # Lock the condition variable
                        self.received_messages.append(message)
                        print("received messages: ")
                        print(self.received_messages)
                        self.received_messages_condition.notify()  # Notify waiting threads

            except Exception as e:
                print("Connection closed by the client:", e)
                break

        self.client_socket.close()


# Main execution
Alice = ChatServer()
alice_deffi = MyDeffieHellman()
Alice.send_message(str(alice_deffi.p))
Alice.send_message(str(alice_deffi.g))

# Call the function to create the shared key
MessageSignaturePackage.create_shared_key(Alice, alice_deffi)
