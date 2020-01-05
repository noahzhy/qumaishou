import re

def is_chinese(string):
    """判断一个unicode是否是汉字"""
    string = only_chinese(string)
    if string >= u'\u4e00' and string <= u'\u9fa5':
        return True
    else:
        return False


# def only_eng_and_num(string):
#     new_string = filter(str.isalnum, string)
#     return (''.join(list(new_string)))


def only_chinese(string):
    r1 = '[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
    return re.sub(r1, '', string).strip()


def only_num(string):
    return int(''.join(list(filter(str.isdigit, string))))


if __name__ == "__main__":
    s1 = '72CPB2911-50L-FREE [FW_BEANIE] F-BASIC LOGO BASIC BEANIE NEW YORK YANKEES 帽子'
    print(is_chinese('sdsds登录后可查看折扣价'), is_chinese('$306'))
    # print(only_eng_and_num(s1))
    print(only_chinese(s1))
    pass