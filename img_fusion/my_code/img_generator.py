import Class
import magic_key as mk


key = 'SC00-PC00FS03PR45GR04PP03WK00BF00NC00UC00-0000'

def img_generator(key):
    img_text = Class.ImgText()

    d = mk.magic_key_parsing(key)
    print(d)

    if d.get('P'): img_text.set_product = Class.ImgBase(d.get('P'))
    if d.get('G'): img_text.set_background = Class.ImgBase(d.get('G'))
    if d.get('F'): img_text.frame = Class.ImgBase(d.get('F'))
    if d.get('W'): img_text.watermark = Class.ImgBase(d.get('W'))

    if d.get('B'): img_text.brand = Class.TextBase(d.get('B'))
    if d.get('N'): img_text.name = Class.TextBase(d.get('N'))
    if d.get('U'): img_text.usage = Class.TextBase(d.get('U'))
    if d.get('E'): img_text.effect = Class.TextBase(d.get('E'))
    if d.get('R'): img_text.review = Class.TextBase(d.get('R'))
    if d.get('I'): img_text.ingredient = Class.TextBase(d.get('I'))
    # print(d.get('P').get('U'))


if __name__ == "__main__":
    img_generator(key)
