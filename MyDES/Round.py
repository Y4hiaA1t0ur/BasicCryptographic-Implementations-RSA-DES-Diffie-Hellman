from MyDES.MatrixBin import MatrixBin
from .Permutations import Permutations


class Round:
    def __init__(self):
        pass

    @staticmethod
    def mangler_function(right_half, round_key):
        first_step = MatrixBin.matrix_to_binary(Permutations.expansion_permutation(
            MatrixBin.add_zeros_to_array(MatrixBin.binary_to_bit_array(right_half), 32)))
        first_step = first_step ^ round_key

        second_step = Round.des_s_box_substitution(first_step)
        return MatrixBin.matrix_to_binary(
            Permutations.permutation_function_p(
                MatrixBin.add_zeros_to_array(MatrixBin.binary_to_bit_array(int(second_step, 2)), 32)))

    @staticmethod
    def des_s_box_substitution(input_int):
        # DES S-boxes
        s_boxes = [
            [
                [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
                [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
                [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
                [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
            ],
            [
                [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
                [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
                [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
                [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
            ],
            [
                [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 2, 8, 4, 7, 12, 11],
                [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
                [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
                [2, 12, 4, 15, 1, 10, 14, 7, 6, 11, 0, 13, 9, 5, 3, 8]
            ],
            [
                [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
                [13, 0, 11, 7, 4, 9, 1, 10, 2, 8, 5, 14, 6, 3, 15, 12],
                [4, 7, 13, 1, 2, 14, 0, 9, 10, 6, 11, 12, 5, 3, 8, 15],
                [1, 10, 13, 4, 2, 8, 7, 14, 15, 11, 6, 12, 0, 5, 9, 3]
            ],
            [
                [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 14, 0, 15, 9, 13],
                [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
                [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
                [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
            ],
            [
                [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
                [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
                [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
                [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
            ],
            [
                [4, 11, 2, 14, 15, 0, 8, 13, 3, 7, 10, 6, 1, 9, 5, 12],
                [13, 0, 11, 7, 4, 9, 1, 10, 2, 8, 5, 14, 6, 3, 15, 12],
                [1, 4, 11, 13, 0, 14, 9, 7, 3, 10, 2, 15, 5, 6, 8, 12],
                [3, 9, 7, 10, 4, 6, 8, 15, 12, 0, 1, 2, 14, 11, 13, 5]
            ],
            [
                [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
                [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
                [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
                [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
            ]
        ]

        output_bin = ""

        # Extract 8 groups of 6 bits
        for i in range(8):
            six_bits = (input_int >> (42 - (i * 6))) & 0b111111  # Get 6 bits
            row = (six_bits & 0b100000) >> 5 | (six_bits & 0b000001)  # First and last bits for row
            col = (six_bits >> 1) & 0b000111  # Middle four bits for column

            # Get the corresponding S-box value
            s_value = s_boxes[i][row][col]

            # Convert the S-box output (4-bit) to binary and append to output
            output_bin += f"{s_value:04b}"

        return output_bin
