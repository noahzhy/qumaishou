class Color:
    def __init__(self):
        self.black = ''
        self.white = ''
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


if __name__ == "__main__":
    c = Color()

    print(c.get_color(3))