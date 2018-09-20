from ciphers import Cipher


class Alberti(Cipher):
    def __init__(self, AEaualInner='g'):
        super().__init__()
        outer = list('ABCDEFGILMNOPQRSTVXZ1234')
        if AEaualInner != 'g':
            _partition_inner = 'gklnprtuz&xysomqihfdbace'.partition(AEaualInner)
            inner = ''.join(_partition_inner[1] + _partition_inner[2] + _partition_inner[0])

        else:
            inner = list('gklnprtuz&xysomqihfdbace')
        self.cipher = dict(zip(outer, inner))

    def encrypt(self, data):
        if type(data) is not str:
            raise ValueError('Input must be string text')

        encrypted = []
        for word in data.split():
            each_word = []
            for l in word.upper():
                try:
                    each_word.append(self.cipher[l])
                except KeyError:
                    each_word.append(l)
            encrypted.append(''.join(each_word))
        return ' '.join(encrypted)

    def decrypt(self, data):
        if type(data) is not str:
            raise ValueError('Input must be string text')

        encrypted = []
        for word in data.split():
            each_word = []
            for l in word.upper():
                try:
                    each_word.append(self.cipher[l])
                except KeyError:
                    each_word.append(l)
            encrypted.append(''.join(each_word))
        return ' '.join(encrypted)


if __name__ == '__main__':
    alb = Alberti('c')
    result = alb.encrypt('serhat bolsu')
    print("Encrypt : " + result)
    de = alb.decrypt(result)
    print("Decrypt : " + de)
