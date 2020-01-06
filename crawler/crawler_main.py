import os
import sys
# 导入同级目录下其他文件夹下的文件
sys.path.append("./")


import tools.database_tool as dt
import crawler.crawler_brand as cb
import crawler.crawler_product_detail as cpd
import crawler.crawler_total_product as ctp


def main():
    # cb.get_all_brand('CHN')
    # cb.get_all_brand('ENG')
    # dt.intersection_db_brand()
    ctp.get_product_info_by_brand_list(False)
    pass


if __name__ == "__main__":
    main()