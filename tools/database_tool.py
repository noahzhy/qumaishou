import os
import pandas as pd


db_dir_path = 'database'


def remove_repetition(path_dataframe):
    return path_dataframe.drop_duplicates(subset=None, keep='first', inplace=False)


def db_brand(db_name, brand_no, brand_name, brand_url):
    #字典中的 key 值即为 csv 中列名
    df = pd.DataFrame({
        # 'index': indexList,
        'brand_No': brand_no,
        'brand_name': brand_name,
        'brand_url': brand_url
    })

    df = remove_repetition(df)
    print('db_brand:', df.shape[0])

    # index 表示是否显示行名，default=True
    if df.to_csv(os.path.join(db_dir_path, '{}.csv'.format(db_name)), index=False, sep=','):
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


def merge_db_brand_lang(original='ENG', other_lang='CHN'):
    # data = pd.read_csv(os.path.join(db_dir_path, 'db_brand_{}.csv'.format(original.lower())))
    # df = pd.DataFrame(data)
    # [print(i) for i in df.loc[:,'brand_name']]

    df = pd.merge(original, other_lang, how='left', on='user_id')



def main():
    # db_brand_eng()
    merge_db_brand_lang()
    pass


if __name__ == "__main__":
    main()