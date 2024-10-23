class Permutations:
    def __init__(self):
        pass

    @staticmethod
    def position_array_in_matrix(array, matrix):
        rows = len(matrix)
        cols = len(matrix[0]) if rows > 0 else 0

        output_matrix = [[0] * cols for _ in range(rows)]

        for i in range(rows):
            for j in range(cols):
                index = matrix[i][j] - 1
                output_matrix[i][j] = array[index]
        return output_matrix

    @staticmethod
    def initial_permutation(binary_array):
        ip_table = [
            [58, 50, 42, 34, 26, 18, 10, 2],
            [60, 52, 44, 36, 28, 20, 12, 4],
            [62, 54, 46, 38, 30, 22, 14, 6],
            [64, 56, 48, 40, 32, 24, 16, 8],
            [57, 49, 41, 33, 25, 17, 9, 1],
            [59, 51, 43, 35, 27, 19, 11, 3],
            [61, 53, 45, 37, 29, 21, 13, 5],
            [63, 55, 47, 39, 31, 23, 15, 7]
        ]
        return Permutations.position_array_in_matrix(binary_array, ip_table)

    @staticmethod
    def expansion_permutation(binary_array):
        e = [
            [32, 1, 2, 3, 4, 5],
            [4, 5, 6, 7, 8, 9],
            [8, 9, 10, 11, 12, 13],
            [12, 13, 14, 15, 16, 17],
            [16, 17, 18, 19, 20, 21],
            [20, 21, 22, 23, 24, 25],
            [24, 25, 26, 27, 28, 29],
            [28, 29, 30, 31, 32, 1]
        ]
        return Permutations.position_array_in_matrix(binary_array, e)

    @staticmethod
    def permutation_function_p(binary_array):
        p_box = [[16, 7, 20, 21, 29, 12, 28, 17],
                 [1, 15, 23, 26, 5, 18, 31, 10],
                 [2, 8, 24, 14, 32, 27, 3, 9],
                 [19, 13, 30, 6, 22, 11, 4, 25]
                 ]
        return Permutations.position_array_in_matrix(binary_array, p_box)

    @staticmethod
    def inverse_permutation(binary_array):
        ip_inverse_matrix = [
            [40, 8, 48, 16, 56, 24, 64, 32],
            [39, 7, 47, 15, 55, 23, 63, 31],
            [38, 6, 46, 14, 54, 22, 62, 30],
            [37, 5, 45, 13, 53, 21, 61, 29],
            [36, 4, 44, 12, 52, 20, 60, 28],
            [35, 3, 43, 11, 51, 19, 59, 27],
            [34, 2, 42, 10, 50, 18, 58, 26],
            [33, 1, 41, 9, 49, 17, 57, 25]
        ]
        return Permutations.position_array_in_matrix(binary_array, ip_inverse_matrix)


# array_64 = list(range(1, 65))
# array_32 = list(range(1, 33))
#
# # Test initial permutation
# initial_perm_result = Permutations.initial_permutation(array_64)
# print("Initial Permutation Result:")
# print(initial_perm_result)
#
# # Test expansion permutation
# expansion_perm_result = Permutations.expansion_permutation(array_32)
# print("Expansion Permutation Result:")
# print(expansion_perm_result)
#
# # Test permutation function P
# p_perm_result = Permutations.permutation_function_p(array_32)
# print("Permutation Function P Result:")
# print(p_perm_result)
#
# # Test inverse permutation
# inverse_perm_result = Permutations.inverse_permutation(array_64)
# print("Inverse Permutation Result:")
# print(inverse_perm_result)
