import magic_key as mk


key = 'SC00-PC00PR45GR04PP03WK00BF00NC00UC00-0000'

def img_generator(key):
    j = mk.magic_key_parsing(key)
    print(j.get('P').get('U'))


if __name__ == "__main__":
    img_generator(key)
