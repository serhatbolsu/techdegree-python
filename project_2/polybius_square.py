from ciphers import Cipher


class PolybiusSquare(Cipher):
    def __init__(self):
        super().__init__()
        numbers = [(x, y) for y in [1, 2, 3, 4, 5] for x in [1, 2, 3, 4, 5]]
        alphabet = self.get_latin25()  # i/j are combined for simplification
        numbers.sort()
        self._encrpyt_cipher = {k: '{}{}'.format(v[0], v[1]) for k, v in dict(zip(alphabet, numbers)).items()}
        self._decrypt_cipher = {'{}{}'.format(k[0], k[1]): v for k, v in dict(zip(numbers, alphabet)).items()}

    def encrypt(self, data):
        """
        Encrypt message based on Polybius Square ,
        `j` is handled as `i` for simplification
        """
        if type(data) != str:
            raise ValueError("Input must be a sentences")
        data_notj = data.replace('j', 'i')
        encrypted = []
        words = data_notj.split()
        for word in words:
            each_word = []
            for c in word:
                try:
                    each_word.append(self._encrpyt_cipher[c.lower()])
                except:
                    each_word.append(c)
            enc_word = ''.join(each_word)
            encrypted.append(enc_word)
        return ' '.join(encrypted)

    def decrypt(self, data):
        """
        Dencrypt message based on Polybius Square ,
        `j` is handled as `i` for simplification
        """
        if type(data) != str:
            raise ValueError("Input must be a sentences of numbers seperated by space")
        encrypted = []
        words = data.split()
        for word in words:
            each_word = []
            start_slice = 0
            end_slice = 2
            while end_slice <= len(word):
                key = word[start_slice:end_slice]
                each_word.append(self._decrypt_cipher[key])
                start_slice += 2
                end_slice += 2
            enc_word = ''.join(each_word)
            encrypted.append(enc_word)
        return ' '.join(encrypted)


if __name__ == '__main__':
    poly = PolybiusSquare()
    poly.decrypt('1112')
