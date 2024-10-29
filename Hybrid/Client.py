import socket
import threading

from Hybrid.OneFileHybrid import MessageSignaturePackage
from MyDiffieHellman.DiffieHellman import MyDeffieHellman


# Client class to connect to the server
class ChatClient:
    def __init__(self, host='127.0.0.1', port=12345):
        self.received_messages = []
        self.received_messages_condition = threading.Condition()  # Create a condition variable
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

        # Start receiving messages in a separate thread
        threading.Thread(target=self.receive_messages, daemon=True).start()

    # Receive messages from the server
    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    with self.received_messages_condition:  # Lock the condition variable
                        self.received_messages.append(message)
                        print("received messages: ")
                        print(self.received_messages)
                        self.received_messages_condition.notify()  # Notify waiting threads
            except Exception as e:
                print("Connection closed by the server:", e)
                break

    def send_message(self, message):
        self.client_socket.send(message.encode('utf-8'))

    # Send messages to the server
    def send_messages_chat(self):
        while True:
            message = input("You: ")  # Input for the client
            self.client_socket.send(message.encode('utf-8'))


# Create the client and initialize Diffie-Hellman
Bob = ChatClient()
print("bob is made")

# Wait for the first two messages (p and g) to be received
with Bob.received_messages_condition:  # Lock the condition variable
    while len(Bob.received_messages) < 2:  # Ensure both p and g are received
        Bob.received_messages_condition.wait()  # Wait until notified

# Now pop the first two values for p and g
p = int(Bob.received_messages.pop(0))
g = int(Bob.received_messages.pop(0))
bob_deffi = MyDeffieHellman(p, g)
# Create the shared key
MessageSignaturePackage.create_shared_key(Bob, bob_deffi)
