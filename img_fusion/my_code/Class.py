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


class ImgBase:
    def __init__(self):
        self.url = ''
        self.size = ''
        self.color = Color()
        self.position = ''
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
    _size = property(get_size, set_size)
    _color = property(get_color, set_color)
    _position = property(get_position, set_position)


class TextBase:
    def __init__(self, font, size, color, position):
        self.font = font
        self.size = size
        self.color = color
        self.position = position


class ImgText:
    def __init__(self, magic_key):
        self.magic_key = magic_key
        self.obj_class = obj_class
        self.obj_main = obj_main

    def img_generator(self, img_list, text_list):
        for img in img_list:
            pass
        
        for text in text_list:
            pass

    def funcname(parameter_list):
        pass


if __name__ == "__main__":
    pass