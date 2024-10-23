import gmpy2
from Crypto.Util import number


class PnQGenerator:
    def __init__(self):
        pass

    @staticmethod
    def get_rsa_numbers(bit_size, max_attempts):
        for attempt in range(max_attempts):
            p = number.getStrongPrime(bit_size)
            q = number.getStrongPrime(bit_size)
            n = p * q

            # Calculate the integer 4th root of n using gmpy2
            n_root_4, exact = gmpy2.iroot(n, 4)

            if abs(p - q) > n_root_4:
                return p, q, n

        raise ValueError("Failed to find suitable primes in the allowed attempts.")

