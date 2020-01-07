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


# proxies = {'http': proxies_api.get_proxies()}
csv_file='database/db_brand_final.csv'
df = pd.read_csv(csv_file)
result_df = pd.read_csv('database/db_brand_list_check.csv')


def get_product_info(row=0, proxies=proxies_api.get_proxies()):

    dispShopNo = df.loc[row]['dispShopNo_x']

    if (os.path.exists('database/brand_product/brand_product_{}.csv'.format(dispShopNo))):
        has_existed_df = pd.read_csv('database/brand_product/brand_product_{}.csv'.format(dispShopNo))
        brand_name = has_existed_df.loc[0]['brand_name_eng']
        brndNo = has_existed_df.loc[0]['brand_No']
        total_num_df = has_existed_df.shape[0]
        
        data = {
            'dispShopNo': dispShopNo,
            'brand_No': brndNo,
            'brand_name': brand_name, 
            'total': total_num_df, 
            'status': 'o'
        }
        # result_df = result_df.append(data, ignore_index=True)
        pd.DataFrame(data, index=[0]).to_csv('database/db_brand_list_check.csv', mode='a', header=False, index=False)
        # print(dispShopNo, 'file has existed')
        return True
        # continue

    else:
        try:
            status_df, total_num_df, brndNo = cpd.get_product_detail(dispShopNo, proxies)

            if (status_df):
                status = 'o'
            else:
                status = 'x'
            
            brand_name = df.loc[row]['brand_name']

            data = {
                'dispShopNo': dispShopNo,
                'brand_No': brndNo,
                'brand_name': brand_name, 
                'total': total_num_df, 
                'status': status
            }
            # result_df = result_df.append(data, ignore_index=True)
            pd.DataFrame(data, index=[0]).to_csv('database/db_brand_list_check.csv', mode='a', header=False, index=False)
            return True

        except Exception as e:
            print('超时或无应答')
            return False
            # print(e)
    
        
def main():
    get_product_info()


if __name__ == "__main__":
    main()