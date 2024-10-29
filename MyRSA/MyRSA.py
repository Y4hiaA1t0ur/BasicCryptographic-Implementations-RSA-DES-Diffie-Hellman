from .PnQGenerator import PnQGenerator


class MyRSA:
    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key

    @staticmethod
    def rsa_keys_generator(bit_size=1024, max_attempts=500):
        p, q, n = PnQGenerator.get_rsa_numbers(bit_size, max_attempts)
        e = 65537
        phi_n = (p - 1) * (q - 1)
        d = pow(e, -1, phi_n)

        public_key = e, n
        private_key = d, n

        return public_key, private_key

    def encrypt_block(self, block):
        e, n = self.public_key
        return pow(block, e, n)

    def decrypt_block(self, block):
        d, n = self.private_key
        return pow(block, d, n)

    def encrypt_large_message(self, message):
        e, n = self.public_key
        max_block_size = (n.bit_length() - 1) // 8  # Calculate max block size in bytes
        encrypted_blocks = []

        # Break message into blocks that fit within n's size constraint
        for i in range(0, len(message), max_block_size):
            block = message[i:i + max_block_size].encode('utf-8')
            block_int = int.from_bytes(block, byteorder='big')
            encrypted_block = self.encrypt_block(block_int)
            encrypted_blocks.append(encrypted_block)

        return encrypted_blocks

    def decrypt_large_message(self, encrypted_blocks):
        decrypted_message = bytearray()

        for block in encrypted_blocks:
            decrypted_block_int = self.decrypt_block(block)
            block_size = (decrypted_block_int.bit_length() + 7) // 8
            decrypted_block = decrypted_block_int.to_bytes(block_size, byteorder='big')
            decrypted_message.extend(decrypted_block)

        return decrypted_message.decode('utf-8')

    def encrypt(self, message):
        """Encrypts a large message using block encryption."""
        return self.encrypt_large_message(message)

    def decrypt(self, encrypted_message):
        """Decrypts a large message using block decryption."""
        return self.decrypt_large_message(encrypted_message)


# message_input = input('Enter message: ')
#
# public_k, private_k = MyRSA.rsa_keys_generator()
#
# rsa = MyRSA(public_k, private_k)
# encrypted = rsa.encrypt(message_input)
# print(encrypted)
# decrypted = rsa.decrypt(encrypted)
# print(decrypted)
