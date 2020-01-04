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
    &catNo=&cntPerPage=100
    &curPageNo=1
    &viewType01=0
    &lodfsAdltYn=N
'''

session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
}

def get_brnd_No(dispShopNo):
    url = 'http://eng.lottedfs.com/kr/display/brand?dispShopNo={}'.format(dispShopNo)
    r = session.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "html5lib")
    BrndNo = soup.find_all('input', id='thisBrndNo', type='hidden')
    return str(BrndNo[0]["value"])


def get_product_list(dispShopNo):
    # data = {
    #     'tag': tag,
    #     'product_No': prdNo, 
    #     'brand_name': brand,
    #     'product_name': product.strip(),
    #     'img_url': img_url,
    #     'us_price': us_price
    # }
    df = pd.DataFrame(columns=['tag', 'product_No', 'us_price', 'brand_name', 'product_name', 'img_url'])
    # 通过店铺号来获取品牌号
    brndNo = get_brnd_No(dispShopNo)
    print('Test>>>', brndNo)
    # 默认从第一页开始，使用动态的 page_list 来控制循环
    page_list = [1]
    FLAG_GET_PAGES = False

    for curPage in page_list:
        url = '''http://chn.lottedfs.cn/kr/display/brand/getLrnkBrandPrdListAjax?
            listType=img
            &brndNo={}
            &prdSortStdCd=01
            &cntPerPage=500
            &curPageNo={}
            &viewType01=0
            &lodfsAdltYn=N'''.format(brndNo, curPage).replace('\n', '').replace('\r', '').replace(' ', '')
        # print(url)
        r = session.get(url=url, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        # <div class="paging ">
        if not FLAG_GET_PAGES:
            pages_tag = soup.find_all('div', class_='paging')[0].select('a')[-1]['href']
            pages = int(''.join(list(filter(str.isdigit, pages_tag))))
            print('pages:', pages)
            [page_list.append(i) for i in range(2, pages+1)]
            FLAG_GET_PAGES = True

        productMd = soup.find_all('ul', class_='listUl')

        # <input type="hidden" class="prdNoHidden" value="20000558611">
        for i in productMd[0].select('li', class_='productMd'):

            if (i.find_all('div', class_='flagArea')[0].select('em')):
                tag = i.find_all('div', class_='flagArea')[0].select('em')[0].get_text()
            else:
                tag = ''
            
            prdNo = i.find_all('input', class_='prdNoHidden')[0]['value']
            brand = i.find_all('div', class_='brand')[0].select('strong')[0].get_text()
            product = i.find_all('div', class_='product')[0].get_text()
            img_url = i.find_all('div', class_='img')[0].select('img')[0]['src'].replace('/dims/resize/180x180','')
            us_price = i.find_all('div', class_='price')[0].select('span')[0].get_text()

            data = {
                'tag': tag,
                'product_No': prdNo, 
                'brand_name': brand,
                'product_name': product.strip(),
                'img_url': img_url,
                'us_price': us_price
            }
            df = df.append(data, ignore_index=True)
    
    # print(df.size())
    db_tool.db_product_img(df)


def main():
    print(get_product_list(10004945))


if __name__ == "__main__":
    main()


'''http://chn.lottedfs.cn/kr/display/brand/getLrnkBrandPrdListAjax?
    listType=img
    &brndNo=10073
    &prdSortStdCd=01
    &cntPerPage=500
    &curPageNo=1
    &viewType01=0
    &lodfsAdltYn=N'''