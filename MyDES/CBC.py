# Continue Later

from MyDES.KeyManager import KeyManager
from MyDES.MatrixBin import MatrixBin
from MyDES.MyDESMain import MyDES


class MyCBC:
    def __init__(self):
        self.__des = MyDES()
        self.iv = int(KeyManager.generate_main_key())  # we need a 64-bit number and it does just that

    def __cbc_encryption_loop(self, chunks_array, xored, loop_num):
        if loop_num == len(chunks_array):
            return chunks_array
        else:
            des_input = chunks_array[loop_num] ^ xored
            chunks_array[loop_num] = self.__des.encrypt(des_input)
            return self.__cbc_encryption_loop(chunks_array, chunks_array[loop_num - 1], loop_num + 1)

    def __cbc_decryption_loop(self, chunks_array, xored, loop_num):
        if loop_num == len(chunks_array):
            return chunks_array
        else:
            ciphered_chunk = chunks_array[loop_num]
            chunk = self.__des.decrypt(ciphered_chunk)
            plain_chunk = chunk ^ xored
            chunks_array[loop_num] = plain_chunk
            return self.__cbc_decryption_loop(chunks_array, ciphered_chunk, loop_num + 1)

    def encrypt(self, plaintext):
        message_int = int.from_bytes(plaintext.encode('utf-8'), byteorder='big')
        chunks_array = MatrixBin.split_binary_into_chunks(message_int, 64)
        self.__cbc_encryption_loop(chunks_array, self.iv, 0)
        return chunks_array

    def decrypt(self, cipher_array):
        plaintext_array = self.__cbc_decryption_loop(cipher_array, self.iv, 0)
        print(plaintext_array)
        message_int = MatrixBin.combine_chunks_into_binary(plaintext_array, 64)
        byte_length = (message_int.bit_length() + 7) // 8
        decrypted_bytes = message_int.to_bytes(byte_length, byteorder='big')
        return decrypted_bytes.decode('utf-8')


CBC = MyCBC()
msg = input('Enter message: ')
encrypted_msg = CBC.encrypt(msg)
print(encrypted_msg)
decrypted_msg = CBC.decrypt(encrypted_msg)
print(decrypted_msg)
