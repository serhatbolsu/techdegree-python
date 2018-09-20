import operator
import re


class Alphabet:
    def __init__(self, alphabet_type='latin'):
        if alphabet_type == 'latin':
            self.__alphabet = 'abcdefghijklmnopqrstuvwxyz'
            self.__type = 'latin'
        else:
            pass  # TODO: add other required alphabets

    def set_alphabet(self, alphabet):
        if type(alphabet) is str:
            self.__alphabet = alphabet
        else:
            raise ValueError("Alphabet must be a string list of letters and characters")

    def text_to_alphabet_position_list(self, text):
        """
        Converts text to list of positions where is position represents the index of letter in supplied
        alphabet if not supplied 'latin'-26 is used
        :return:
        """
        return list([self.get_alphabet().index(letter) for letter in list(text.lower())])

    def alphabet_position_list_to_text(self, position_list):
        return list([self.__alphabet[position] for position in position_list])

    def get_alphabet(self):
        return list(self.__alphabet)

    def get_latin25(self):
        if self.__type != 'latin':
            raise ValueError('Current alphabet is not latin, this method is only for latin alphabet')
        else:
            return list(self.__alphabet.replace('j', ''))[::-1]

    def get_reserve_alphabet(self):
        return list(self.__alphabet)[::-1]


class Cipher(Alphabet):
    def encrypt(self, *args):
        raise NotImplementedError()

    def decrypt(self, *args):
        raise NotImplementedError()

    def one_time_pad(self, text, key, method='encrypt'):
        if type(key) is int:
            key_indexes = [int(l) for l in str(key)]
        else:
            key_indexes = self.text_to_alphabet_position_list(key)
        op_func = operator.add
        if method.lower() == 'decrypt':
            op_func = operator.sub
        text_filtered = ''.join(list(
            filter(re.compile('[a-zA-Z]').match, list(text))
        ))
        message_partitioned = [list(text_filtered[i: i + len(key_indexes)]) for i in range(0, len(text_filtered),
                                                                                           len(key_indexes))
                               ]
        message_final = []
        for part in message_partitioned:
            part_indexes = self.text_to_alphabet_position_list(''.join(part))
            encrypted_word = list(
                map(lambda x: op_func(x[0], x[1]) % len(self.get_alphabet()), list(zip(part_indexes, key_indexes)))
            )
            message_final.append(''.join(self.alphabet_position_list_to_text(encrypted_word)).upper())
        return ''.join(message_final)


if __name__ == '__main__':
    cipher = Cipher()
    encrypted = cipher.one_time_pad('WEAREDISCOVEREDFLEENOW', 'XMCKL', method='encrypt')
    print("Encrypted message : \n{}".format(encrypted))
    decrypted = cipher.one_time_pad(encrypted, 'XMCKL', method='decrypt')
    print("Decrypted message : \n{}".format(decrypted))
