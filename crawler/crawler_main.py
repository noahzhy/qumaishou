import os
import sys
# 导入同级目录下其他文件夹下的文件
sys.path.append("./")
import time
import pandas as pd
import multiprocessing

import tools.database_tool as dt
import crawler.crawler_brand as cb
import crawler.crawler_product_detail as cpd
import crawler.crawler_total_product as ctp
import crawler.crawler_product_img as cpi
import crawler.crawler_proxies as proxies_api


fail_counter = 0
proxies = {}

def refresh_ip():
    global proxies
    proxies = {'http': proxies_api.get_proxies()}


def total_product_info(rows):
    global fail_counter

    if not ctp.get_product_info(rows, proxies):
        fail_counter += 1

    # 代理IP更换频率
    if fail_counter >= 3:
        # refresh_ip()
        fail_counter = 0


def total_img_info(dispShopNo, img_url):
    global fail_counter

    if not cpi.save_img_by_dispShopNo(dispShopNo, img_url, proxies):
        fail_counter += 1

    # 代理IP更换频率
    if fail_counter >= 2:
        refresh_ip()
        fail_counter = 0


def get_total_product_info_by_multi_processing():
    rows = []
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    if os.path.exists('database/db_brand_list_check.csv'):
        os.remove('database/db_brand_list_check.csv')

    csv_file = 'database/db_brand_final.csv'
    
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        # 初始化 db_brand_list_check.csv
        result_df = pd.DataFrame(columns=['dispShopNo', 'brand_No', 'brand_name', 'total', 'status'])
        dt.db_save('db_brand_list_check', result_df)

        [rows.append(i) for i in range(0, df.shape[0])]

        pool.map(total_product_info, rows)
        pool.close()
        pool.join()

def get_total_img_by_multi_processing():
    df = pd.read_csv('database/db_total_product.csv')
    # print(df)
    dispShopNo, img_url = [], []
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    for index, i in df.iterrows():
        # print(i)
        # break
        dispShopNo.append(i['brand_No'])
        img_url.append(i['img_url'])

    zip_args = list(zip(dispShopNo, img_url))
    pool.starmap(total_img_info, zip_args)
    pool.close()
    pool.join()


if __name__ == '__main__':
    # cb.get_all_brand('CHN')
    # cb.get_all_brand('ENG')
    # dt.intersection_db_brand()

    # get_total_product_info_by_multi_processing()
    get_total_img_by_multi_processing()
    pass