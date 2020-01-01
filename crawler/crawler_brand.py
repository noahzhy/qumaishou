import sys
# 导入同级目录下其他文件夹下的文件
sys.path.append("./")

import requests
from bs4 import BeautifulSoup

import tools.database_tool as db_tool


domain = 'http://chn.lottedfs.cn'
brand_name = []
brand_url = []

def requests_brand(brand_name, brand_url):
    brand = []
    
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    }

    def requests_special_brand():
        url = 'http://chn.lottedfs.cn/kr/display/brand'
        r = session.get(url=url, headers=headers)
        soup = BeautifulSoup(r.text, "html5lib")
        brandIndexList = soup.find_all('div', id='brandIndexList_GLBL')
        print(brandIndexList[0].select('dl > dd > ul > li > a'))
        [brand.append(i) for i in brandIndexList[0].select('dl > dd > ul > li > a')]
        # print('Special Brand Total:', len(brand))

    def requests_brand_from_A_to_Z():
        url = 'http://chn.lottedfs.cn/kr/display/brand/getBrandMainBrandListAjax?flag=GLBL'
        r = session.get(url=url, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        brandIndexList = soup.find_all('body')
        [brand.append(i) for i in brandIndexList[0].select('dl > dd > ul > li > a')]

    requests_special_brand()
    requests_brand_from_A_to_Z()

    print('Total:', len(brand))
    for i in brand:
        brand_name.append(i.get_text().strip())
        if ('chn.lottedfs.cn' in i['href'].strip()):
            brand_url.append(i['href'].strip())
        else:
            brand_url.append(domain + i['href'].strip())


def main():
    requests_brand(brand_name, brand_url)
    db_tool.db_brand(brand_name, brand_url)
    pass


if __name__ == "__main__":
    main()