
from Crypto.Cipher import AES


class Encrypter:

    def __init__(self, key_enc, key_mac):
        self.key_enc = key_enc
        self.key_mac = key_mac


    def encrypt(self, plaintext):

        # plaintext = pad(plaintext, AES.block_size)

        # cipher = AES.new(key, AES.MODE_CFB, iv)
        # cipher.encrypt(plaintext)

        return plaintext

    def decrypt(self, ciphertext):
        return ciphertext


def pad(input, block_size):
    input += '1'
    length = len(input)
    mod = length % block_size
    if mod != 0:
        input += '0'*(block_size-mod)
    return inputs

def unpad(input):
    while input[-1] != '1':
        input = input[:-1]
    return input
