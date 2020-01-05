import os
import sys
import pandas as pd
# 导入同级目录下其他文件夹下的文件
sys.path.append("./")

import crawler.crawler_product_detail as cpd


def get_brand_list(csv_file='database/db_brand_final.csv'):
    df = pd.read_csv(csv_file)
    print('db_brand:', df.shape[0])


def main():
    get_brand_list()


if __name__ == "__main__":
    main()