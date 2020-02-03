class Color:
    # def __init__(self):
    #     pass

    black = ''
    white = ''
    dark_red = '#8B0000'
    light_red = ''
    light_orange = ''


class Makeup(object):
    def __init__(self):
        pass


class Skincare(object):
    def __init__(self, img_obj, text_obj):
        self.img_obj = img_obj
        self.text_obj = text_obj


class ImgBase(object):
    def __init__(self, url='', size='', color='', position=''):
        self.url = url
        self.size = size
        self.color = color
        self.position = position

    def set_url(self, url):
        self.url = url

    def set_size(self, size):
        self.size = size

    def set_color(self, color):
        self.color = color

    def set_position(self, position):
        self.position = position

    def get_url(self):
        return self._url

    def get_size(self):
        return self.S

    def get_color(self):
        return self.C

    def get_position(self):
        return self.P

    # _url = property(get_url, set_url)
    # S = property(get_size, set_size)
    # C = property(get_color, set_color)
    # P = property(get_position, set_position)


class TextBase:
    def __init__(self, obj=''):
        self.font = [obj.S if hasattr(obj, 'F') else '']
        self.size = [obj.S if hasattr(obj, 'S') else '']
        self.color = [obj.S if hasattr(obj, 'C') else '']
        self.position = [obj.S if hasattr(obj, 'P') else '']


class ImgText:
    def __init__(self, obj):
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

    def img_generator(self, img_list, text_list):
        for img in img_list:
            pass
        
        for text in text_list:
            pass


    # P = property(set_P)



if __name__ == "__main__":
    pass