def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False

if __name__ == "__main__":
    print(is_chinese('登录后可查看折扣价'))
    print(is_chinese('$306'))
    pass