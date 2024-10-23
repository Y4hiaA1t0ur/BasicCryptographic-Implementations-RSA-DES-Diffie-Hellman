from PnQGenerator import PnQGenerator


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

    # Encrypt: ciphertext = message^e mod n
    # Decrypt: message = ciphertext^d mod n

    def simple_encrypt(self, message):
        e, n = self.public_key
        ciphertext = []
        for c in message:
            c_int = ord(c)
            encrypted_c = pow(c_int, e, n)
            ciphertext.append(encrypted_c)
        return ciphertext

    def simple_decrypt(self, ciphertext):
        d, n = self.private_key
        message = []

        for i in ciphertext:
            c_int = pow(i, d, n)
            c = chr(c_int)
            message.append(c)

        return ''.join(message)

    def encrypt(self, message):
        e, n = self.public_key
        message_int = int.from_bytes(message.encode('utf-8'), byteorder='big')
        encrypted_message = pow(message_int, e, n)
        return encrypted_message

    def decrypt(self, encrypted_message):
        d, n = self.private_key
        decrypted_int = pow(encrypted_message, d, n)
        # decrypt int might translate to 1111000 which is a byte but // would give us 0, since its 0,something, so we add 7 ro get it right, if we add 8 we'd have problems with numbers like 11110000
        byte_length = (decrypted_int.bit_length() + 7) // 8
        decrypted_bytes = decrypted_int.to_bytes(byte_length, byteorder='big')
        return decrypted_bytes.decode('utf-8')


message_input = input('Enter message: ')

public_k, private_k = MyRSA.rsa_keys_generator()

rsa = MyRSA(public_k, private_k)
encrypted = rsa.encrypt(message_input)
print(encrypted)
decrypted = rsa.decrypt(encrypted)
print(decrypted)
