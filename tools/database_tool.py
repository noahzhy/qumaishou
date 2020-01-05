import os
import pandas as pd
import sys
import glob


db_dir_path = 'database'


def db_save(db_name, df):
    # index 表示是否显示行名，default=True
    if df.to_csv(os.path.join(db_dir_path, '{}.csv'.format(db_name)), index=False, sep=','):
        return True
    else:
        return False


def remove_repetition(df, key=None):
    return df.drop_duplicates(subset=key, keep='first', inplace=False)


def db_brand(db_name, df):
    #字典中的 key 值即为 csv 中列名
    df = remove_repetition(df)
    print('db_brand:', df.shape[0])
    db_save(db_name, df)
    return df


def db_brand_product(db_name, df):
    # dataframe = pd.DataFrame({
    #     'product_No': prdNo,
    #     'brand_name': brand,
    #     'product_name': product,
    #     'img_url': img_url,
    #     'us_price': us_price
    # })
    dataframe = pd.DataFrame(df)
    print('db_brand:', dataframe.shape[0])
    db_save('brand_product_{}'.format(db_name), df)
    return df


def db_add_mode(db_name, df):
    pass


def intersection_db_brand():
    '''合并品牌数据库，最终英文版的'''
    d1 = pd.read_csv(os.path.join(db_dir_path, 'db_brand_eng.csv'))
    d2 = pd.read_csv(os.path.join(db_dir_path, 'db_brand_chn.csv'))
    df = pd.merge(d1, d2, how='left', on='brand_name')
    df = remove_repetition(df, 'brand_name')
    df = df.loc[:, ['brand_No_x', 'brand_name', 'brand_url_x']]
    db_save('db_brand_final', df)
    print('df_merged:', df.shape[0])
    return df


def main():
    # db_brand_eng()
    # db_brand_merge()
    # intersection_db_brand()
    pass


if __name__ == "__main__":
    main()