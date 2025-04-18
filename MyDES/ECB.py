from MyDES.MatrixBin import MatrixBin
from MyDES.MyDESMain import MyDES


class MyECB:
    def __init__(self, key=None):
        self.__des = MyDES(key)

    def ecb_encrypt(self, plaintext):
        message_int = int.from_bytes(plaintext.encode('utf-8'), byteorder='big')
        chunks_array = MatrixBin.split_binary_into_chunks(message_int, 64)
        output_array = [self.__des.encrypt(chunk) for chunk in chunks_array]
        return output_array

    def ecb_decrypt(self, output_array):
        decrypted_array = [self.__des.decrypt(chunk) for chunk in output_array]
        message_int = MatrixBin.combine_chunks_into_binary(decrypted_array, 64)
        byte_length = (message_int.bit_length() + 7) // 8
        decrypted_bytes = message_int.to_bytes(byte_length, byteorder='big')
        return decrypted_bytes.decode('utf-8')


# #
# ECB = MyECB()
# msg = "Hi world!"
# encrypted_msg = ECB.ecb_encrypt(msg)
# print(type(encrypted_msg[0]))
# decrypted_msg = ECB.ecb_decrypt([10536776382724176978])
# print(decrypted_msg)
