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


count = 0
fail_counter = 0
proxies = {'http': proxies_api.get_proxies()}

def get_product_info_by_brand_list(TEST_FLAG=True, csv_file='database/db_brand_final.csv'):
    global count
    global fail_counter
    global proxies

    os.remove('database/db_brand_list_check.csv')
    df = pd.read_csv(csv_file)
    result_df = pd.DataFrame(columns=['dispShopNo', 'brand_No', 'brand_name', 'total', 'status'])
    db_tool.db_save('db_brand_list_check', result_df)

    print('db_brand:', df.shape[0])
    for i in range(df.shape[0]):
        dispShopNo = df.loc[i]['dispShopNo_x']
        if (os.path.exists('database/brand_product_{}.csv'.format(dispShopNo))):
            has_existed_df = pd.read_csv('database/brand_product_{}.csv'.format(dispShopNo))
            brand_name = has_existed_df.loc[0]['brand_name_eng']
            brndNo = has_existed_df.loc[0]['brand_No']
            total_num_df = has_existed_df.shape[0]
            status = 'o'
            data = {
                'dispShopNo': dispShopNo,
                'brand_No': brndNo,
                'brand_name': brand_name, 
                'total': total_num_df, 
                'status': status
            }
            result_df = result_df.append(data, ignore_index=True)
            pd.DataFrame(data, index=[0]).to_csv('database/db_brand_list_check.csv', mode='a', header=False, index=False)
            print('file has existed')
            continue

        brand_name = df.loc[i]['brand_name']
        try:
            status_df, total_num_df, brndNo = cpd.get_product_detail(dispShopNo, proxies)

            if (status_df):
                status = 'o'
            else:
                status = 'x'
                fail_counter += 1
                if fail_counter >= 2:
                    fail_counter = 0
                    proxies = {'http': proxies_api.get_proxies()}
                    continue
            
            data = {
                'dispShopNo': dispShopNo,
                'brand_No': brndNo,
                'brand_name': brand_name, 
                'total': total_num_df, 
                'status': status
            }
            result_df = result_df.append(data, ignore_index=True)
            pd.DataFrame(data, index=[0]).to_csv('database/db_brand_list_check.csv', mode='a', header=False, index=False)
            # 测试用
            if TEST_FLAG:
                count = count + 1
                if count>2 :
                    break
            else:
                # time.sleep(10)
                pass

        except Exception as e:
            fail_counter += 1
            if fail_counter >= 2:
                fail_counter = 0
                proxies = {'http': proxies_api.get_proxies()}
            print('超时或无应答')
            # print(e)
    
    # db_tool.db_save('db_brand_list_check', result_df)
    
        
def main():
    get_product_info_by_brand_list(False)


if __name__ == "__main__":
    main()