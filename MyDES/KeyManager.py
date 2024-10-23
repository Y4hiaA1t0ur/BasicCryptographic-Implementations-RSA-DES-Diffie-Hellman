import secrets


class KeyManager:
    def __init__(self):
        pass

    @staticmethod
    def generate_main_key():
        random_64bit_int = secrets.randbits(64)

        # Convert the integer to a binary string, remove the '0b' prefix, and pad with zeros to ensure 64 bits
        main_key = f"{random_64bit_int:064b}"

        return main_key

    # DES Key Schedule Implementation

    # PC-1 permutation table
    PC1 = [
        57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4
    ]

    # PC-2 permutation table
    PC2 = [
        14, 17, 11, 24, 1, 5,
        3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8,
        16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32
    ]

    @staticmethod
    def permute(key, permutation):
        """ Applies a permutation to the key based on the given permutation table. """
        return ''.join(key[i - 1] for i in permutation)

    @staticmethod
    def rotate_left(key, bits):
        """ Rotates the key left by the specified number of bits. """
        return key[bits:] + key[:bits]

    @staticmethod
    def generate_round_keys(key):
        """ Generates 16 round keys from the provided 56-bit key. """
        # Step 1: Apply PC-1 to create C0 and D0
        key56 = KeyManager.permute(key, KeyManager.PC1)  # Assume input key is 64 bits (with parity bits)
        C0 = key56[:28]  # First 28 bits
        D0 = key56[28:]  # Last 28 bits

        round_keys = []

        for i in range(16):
            # Rotate C and D
            if i in [0, 1, 8, 15]:
                C0 = KeyManager.rotate_left(C0, 1)  # Rotate left by 1
                D0 = KeyManager.rotate_left(D0, 1)  # Rotate left by 1
            else:
                C0 = KeyManager.rotate_left(C0, 2)  # Rotate left by 2
                D0 = KeyManager.rotate_left(D0, 2)  # Rotate left by 2

            # Combine and permute using PC-2 to get Ki
            round_key = KeyManager.permute(C0 + D0, KeyManager.PC2)
            round_keys.append(round_key)
        return round_keys
