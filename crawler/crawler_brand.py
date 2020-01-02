import sys
# 导入同级目录下其他文件夹下的文件
sys.path.append("./")

import requests
from bs4 import BeautifulSoup

import tools.database_tool as db_tool


def get_all_brand():
    brand, brand_name, brand_url = [], [], []
    domain = 'http://chn.lottedfs.cn'

    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    }

    def get_special_brand():
        url = 'http://chn.lottedfs.cn/kr/display/brand'
        r = session.get(url=url, headers=headers)
        soup = BeautifulSoup(r.text, "html5lib")
        brandIndexList = soup.find_all('div', id='brandIndexList_GLBL')
        return brandIndexList[0].select('dl > dd > ul > li > a')
        # print('Special Brand Total:', len(brand))

    def get_brand_from_A_to_Z(flag='CATE'):
        # flag=GLBL 表示按照拼音序列，flag=ENG 表示按照英文排序，flag=CATE 表示按照类别排列
        url = 'http://chn.lottedfs.cn/kr/display/brand/getBrandMainBrandListAjax?flag={}'.format(flag)
        r = session.get(url=url, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        brandIndexList = soup.find_all('body')
        return brandIndexList[0].select('dl > dd > ul > li > a')

    brand = get_special_brand() + get_brand_from_A_to_Z()
    # include repetition
    # print('Total:', len(brand))
    for i in brand:
        brand_name.append(i.get_text().strip())
        if ('chn.lottedfs.cn' in i['href'].strip()):
            brand_url.append(i['href'].strip())
        else:
            brand_url.append(domain + i['href'].strip())

    return brand_name, brand_url


def main():
    brand_name, brand_url = get_all_brand()
    db_tool.db_brand(brand_name, brand_url)
    pass


if __name__ == "__main__":
    main()