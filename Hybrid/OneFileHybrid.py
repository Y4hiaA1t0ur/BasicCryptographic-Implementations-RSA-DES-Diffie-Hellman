import ast
import hashlib
import time

from MyRSA.MyRSA import MyRSA


class MessageSignaturePackage:
    def __init__(self, message):
        self.message = message
        self.public_k, self.__private_k = MyRSA.rsa_keys_generator()
        self.rsa = MyRSA(self.__private_k, self.public_k)

    def make_signature(self):
        sha256_hash = hashlib.sha256()
        sha256_hash.update(str(self.message).encode('utf-8'))
        hashed_message = sha256_hash.hexdigest()
        encrypted_hash = self.rsa.encrypt(hashed_message)
        print("encrypted hash: " + str(encrypted_hash))
        return self.message, encrypted_hash, self.public_k

    @staticmethod
    def check_signature(message, encrypted_hash, public_key):
        message_str = str(message)
        rsa_verifier = MyRSA(None, public_key)
        encrypted_hash_in_array = [encrypted_hash]
        decrypted_hash = rsa_verifier.decrypt(encrypted_hash_in_array)
        sha256_hash = hashlib.sha256()
        sha256_hash.update(message_str.encode('utf-8'))
        recalculated_hash = sha256_hash.hexdigest()
        if decrypted_hash == recalculated_hash:
            print("Signature is valid!")
            return 0
        else:
            print("Signature is invalid.")
            return 1

    @staticmethod
    def create_shared_key(current, current_deffi):
        other_dh_public = ""
        other_public_k = ""
        other_encrypted_hash = ""
        current_dh_public = current_deffi.make_public_key()

        current_package = MessageSignaturePackage(current_dh_public)
        current_dh_public, encrypted_hash, public_k = current_package.make_signature()
        bigtext = str(current_dh_public) + "\n" + str(encrypted_hash) + "\n" + str(public_k)
        # print("Big text: " + bigtext)
        # smalltext = bigtext.split("\n")
        # print("Smalltext: ")
        # print(smalltext[0])
        # print(smalltext[1])
        # print(smalltext[2])
        # print("end")

        current.send_message("dh public" + str(current_dh_public))
        time.sleep(2)
        current.send_message("hash" + str(encrypted_hash))
        time.sleep(2)
        current.send_message("k" + str(public_k))
        print("package sent")
        with current.received_messages_condition:  # Lock the condition variable
            while len(current.received_messages) < 3:  # Keep checking until it's not empty
                current.received_messages_condition.wait()

        for message in current.received_messages:
            if "SPLIT" in message:
                pass
            elif "dh public" in message:
                other_dh_public = message.replace("dh public", "")
            elif "hash" in message:
                other_encrypted_hash = message.replace("hash", "").replace("[", "").replace(",", "").replace("]", "")
            elif "k" in message:
                other_public_k = message.replace("k", "")

        shared_secret_key = current_deffi.get_secret_key(int(other_dh_public))
        print("Shared key: " + str(shared_secret_key))
        MessageSignaturePackage.check_signature(int(other_dh_public), int(other_encrypted_hash),
                                                MessageSignaturePackage._convert_key_string_to_tuple(other_public_k))

        des_key = f"{shared_secret_key % (1 << 64):064b}"
        print("the des key: " + str(des_key))
        return des_key

    @staticmethod
    def _convert_key_string_to_tuple(key_string):
        """Convert a string representation of a tuple into an actual tuple."""
        try:
            key_tuple = ast.literal_eval(key_string)
            if isinstance(key_tuple, tuple) and len(key_tuple) == 2:
                return key_tuple
            else:
                raise ValueError("Key string is not a valid tuple format")
        except (ValueError, SyntaxError):
            raise ValueError("Invalid key format; expected a tuple in string form.")

# alice = MyDeffieHellman()
# bob = MyDeffieHellman(alice.p, alice.g)
# # Diffie-Hellman public key exchange
# A = alice.make_public_key()
# B = bob.make_public_key()
#
# # Package the public keys with signatures
# A_package = MessageSignaturePackage(A)
# B_package = MessageSignaturePackage(B)
#
# # Alice and Bob generate their shared secret keys
# secret_key_alice = alice.get_secret_key(B)
# secret_key_bob = bob.get_secret_key(A)
#
# # Sign and verify A's public key
# message, signature, public_key = A_package.make_signature()
# B_package.check_signature(message, signature, public_key)
# print(signature)
# print(type(signature))
# # Sign and verify B's public key
# message_B, signature_B, public_key_B = B_package.make_signature()
# A_package.check_signature(message_B, signature_B, public_key_B)
#
# # Verify that both secret keys match
# if secret_key_alice == secret_key_bob:
#     print("Diffie-Hellman key exchange successful!")
#     shared_secret_key = secret_key_alice
# else:
#     raise ValueError("Diffie-Hellman key exchange failed.")
#
# des_key = f"{shared_secret_key % (1 << 64):064b}"
#
# # Encrypt a message using DES in ECB mode
# plaintext_message = "This is a secret message."
# ecb_cipher = MyECB(des_key)  # Initialize the ECB cipher
# encrypted_message = ecb_cipher.ecb_encrypt(plaintext_message)
# print("Encrypted message:", encrypted_message)
#
# # Decrypt the message to verify correctness
# decrypted_message = ecb_cipher.ecb_decrypt(encrypted_message)
# print("Decrypted message:", decrypted_message)
#
# # Verify that the decrypted message matches the original
# if decrypted_message == plaintext_message:
#     print("Encryption and decryption successful!")
# else:
#     print("Decryption failed. Messages do not match.")
