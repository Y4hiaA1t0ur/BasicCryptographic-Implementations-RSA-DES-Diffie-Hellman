from MyDES.KeyManager import KeyManager
from MyDES.MatrixBin import MatrixBin
from MyDES.Permutations import Permutations
from MyDES.Round import Round


class MyDES:
    def __init__(self, key=None):
        if key is None:
            self.__r_keys = KeyManager.generate_round_keys(KeyManager.generate_main_key())
        else:
            self.__r_keys = KeyManager.generate_round_keys(key)

    @staticmethod
    def des(msg, rounds_keys):
        ip_output = MatrixBin.matrix_to_binary(
            Permutations.initial_permutation(MatrixBin.add_zeros_to_array(MatrixBin.binary_to_bit_array(msg), 64)))
        left_half_array, right_half_array = MatrixBin.split_binary_array(
            MatrixBin.add_zeros_to_array(MatrixBin.binary_to_bit_array(ip_output), 64))

        left_half = MatrixBin.bit_array_to_binary(left_half_array)
        right_half = MatrixBin.bit_array_to_binary(right_half_array)

        for round_number in range(0, 16):
            old_left_half = left_half
            old_right_half = right_half
            right_half = Round.mangler_function(right_half, int(rounds_keys[round_number]))
            right_half = right_half ^ old_left_half
            left_half = old_right_half

        swap_output = MatrixBin.add_zeros_to_array(MatrixBin.binary_to_bit_array(right_half),
                                                   32) + MatrixBin.add_zeros_to_array(
            MatrixBin.binary_to_bit_array(left_half), 32)
        final_output = MatrixBin.matrix_to_binary(Permutations.inverse_permutation(swap_output))
        return final_output

    def encrypt(self, message):
        return self.des(message, self.__r_keys)

    def decrypt(self, message):
        return self.des(message, self.__r_keys[::-1])


# test_msg = 0b1111000011110000111100001111000011110000111100001111000011110000
#
# DES = MyDES()
# encrypted = DES.encrypt(test_msg)
# print(bin(encrypted))
# decrypted = DES.decrypt(encrypted)
# print(bin(decrypted))
