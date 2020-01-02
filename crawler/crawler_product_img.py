import sys
# 导入同级目录下其他文件夹下的文件
sys.path.append("./")
import requests
import pandas as pd
import os
from bs4 import BeautifulSoup

import tools.database_tool as db_tool


'''http://chn.lottedfs.cn/kr/display/brand/getLrnkBrandPrdListAjax?
    listType=img
    &dispShopNo=10000863
    &brndNo=19207 //重要的是这个 <input type="hidden" id="thisBrndNo" value="1001495"/>
    &prdSortStdCd=01
    &catNo=&cntPerPage=50
    &curPageNo=1
    &viewType01=0
    &lodfsAdltYn=N
'''

session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
}

def get_brnd_No(dispShopNo):
    url = 'http://chn.lottedfs.cn/kr/display/brand?dispShopNo={}'.format(dispShopNo)
    r = session.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "html5lib")
    BrndNo = soup.find_all('input', id='thisBrndNo', type='hidden')
    return str(BrndNo[0]["value"])


def get_product_list(dispShopNo):
    df = pd.DataFrame(columns=['product_No', 'brand_name', 'product_name', 'img_url', 'us_price'])
    brndNo = get_brnd_No(dispShopNo)
    # print(brndNo)

    def get_page_total():
        return 1

    curPage = get_page_total()

    url = '''http://chn.lottedfs.cn/kr/display/brand/getLrnkBrandPrdListAjax?
        listType=img
        &brndNo={}
        &prdSortStdCd=01
        &cntPerPage=50
        &curPageNo={}
        &viewType01=0
        &lodfsAdltYn=N'''.format(brndNo, curPage).replace('\n', '').replace('\r', '').replace(' ', '')
    # print(url)
    r = session.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    # print(r.text)
    # <div class="paging ">
    productMd = soup.find_all('ul', class_='listUl')
    # <input type="hidden" class="prdNoHidden" value="20000558611">
    for i in productMd[0].select('li', class_='productMd'):
        prdNo = i.find_all('input', class_='prdNoHidden')[0]['value']
        # print(prdNo)
        brand = i.find_all('div', class_='brand')[0].select('strong')[0].get_text()
        # print(brand)
        product = i.find_all('div', class_='product')[0].get_text()
        # print(product)
        img_url = i.find_all('div', class_='img')[0].select('img')[0]['src'].replace('/dims/resize/180x180','')
        # print(img_url)
        us_price = i.find_all('div', class_='discount')[0].select('strong')[0].get_text()
        # print(us_price)

        data = {
            'product_No': prdNo, 
            'brand_name': brand,
            'product_name': product,
            'img_url': img_url,
            'us_price': us_price
        }
        df = df.append(data, ignore_index=True)
    
    # print(df.size())
    db_tool.db_product_img(df)

    # return productMd[0].select('dl > dd > ul > li > a')





def main():
    print(get_product_list(10008476))


if __name__ == "__main__":
    main()