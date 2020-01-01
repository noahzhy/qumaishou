import sys
# 导入同级目录下其他文件夹下的文件
sys.path.append("./")

import requests
from bs4 import BeautifulSoup

import tools.database_tool as db_tool


domain = 'http://chn.lottedfs.cn'
brand_name = []
brand_url = []

def requests_special_brand():
    session = requests.Session()
    url = 'http://chn.lottedfs.cn/kr/display/brand'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    }
    r = session.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "html5lib")
    brandIndexList = soup.find_all('div', id='brandIndexList_GLBL')
    brand = brandIndexList[0].select('dl > dd > ul > li > a')
    print('Special Brand Total:', len(brand))

    for i in brand:
        brand_name.append(i.get_text().strip())
        if ('chn.lottedfs.cn' in i['href'].strip()):
            brand_url.append(i['href'].strip())
        else:
            brand_url.append(domain + i['href'].strip())


def requests_brand_from_A_to_Z():
    session = requests.Session()
    url = 'http://chn.lottedfs.cn/kr/display/brand/getBrandMainBrandListAjax?flag=GLBL'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    }
    r = session.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    brandIndexList = soup.find_all('body')
    brand = brandIndexList[0].select('dl > dd > ul > li > a')
    print('Brand from A to Z Total:', len(brand))

    for i in brand:
        brand_name.append(i.get_text().strip())
        if ('chn.lottedfs.cn' in i['href'].strip()):
            brand_url.append(i['href'].strip())
        else:
            brand_url.append(domain + i['href'].strip())


def main():
    requests_special_brand()
    requests_brand_from_A_to_Z()
    db_tool.db_brand(brand_name, brand_url)
    pass


if __name__ == "__main__":
    main()