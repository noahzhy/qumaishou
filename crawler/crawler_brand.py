import sys
# 导入同级目录下其他文件夹下的文件
sys.path.append("./")

import requests
from bs4 import BeautifulSoup
from requests.sessions import session

import tools.database_tool as db_tool
import pandas as pd


def get_all_brand(flag='ENG', a_to_z_flag='CATE'):
    brand, brand_no, brand_name, brand_url = [], [], [], []
    http = 'http://'

    if (flag == 'CHN'):
        domain = 'chn.lottedfs.cn'
        db_name = 'db_brand_chn'
    elif (flag == 'ENG'):
        domain = 'eng.lottedfs.com'
        db_name = 'db_brand_eng'
    else:
        domain = 'eng.lottedfs.com'
        db_name = 'db_brand_eng'

    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    }

    def get_special_brand():
        url = 'http://{}/kr/display/brand'.format(domain)
        r = session.get(url=url, headers=headers)
        soup = BeautifulSoup(r.text, "html5lib")
        # for english version
        brandIndexList = soup.find_all('div', id='brandIndexList_{}'.format(a_to_z_flag))
        # brandIndexList = soup.find_all('div', id='brandIndexList_GLBL')
        return brandIndexList[0].select('dl > dd > ul > li > a')
        # print('Special Brand Total:', len(brand))

    def get_brand_from_A_to_Z(flag=a_to_z_flag):
        # flag=GLBL 表示按照拼音序列，flag=ENG 表示按照英文排序，flag=CATE 表示按照类别排列
        url = 'http://{}/kr/display/brand/getBrandMainBrandListAjax?flag={}'.format(domain, flag)
        r = session.get(url=url, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        brandIndexList = soup.find_all('body')
        return brandIndexList[0].select('dl > dd > ul > li > a')

    brand = get_special_brand() + get_brand_from_A_to_Z()
    # include repetition
    # print('Total:', len(brand))
    for i in brand:
        brand_name.append(i.get_text().strip())
        if (domain in i['href'].strip()):
            brand_url.append(i['href'].strip())
        else:
            brand_url.append(http + domain + i['href'].strip())
        brand_no.append(i['href'].strip().split('=')[-1])

    df = pd.DataFrame({
        # 'index': indexList,
        'dispShopNo': brand_no,
        'brand_name': brand_name,
        'brand_url': brand_url
    })
    db_tool.db_save('db_brand_{}'.format(flag.lower()), df)
    return df


def main():
    # 中文拼音排序 品牌 数据库
    # 英文类别 品牌 数据库（常用）
    get_all_brand('CHN', 'CATE')
    get_all_brand()
    pass


if __name__ == "__main__":
    main()