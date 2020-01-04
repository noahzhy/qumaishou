import os
import pandas as pd


db_dir_path = 'database'


def db_save(db_name, df):
    # index 表示是否显示行名，default=True
    if df.to_csv(os.path.join(db_dir_path, '{}.csv'.format(db_name)), index=False, sep=','):
        return True
    else:
        return False


def remove_repetition(path_dataframe):
    return path_dataframe.drop_duplicates(subset=None, keep='first', inplace=False)


def db_brand(db_name, df):
    #字典中的 key 值即为 csv 中列名
    df = remove_repetition(df)
    print('db_brand:', df.shape[0])
    db_save(db_name, df)
    return df


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
    db_save('db_product_img', df)


def db_brand_merge(db_name, df1, df2):
    df = pd.merge(df1, df2, how='outer', on='brand_No')
    df = df.drop_duplicates(subset='brand_No', keep='first', inplace=False)
    db_save(db_name, df)


def concat_db_brand_lang(original='ENG', other_lang='CHN'):
    df1 = pd.read_csv(os.path.join(db_dir_path, 'db_brand_{}.csv'.format(original.lower())))
    df2 = pd.read_csv(os.path.join(db_dir_path, 'db_brand_{}.csv'.format(other_lang.lower())))
    df = pd.concat([df1, df2])
    db_save('db_brand_concat', df)


def main():
    # db_brand_eng()
    merge_db_brand_lang()
    # concat_db_brand_lang()
    pass


if __name__ == "__main__":
    main()