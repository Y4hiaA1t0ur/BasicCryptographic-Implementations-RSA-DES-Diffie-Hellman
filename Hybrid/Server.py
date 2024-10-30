import socket
import threading

from MyDES.ECB import MyECB
from MyDiffieHellman.DiffieHellman import MyDeffieHellman
from OneFileHybrid import MessageSignaturePackage


# Server class to handle communication with a single client
class ChatServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.encrypted_array = []
        self.des_started = False
        self.ecb = None
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
                    with self.received_messages_condition:
                        if not self.des_started:
                            # Normal message handling before DES starts
                            self.received_messages.append(message)
                            self.received_messages_condition.notify()
                        else:
                            if message == "FIN":
                                self.ecb.ecb_decrypt(self.encrypted_array)
                                print("Bob: " + self.ecb.ecb_decrypt(self.encrypted_array))
                                self.encrypted_array = []
                            else:
                                self.encrypted_array.append(int(message))
                                print("encrypted message arrived")
            except Exception as e:
                print("Connection closed by the client:", e)
                break

        self.client_socket.close()


Alice = ChatServer()
alice_deffi = MyDeffieHellman()
Alice.send_message(str(alice_deffi.p))
Alice.send_message(str(alice_deffi.g))

des_key = MessageSignaturePackage.create_shared_key(Alice, alice_deffi)
Alice.des_started = True
print("des key:")
print(des_key)
Alice.ecb = MyECB(des_key)

# Now to create a thread for it:
message_thread = threading.Thread(target=MessageSignaturePackage.message_sender_loop, args=(Alice,))
message_thread.start()
