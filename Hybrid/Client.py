import json
import socket
import threading

from Hybrid.OneFileHybrid import MessageSignaturePackage
from MyDES.ECB import MyECB
from MyDiffieHellman.DiffieHellman import MyDeffieHellman


# Client class to connect to the server
class ChatClient:
    def __init__(self, host='127.0.0.1', port=12345):
        self.des_started = False
        self.ecb = None
        self.received_messages = []
        self.encrypted_array = []
        self.received_messages_condition = threading.Condition()  # Create a condition variable
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

        # Start receiving messages in a separate thread
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_array(self, message_list):
        message_json = json.dumps(message_list).encode('utf-8')
        self.client_socket.send(message_json)

    # Receive messages from the server
    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    with self.received_messages_condition:
                        if not self.des_started:
                            self.received_messages.append(message)
                            self.received_messages_condition.notify()
                        else:
                            if message == "FIN":
                                self.ecb.ecb_decrypt(self.encrypted_array)
                                print("Alice: " + self.ecb.ecb_decrypt(self.encrypted_array))
                                self.encrypted_array = []
                            else:
                                self.encrypted_array.append(int(message))
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


Bob = ChatClient()

with Bob.received_messages_condition:
    while len(Bob.received_messages) < 2:
        Bob.received_messages_condition.wait()

p = int(Bob.received_messages.pop(0))
g = int(Bob.received_messages.pop(0))
bob_deffi = MyDeffieHellman(p, g)
# Create the shared key
des_key = MessageSignaturePackage.create_shared_key(Bob, bob_deffi)
a=1+1
Bob.des_started = True
print("des key:")
print(des_key)
Bob.ecb = MyECB(des_key)

message_thread = threading.Thread(target=MessageSignaturePackage.message_sender_loop, args=(Bob,))
message_thread.start()
