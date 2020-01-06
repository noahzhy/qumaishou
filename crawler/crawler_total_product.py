import os
import sys
import pandas as pd
# 导入同级目录下其他文件夹下的文件
sys.path.append("./")

import crawler.crawler_product_detail as cpd
import tools.data_check as data_check
import tools.database_tool as db_tool


count = 0

def get_brand_list(csv_file='database/db_brand_final.csv'):
    global count
    df = pd.read_csv(csv_file)
    result_df = pd.DataFrame(columns=['dispShopNo', 'brand_No', 'brand_name', 'total', 'status'])
    print('db_brand:', df.shape[0])
    for i in range(df.shape[0]):
        brand_name = df.loc[i]['brand_name']
        dispShopNo = df.loc[i]['dispShopNo_x']
        status_df, total_num_df, brndNo = cpd.get_product_detail(dispShopNo)
        if (status_df):
            status = 'o'
        else:
            status = 'x'
        
        data = {
            'dispShopNo': dispShopNo,
            'brand_No': brndNo,
            'brand_name': brand_name, 
            'total': total_num_df, 
            'status': status
        }
        result_df = result_df.append(data, ignore_index=True)
        # 测试用
        count = count + 1
        if count>3 :
            break
    db_tool.db_brand_product('db_brand_list_check', result_df)
    
        
def main():
    get_brand_list()


if __name__ == "__main__":
    main()