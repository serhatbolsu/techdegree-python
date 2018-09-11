import random
import re
import numpy as np

from ciphers import Cipher


class Transposition(Cipher):
    def __init__(self, key=None):

        """
        Transposition class implemented as a 'Columnar transposition'
        'key' must be supplied and same key should be used both ways of encryption
        """
        super().__init__()
        if key is None and type(key) is not str:
            raise ValueError("'key' should be provided for Transposition cipher and should be string")
        self.key = key.lower()
        key_formation = self.text_to_alphabet_position_list(key)
        self.permutation = np.argsort(key_formation)
        # current_big = -1
        # for i in range(len(self.key)):
        #     current_min = min(filter(lambda x: x > current_big, key_formation))
        #     current_big = current_min
        #     self.permutation[key_formation.index(current_min)] = i
        #     key_formation[key_formation.index(current_min)] = 100

    def find_filler(self, data, sub_lenght):
        if sub_lenght > 0:
            return (''.join([
                random.choice(self.get_alphabet()) for _ in range(len(self.key)- len(data)%sub_lenght)
            ])).upper()
        else:
            return ''

    def encrypt(self, data):
        data_filtered = ''.join(list(filter(re.compile('[a-zA-Z]').match, list(data))))
        data_with_filler = data_filtered + self.find_filler(data_filtered, len(self.key))
        data_2d = [list(data_with_filler[i:i + len(self.key)]) for i in range(0, len(data_with_filler), len(self.key))]
        pre_array = np.array(data_2d)
        order = np.argsort(self.permutation)
        data_array_c = pre_array[:, order]
        data_array_final = data_array_c.T
        return  ''.join([char for word in data_array_final for char in word])

    def decrypt(self, data):
        data_filtered = ''.join(list(filter(re.compile('[a-zA-Z]').match, list(data))))
        vertical_lenght = len(data_filtered) // len(self.permutation)
        data_with_filler = data_filtered + self.find_filler(data_filtered, len(data_filtered)% vertical_lenght)
        data_2d = [list(
            data_with_filler[i:i + vertical_lenght]) for i in range(0, len(data_filtered), vertical_lenght)
        ]
        pre_array = np.array(data_2d)
        data_array_t = pre_array.T
        data_array_final = data_array_t[:, self.permutation]
        return  ''.join([char for word in data_array_final for char in word])


if __name__ == '__main__':
    trans = Transposition('XMLCK')
    print("message: " +  'WE ARE DISCOVERED FLEE AT ONCE')
    enc = trans.encrypt('WE ARE DISCOVERED FLEE AT ONCE')
    print(enc)
    print(trans.decrypt(enc))