class Color:
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
    def __init__(self, obj):
        self.url = '02'
        self.S = '01'
        self.C = Color()
        self.P = '05'
        # pass

    def set_url(self, url):
        self.url = url

    def set_size(self, size):
        self.size = size

    def set_color(self, color):
        self.color = color

    def set_position(self, position):
        self.position = position

    def get_url(self):
        return self.url

    def get_size(self):
        return self.size

    def get_color(self):
        return self.color

    def get_position(self):
        return self.position

    _url = property(get_url, set_url)
    S = property(get_size, set_size)
    C = property(get_color, set_color)
    P = property(get_position, set_position)


class TextBase:
    def __init__(self, font, size, color, position):
        self.font = font
        self.size = size
        self.color = color
        self.position = position


class ImgText:
    def __init__(self, obj):
        self.product = [obj.P if hasattr(obj, 'P') else ImgBase()]
        self.ground = [obj.G if hasattr(obj, 'G') else ImgBase()]
        self.frame = [obj.F if hasattr(obj, 'F') else ImgBase()]
        self.watermark = [obj.W if hasattr(obj, 'W') else ImgBase()]

        self.brand = [obj.B if hasattr(obj, 'B') else TextBase()]
        self.name = [obj.N if hasattr(obj, 'N') else TextBase()]
        self.usage = [obj.U if hasattr(obj, 'U') else TextBase()]
        self.effect = [obj.E if hasattr(obj, 'E') else TextBase()]
        self.review = [obj.R if hasattr(obj, 'R') else TextBase()]
        self.ingredient = [obj.I if hasattr(obj, 'I') else TextBase()]

    def img_generator(self, img_list, text_list):
        for img in img_list:
            pass
        
        for text in text_list:
            pass


    # P = property(set_P)



if __name__ == "__main__":
    pass