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
import crawler.crawler_proxies as proxies_api



fail_counter = 0
proxies = {}


def main(rows):
    global fail_counter

    if not ctp.get_product_info(rows, proxies):
        fail_counter += 1

    if fail_counter >= 1:
        refresh_ip()
        fail_counter = 0


def refresh_ip():
    # global proxies
    proxies = {'http': proxies_api.get_proxies()}


if __name__ == '__main__':

    # cb.get_all_brand('CHN')
    # cb.get_all_brand('ENG')
    # dt.intersection_db_brand()

    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    rows = []

    try: 
        os.remove('database/db_brand_list_check.csv')
    except:
        pass

    csv_file = 'database/db_brand_final.csv'
    df = pd.read_csv(csv_file)
    result_df = pd.DataFrame(columns=['dispShopNo', 'brand_No', 'brand_name', 'total', 'status'])
    dt.db_save('db_brand_list_check', result_df)

    [rows.append(i) for i in range(0, df.shape[0])]
    # print(rows[-1])
        # print(df.loc[i][])
        # print(type(i))
        # ctp.get_product_info(i)

    pool.map(main, rows)
    pool.close()
    pool.join()
    pass