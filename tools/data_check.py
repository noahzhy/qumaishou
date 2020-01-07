import re
import os
import sys
import pandas as pd
# 导入同级目录下其他文件夹下的文件
sys.path.append("./")

import crawler.crawler_product_detail as cpd
import crawler.crawler_proxies as proxies_api
import tools.data_check as data_check
import tools.database_tool as db_tool
import time


def is_chinese(string):
    """判断一个unicode是否是汉字"""
    string = only_chinese(string)
    if string >= u'\u4e00' and string <= u'\u9fa5':
        return True
    else:
        return False


def only_chinese(string):
    r1 = '[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
    return re.sub(r1, '', string).strip()


def only_num(string):
    return int(''.join(list(filter(str.isdigit, string))))




# proxies = {'http': proxies_api.get_proxies()}
csv_file='database/db_brand_final.csv'
df = pd.read_csv(csv_file)
result_df = pd.read_csv('database/db_brand_list_check.csv')


def get_product_info(row=0):

    dispShopNo = df.loc[row]['dispShopNo']

    if not (os.path.exists('database/brand_product_{}.csv'.format(dispShopNo))):
        # has_existed_df = pd.read_csv('database/brand_product_{}.csv'.format(dispShopNo))
        # brand_name = df.loc[row]['brand_name_eng']
        brndNo = df.loc[row]['brand_name']
        print(dispShopNo, brndNo, 'brand_name')
        # return True
        # continue


if __name__ == "__main__":
    s1 = '72CPB2911-50L-FREE [FW_BEANIE] F-BASIC LOGO BASIC BEANIE NEW YORK YANKEES 帽子'
    # print(is_chinese('sdsds登录后可查看折扣价'), is_chinese('$306'))
    # print(only_chinese(s1))
    rows = []
    csv_file = 'database/db_brand_list_check.csv'
    df = pd.read_csv(csv_file)

    for i in range(0, df.shape[0]):
        get_product_info(i)
    pass