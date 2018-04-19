
class Encrypter:

    def __init__(self, key_enc, key_mac):
        self.key_enc = key_enc
        self.key_mac = key_mac

    def encrypt(self, plaintext):
        return plaintext

    def decrypt(self, ciphertext):
        return ciphertext
