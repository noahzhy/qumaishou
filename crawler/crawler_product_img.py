import os
import sys
# 导入同级目录下其他文件夹下的文件
sys.path.append("./")
import pandas as pd
import requests
from fake_useragent import UserAgent

import tools.database_tool as dt
import crawler.crawler_brand as cb
import crawler.crawler_product_detail as cpd
import crawler.crawler_total_product as ctp
# import crawler.crawler_proxies as proxies_api

ua = UserAgent()

def get_img(dispShopNo, img_url, proxies):
    session = requests.session()
    img_name = img_url.split('/')[-1]
    headers = {'User-Agent': ua.random}
    if not os.path.exists('images/{}/{}'.format(dispShopNo, img_name)):
        try:
            html = session.get(url=img_url, headers=headers, proxies=proxies, timeout=5)
            with open(os.path.join('images', str(dispShopNo), img_name), 'wb') as file:
                file.write(html.content)

            print('images/{}/{}'.format(dispShopNo, img_name))
            if dt.get_FileSize('images/{}/{}'.format(dispShopNo, img_name)) < 3:
                os.remove('images/{}/{}'.format(dispShopNo, img_name))
                return False
            else:
                return True

        except Exception as e:
            print(e)
            return False

    else:
        # print('img existed')
        return True


def save_img_by_dispShopNo(dispShopNo, img_url, proxies):
    if not os.path.exists('images/{}'.format(dispShopNo)):
        os.mkdir('images/{}'.format(dispShopNo))

    return get_img(dispShopNo, img_url, proxies)


def main():
    save_img_by_dispShopNo('test', 1)
    pass


if __name__ == "__main__":
    main()
