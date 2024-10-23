class MatrixBin:
    def __init__(self):
        pass

    @staticmethod
    def binary_to_matrix(num, a, b):
        binary_str = bin(num)[2:]

        required_length = a * b
        binary_str = binary_str.zfill(required_length)

        if len(binary_str) != required_length:
            raise ValueError("The binary number cannot fill the matrix of size {}x{}.".format(a, b))

        matrix = []
        for i in range(a):
            row = binary_str[i * b:(i + 1) * b]
            matrix.append([int(bit) for bit in row])  # List of integers

        return matrix

    @staticmethod
    def matrix_to_binary(matrix_input):
        binary_str = ''.join(str(bit) for row in matrix_input for bit in row)
        binary_num = int(binary_str, 2)
        return binary_num

    @staticmethod
    def binary_to_bit_array(binary_number):
        binary_str = bin(binary_number)[2:]
        bit_array = [int(bit) for bit in binary_str]
        return bit_array

    @staticmethod
    def bit_array_to_binary(bit_array):
        binary_str = ''.join(str(bit) for bit in bit_array)
        binary_number = int(binary_str, 2)
        return binary_number

    @staticmethod
    def flatten_matrix(matrix):
        return [element for row in matrix for element in row]

    @staticmethod
    def add_zeros_to_array(input_array, desired_size):
        # Calculate the number of zeros to add
        zeros_to_add = desired_size - len(input_array)

        # If the input array is already larger than the desired size, return it as is
        if zeros_to_add <= 0:
            return input_array

        # Create a new array with the zeros added at the front
        new_array = [0] * zeros_to_add + input_array

        return new_array

    @staticmethod
    def split_binary_array(binary_array):
        # Calculate the middle index to split the array
        middle = len(binary_array) // 2

        # Split the array into left and right halves
        left_half = binary_array[:middle]
        right_half = binary_array[middle:]

        return left_half, right_half

    @staticmethod
    def split_binary_into_chunks(binary_int, chunk_size):
        # Convert the binary integer to a string representation (remove '0b' prefix)
        binary_str = bin(binary_int)[2:]

        # Pad the binary string with leading zeros to ensure it's a multiple of the chunk size
        padded_binary_str = binary_str.zfill(((len(binary_str) + chunk_size - 1) // chunk_size) * chunk_size)

        # Split the binary string into chunks of the specified size
        chunks = [padded_binary_str[i:i + chunk_size] for i in range(0, len(padded_binary_str), chunk_size)]

        # Convert each chunk from string to integer
        return [int(chunk, 2) for chunk in chunks]

    @staticmethod
    def combine_chunks_into_binary(chunk_list, chunk_size):
        # Convert each integer chunk back to its binary string representation, padded to the chunk size
        binary_str = ''.join([format(chunk, f'0{chunk_size}b') for chunk in chunk_list])

        # Convert the combined binary string back to an integer
        return int(binary_str, 2)