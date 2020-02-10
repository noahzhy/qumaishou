import numpy as np
import json
import sys
# import cv2
from PIL import Image, ImageOps
# 导入同级目录下其他文件夹下的文件
sys.path.append("./")
import tools.img_tools as img_tool


default_dict = eval('{}')

class Color:
    def __init__(self):
        self.black = '#000'
        self.white = '#FFF'
        self.grey = '#949494'
        self.dark_red = '#8B0000'
        self.light_red = '#CD5C5C'
        self.light_orange = ''

    def get_color(self, idx):
        dict_items = self.__dict__
        dictlist = []
        for _, value in dict_items.items():
            temp = [value]
            dictlist.append(temp)
        return dictlist[idx][0]


class Makeup(object):
    def __init__(self):
        pass


class Skincare(object):
    def __init__(self, img_obj, text_obj):
        self.img_obj = img_obj
        self.text_obj = text_obj


class ImgBase(object):
    def __init__(self, obj=default_dict):
        self.size = obj.get('S')
        self.color = obj.get('C')
        self.rotation = obj.get('R')
        self.position = obj.get('P')
        self.border = obj.get('B')

        self.url = ''
        # print(obj)

    def set_url(self, url):
        self.url = url

    def get_url(self):
        return self.url

    def set_size(self, size):
        self.size = size

    def get_size(self):
        return self.size

    def set_color(self, color):
        self.color = Color().get_color(int(color))

    def get_color(self):
        return self.color

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position

    def set_rotation(self, rotation):
        if int(rotation) >= 10:
            self.rotation = '-{}'.format(rotation[-1])
        else:
            self.rotation = rotation

    def get_rotation(self):
        return int(self.rotation)*10 if self.rotation else 0

    def set_border(self, border):
        self.border = int(border)

    def get_border(self):
        return self.border if self.border else 0

    def get_dominant_color(self):
        return '#000' if self.url == '' else img_tool.get_dominant_color(Image.open(self.url))
        

class TextBase:
    def __init__(self, obj=default_dict):
        self.font = obj.get('F')
        self.size = obj.get('S')
        self.color = obj.get('C')
        self.position = obj.get('P')


class ImgText:
    def __init__(self):
        self.layout_map = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

        self.product = ImgBase()
        self.background = ImgBase()
        self.frame = ImgBase()
        self.watermark = ImgBase()

        self.brand = TextBase()
        self.name = TextBase()
        self.usage = TextBase()
        self.effect = TextBase()
        self.review = TextBase()
        self.ingredient = TextBase()

    def set_product(self, obj):
        self.product = obj

    def set_background(self, obj):
        self.background = obj

    def set_frame(self, obj):
        self.frame = obj

    def set_watermark(self, obj):
        self.watermark = obj

    def set_brand(self, obj):
        self.brand = obj

    def set_name(self, obj):
        self.name = obj

    def set_usage(self, obj):
        self.usage = obj

    def set_effect(self, obj):
        self.effect = obj

    def set_review(self, obj):
        self.review = obj

    def set_ingredient(self, obj):
        self.ingredient = obj

    def is_empty(self, key):
        a = int((key-1) / 3)
        b = (key+2) % 3
        x = np.array(self.layout_map)
        if x[a][b] == 0:
            return True
        else:
            return False

        # for i in range(x.shape[0]):
        #     for j in range(x.shape[1]):
        #         print(x[i][j])

    def img_generator(self, img_list, text_list):
        pass


def add_border(input_image, border, color=0):
    # 先剪裁边框宽度，再扩展出边框来
    img = ImageOps.crop(input_image, border=border)
 
    if isinstance(border, int) or isinstance(border, tuple):
        bimg = ImageOps.expand(img, border=border, fill=color)
    else:
        raise RuntimeError('Border is not an integer or tuple!')
 
    return bimg


if __name__ == "__main__":
    # print(ImgText().is_empty(1))
    img_text = ImgText()
    img_text.background.set_url('img_fusion/img_for_test/background.jpg')
    img_text.product.set_url('img_fusion/img_for_test/product_01.png')
    img_text.product.set_rotation('12')
    img_text.frame.set_border('40')
    # img_text.frame.set_color('02')
    
    # testing

    bg = Image.open(img_text.background.get_url())
    prod = Image.open(img_text.product.get_url())
    prod = prod.resize((500, 500))
    prod = prod.rotate(img_text.product.get_rotation())
    layer = Image.new('RGBA', bg.size, (0,0,0,0))
    layer.paste(
        prod,
        (int((bg.size[0]-prod.size[0])/2),
        int((bg.size[1]-prod.size[1])/2))
    )
    out = Image.composite(layer, bg, layer)
    # out = add_border(out, img_text.frame.get_border(), img_text.frame.get_color())
    out = add_border(out, img_text.frame.get_border(), img_text.product.get_dominant_color())

    # out = add_border(out, 50, '#FFD700')
    # quality: 保存图像的质量，值的范围从1（最差）到95（最佳）
    # 默认值为75，使用中应尽量避免高于95的值; 
    # 100会禁用部分JPEG压缩算法，并导致大文件图像质量几乎没有任何增益
    out.save('result.jpg', quality=95)
    # out.show()

    print(img_text.product.get_dominant_color())

 
 


