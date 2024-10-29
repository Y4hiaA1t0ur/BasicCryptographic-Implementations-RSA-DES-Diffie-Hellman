import random

from Crypto.Util import number


def generate_random_int(bit_size):
    max_value = (1 << bit_size) - 1  # This is 2^bit_size - 1
    return random.randint(0, max_value)


class MyDeffieHellman:
    def __init__(self, p=None, g=None, private_key_size=2048):
        if p is None and g is None:
            self.p, self.g = MyDeffieHellman.p_and_g_generator(private_key_size)
        else:
            self.p = p
            self.g = g
        self.private_key = generate_random_int(private_key_size)

    @staticmethod
    def p_and_g_generator(p_size):
        prime_max_5bits_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
        return number.getStrongPrime(p_size), random.choice(prime_max_5bits_numbers)

    def make_public_key(self):
        public_key = pow(self.g, self.private_key, self.p)
        return public_key

    def get_secret_key(self, public_key):
        secret_key = pow(public_key, self.private_key, self.p)
        return secret_key


# alice = MyDeffieHellman()
# bob = MyDeffieHellman(alice.p, alice.g)
#
# A = alice.make_public_key()
# B = bob.make_public_key()
#
# secret_key_alice = alice.get_secret_key(B)
# secret_key_bob = bob.get_secret_key(A)
#
# print("Alice's Secret Key:", secret_key_alice)
# print("Bob's Secret Key:", secret_key_bob)
#
# if secret_key_alice != secret_key_bob:
#     print("Secret keys do not match!")
# else:
#     print("Secret keys match!")
