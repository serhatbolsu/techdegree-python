from unit_2.alberti import Alberti
from unit_2.atbash import Atbash
from unit_2.polybius_square import PolybiusSquare
from unit_2.transposition import Transposition



def main():
    print("Welcome to encryption/decrpytion program.")
    print()
    name = str(input("Please enter your name: "))
    print("Hi {},".format(name.capitalize()))
    encryption = {'Alberti': Alberti, 'Atbash': Atbash, 'Polybius': PolybiusSquare,
                   'Transposition': Transposition}

    game = True
    while game:
        picked = str(input("Please pick one of the ciphers: \n-{} \n"
                           .format('\n-'.join(key for key in encryption.keys())))).capitalize()

        if picked not in encryption.keys():
            continue
        # Special cases
        if picked == 'Alberti':
            start_letter = str(input("Please Enter Albert inner allignment letter: "))
            cipher = Alberti(start_letter)
        elif picked == 'Transposition':
            secret_word = str(input("Please Enter Secret word (ex. ZEBRAS): "))
            cipher = Transposition(key=secret_word)
        else:
            cipher = encryption[picked]()
        method = str(input("Do you want to encrpyt (en) or decrpyt (de)? ")).lower()
        if method == 'en':
            try:
                text = str(input("What is your text for encryption: \n"))
                print(cipher.decrypt(text))
                # pad = str(input("Please enter the pad number (ex. XMCKL): "))
                # text_pad = cipher.one_time_pad(text, pad, method='encrypt')
                # print(cipher.encrypt(text_pad))
            except TypeError:
                raise ValueError("Input must be text")
        elif method == 'de':
            try:
                text = str(input("What is your text for decryption: \n"))
                print(cipher.decrypt(text))
                # pad = str(input("Please enter the pad number (ex.XMCKL): "))
                # text_pad = cipher.one_time_pad(text, pad, method='decrypt')
                # print(cipher.decrypt(text_pad))
            except TypeError:
                raise ValueError("Input must be text")
        print()
        cont = str(input("Do you want to continue (yes/no) : "))
        if not cont.lower() == 'yes':
            game = False





if __name__ == '__main__': main()
