import os
import pandas as pd

db_dir_path = 'database'

def db_brand(name, url):
    # indexList = index
    brandName = name
    brandUrl = url

    #字典中的 key 值即为 csv 中列名
    dataframe = pd.DataFrame({
        # 'index': indexList,
        'brand_name': brandName,
        'brand_url': brandUrl
    })

    # index 表示是否显示行名，default=True
    if dataframe.to_csv(os.path.join(db_dir_path, 'db_brand.csv'), index=False, sep=','):
        return True
    else:
        return False



def main():
    db_brand()


if __name__ == "__main__":
    main()