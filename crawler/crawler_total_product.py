import os
import sys
import pandas as pd
# 导入同级目录下其他文件夹下的文件
sys.path.append("./")

import crawler.crawler_product_detail as cpd
import tools.data_check as data_check
import tools.database_tool as db_tool

def get_brand_list(csv_file='database/db_brand_final.csv'):
    df = pd.read_csv(csv_file)
    result_df = pd.DataFrame(columns=['brand_No', 'brand_name', 'total', 'status'])
    print('db_brand:', df.shape[0])
    for i in range(df.shape[0]):
        brand_name = df.loc[i]['brand_name']
        brand_No = df.loc[i]['brand_No_x']
        status_df, total_num_df = cpd.get_product_detail(brand_No)
        if (status_df):
            status = 'o'
        else:
            status = 'x'
        
        data = {
            'brand_No': brand_No, 
            'brand_name': brand_name, 
            'total': total_num_df, 
            'status': status
        }
        result_df = result_df.append(data, ignore_index=True)
        # 测试用
        break
    db_tool.db_brand_product('db_brand_list_check', result_df)
    
        
def main():
    get_brand_list()


if __name__ == "__main__":
    main()