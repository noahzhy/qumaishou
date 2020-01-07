import os
import sys
# 导入同级目录下其他文件夹下的文件
sys.path.append("./")
import pandas as pd

# import tools.database_tool as dt
import crawler.crawler_brand as cb
import crawler.crawler_product_detail as cpd
import crawler.crawler_total_product as ctp
import requests
# import crawler.crawler_proxies as proxies_api

def get_img(dispShopNo, img_url):
    img_url = 'http://static.lottedfs.cn/prod/prd-img/52/90/55/00/00/02/20000559052_1.jpg'
    img_name = img_url.split('/')[-1]
    if not os.path.exists('images/{}/{}'.format(dispShopNo, img_name)):
        html = requests.get(img_url)

        with open(os.path.join('images', str(dispShopNo), img_name), 'wb') as file:
            file.write(html.content)
        pass

    else:
        print('img existed')


def save_img_by_dispShopNo(dispShopNo, img_url):
    if not os.path.exists('images/{}'.format(dispShopNo)):
        os.mkdir('images/{}'.format(dispShopNo))
    else:
        print(dispShopNo, 'has existed')
        get_img(dispShopNo, img_url)


def main():
    save_img_by_dispShopNo('test', 1)
    pass


if __name__ == "__main__":
    main()
