import os
import requests


session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
}

def get_proxies():
    url = 'http://dps.kdlapi.com/api/getdps/?orderid=997828592555021&num=1&pt=1&sep=1'
    r = session.get(url=url, headers=headers)
    return r.text


def main():
    print(get_proxies())


if __name__ == "__main__":
    main()