import os
import pandas as pd


db_dir_path = 'database'


def remove_repetition(path_dataframe):
    return path_dataframe.drop_duplicates(subset=None, keep='first', inplace=False)


def db_brand(db_name, brand_name, brand_url):
    #字典中的 key 值即为 csv 中列名
    dataframe = pd.DataFrame({
        # 'index': indexList,
        'brand_name': brand_name,
        'brand_url': brand_url
    })

    dataframe = remove_repetition(dataframe)
    print('db_brand:', dataframe.shape[0])

    # index 表示是否显示行名，default=True
    if dataframe.to_csv(os.path.join(db_dir_path, '{}.csv'.format(db_name)), index=False, sep=','):
        return True
    else:
        return False


def db_product_img(df):
    # dataframe = pd.DataFrame({
    #     'product_No': prdNo,
    #     'brand_name': brand,
    #     'product_name': product,
    #     'img_url': img_url,
    #     'us_price': us_price
    # })
    dataframe = pd.DataFrame(df)
    print('db_brand:', dataframe.shape[0])
    # index 表示是否显示行名，default=True
    if dataframe.to_csv(os.path.join(db_dir_path, 'db_product_img.csv'), index=False, sep=','):
        return True
    else:
        return False


def main():
    # db_brand_eng()
    pass


if __name__ == "__main__":
    main()