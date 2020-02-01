class Color:
    red = ''
    black = ''
    white = ''
    light_red = ''
    light_orange = ''


class Makeup:
    def __init__(self):
        pass


class Skincare:
    def __init__(self):
        pass

    def set_text(self, brand_name, produce_name, ):
        pass


class ImgBase:
    def __init__(self, url, size, color, position):
        self.url = url
        self.size = size
        self.color = color
        self.position = position


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