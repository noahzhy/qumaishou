import os
import sys
import random
# 导入同级目录下其他文件夹下的文件
sys.path.append("./")

import pandas as pd
import requests
from bs4 import BeautifulSoup
from pypinyin import lazy_pinyin
from fake_useragent import UserAgent

import tools.data_check as data_check
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

ua = UserAgent()

def get_product_detail(dispShopNo, proxies):
    session = requests.Session()
    headers = {'User-Agent': ua.random}
    url = 'http://eng.lottedfs.com/kr/display/brand?dispShopNo={}'.format(dispShopNo)
    print(url)
    r = session.get(url=url, headers=headers, proxies=proxies, timeout=5)
    soup = BeautifulSoup(r.text, "html5lib")
    BrndNo = soup.find_all('input', id='thisBrndNo', type='hidden')
    # brdWrap = soup.find_all('div', class_='brdWrap')
    # print(brdWrap)
    try:
        df = pd.DataFrame(columns=['tag', 'brand_No', 'product_No', 'us_price', 'brand_name_chn', 'brand_name_eng', 'product_name', 'img_url'])
        # 通过店铺号来获取品牌号
        brndNo = BrndNo[0]['value']
        print('brndNo:', brndNo)
        # 默认从第一页开始，使用动态的 page_list 来控制循环
        page_list = [1]
        FLAG_GET_PAGES = False

        for curPage in page_list:
            url = '''http://chn.lottedfs.cn/kr/display/brand/getLrnkBrandPrdListAjax?
                listType=img
                &brndNo={}
                &prdSortStdCd=01
                &catNo=
                &cntPerPage=500
                &curPageNo={}
                &viewType01=1
                &lodfsAdltYn=N'''.format(brndNo, curPage).replace('\n', '').replace('\r', '').replace(' ', '')
            # print(url)
            r = session.get(url=url, headers=headers, proxies=proxies, timeout=20)
            soup = BeautifulSoup(r.text, "lxml")
            # <div class="paging ">
            if not FLAG_GET_PAGES:
                pages_tag = soup.find_all('div', class_='paging')[0].select('a')[-1]['href']
                pages = data_check.only_num(pages_tag)
                print('pages:', pages)
                [page_list.append(i) for i in range(2, pages+1)]
                FLAG_GET_PAGES = True
                # print('DEBUG_01')

            productMd = soup.find_all('ul', class_='listUl')
            # <input type="hidden" class="prdNoHidden" value="20000558611">
            for i in productMd[0].select('li', class_='productMd'):
                # print('DEBUG_02')
                list_flag = i.find_all('div', class_='flagArea')[0].select('em')
                # print('DEBUG_03')
                prdNo, _tag, us_price, brand_chn, brand_eng, product, img_url = '', '', '', '', '', '', ''
                if (list_flag):
                    for num in range(len(list_flag)):
                        # 忽略 3小时前 这个标签
                        if not (list_flag[num].get_text() == '3小时前'):
                            _tag = _tag + (list_flag[num].get_text()+' ')
                
                if (len(_tag)>0):
                    # 按拼音排序
                    sorted_list = _tag.strip().split()
                    sorted_list.sort(key=lambda char: lazy_pinyin(char)[0][0])
                    tag_sort = ' '.join(sorted_list)
                else:
                    tag_sort = ''

                # print('DEBUG_04')
                prdNo = i.find_all('input', class_='prdNoHidden')[0]['value']
                brand_chn = i.find_all('div', class_='brand')[0].select('strong')[0].get_text()
                brand_eng = i.find_all('div', class_='brand')[0].contents[-1].strip()
                product = i.find_all('div', class_='product')[0].get_text()
                # print('DEBUG_05')
                img_url = i.find_all('div', class_='img')[0].select('img')[0]['src'].replace('/dims/resize/180x180','')
                try:
                    us_price = i.find_all('div', class_='price')[0].select('span')[0].get_text()
                except Exception as e:
                    us_price = i.find_all('div', class_='discount')[0].select('strong')[0].get_text()
                

                if data_check.is_chinese(us_price):
                    us_price = i.find_all('div', class_='discount')[0].select('strong')[0].get_text()

                data = {
                    'tag': tag_sort.strip(),
                    'brand_No': brndNo,
                    'product_No': prdNo,
                    'brand_name_chn': brand_chn,
                    'brand_name_eng': brand_eng,                
                    'product_name': product.strip(),
                    'img_url': img_url,
                    'us_price': us_price
                }
                df = df.append(data, ignore_index=True)
        
        # print(df.size())
        db_tool.db_brand_product(dispShopNo, df)
        return True, df.shape[0], brndNo

    except Exception as e:
        print(e)
        return False, 0, 0

def main():
    # 输入英文品牌数据库的品牌编号
    print(get_product_detail(10020359, proxies={}))


if __name__ == "__main__":
    main()


'''
    http://chn.lottedfs.cn/kr/display/brand/brandGwanPrdList?
    returnFilePath=display%2Fcommon%2Fbrand%2FesteeLauder%2Ffragments%2F
    &returnFileName=esteeLauderPrdList
    &thisDispShopNo=10006056
    &prdSortStdCd=01
    &cntPerPage=15
    &curPageNo=1
'''

'''
    returnFilePath: display/common/brand/joMalone/fragments/
    returnFileName: joMalonePrdList
    thisDispShopNo: 10018131
    prdSortStdCd: 01
    cntPerPage: 9
    curPageNo: 1
'''

'''
    returnFilePath: display/common/brand/esteeLauder/fragments/
    returnFileName: esteeLauderPrdList
    thisDispShopNo: 10021874
    prdSortStdCd: 01
    cntPerPage: 15
    curPageNo: 1
'''

'''
    returnFilePath: display/common/brand/mac/fragments/
    returnFileName: macPrdListArea_new
    thisDispShopNo: 10021104
    prdSortStdCd: 01
    cntPerPage: 12
    curPageNo: 1
'''

'''
    香奈儿 特殊规则
    http://chn.lottedfs.cn/kr/display/brand/brandGwanPrdList?
        returnFilePath=display%2Fcommon%2Fbrand%2Fchanel%2Ffragments%2F
        &returnFileName=chanelPrdList
        &thisDispShopNo=1230790 // 重点
        &prdSortStdCd=01
        &cntPerPage=20
        &curPageNo=1
    http://chn.lottedfs.cn/kr/display/brand/brandGwanPrdList?
        returnFilePath=display%2Fcommon%2Fbrand%2Fchanel%2Ffragments%2F
        &returnFileName=chanelPrdList
        &thisDispShopNo=1230837 // 重点
        &prdSortStdCd=01
        &cntPerPage=20
        &curPageNo=1
'''