from ciphers import Cipher


class Atbash(Cipher):
    def __init__(self):
        super().__init__()
        self.cipher = dict(zip(self.get_alphabet(), self.get_reserve_alphabet()))

    def crypt(self ,string):
        encrypted = []
        for char in string:
            try:
                encrypted.append(self.cipher[char.lower()])
            except:
                encrypted.append(char)
        return ''.join(encrypted)

    def encrypt(self, data):
        return self.crypt(data)

    def decrypt(self, data):
        return self.crypt(data)
