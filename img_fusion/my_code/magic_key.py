import os
import random
import Class

key = 'SC00-PC00GR00PR00WK00BF00NC00UC00-0000'

def magic_key_generator(rule):
    pass


def magic_key_parsing(magic_key):
    key_code = []
    img_code = list('PGWF')
    key_list = key.split('-')
    print(img_code)

    for i in range(0, len(key_list[1]), 4):
        key_code.append(key_list[1][i:i+4])

    key_code.sort()

    for code in key_code:
        if code[0] == 'P':
            pruduct_obj = Class.ImgBase()
            if code[1] == 'P':
                pruduct_obj._position = code[2:]
            if code[1] == 'S':
                pruduct_obj._size = code[2:]
            if code[1] == 'C':
                print(Class.Color.dark_red)
                pruduct_obj._color = Class.Color.dark_red
        
        if code[1] == 'G':
            background_obj = Class.ImgBase()
            if code[1] == 'P':
                background_obj._position = code[2:]
            if code[1] == 'S':
                background_obj._size = code[2:]
            if code[1] == 'C':
                background_obj._color = Class.Color.dark_red            

        


if __name__ == "__main__":
    magic_key_parsing(key)
