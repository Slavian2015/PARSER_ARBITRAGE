from random import choice
import os
import requests
from time import sleep
import time
from urllib.parse import urlparse
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
from fake_useragent import UserAgent
import hashlib
import json

main_path_data = os.path.abspath(r"C:/inetpub/wwwroot/Arbitrage/data")


def loadRSS():
    # file1 = open("proxies.txt", "r")
    # PROXIES2 = file1.readlines()
    prox = ['36.74.205.128:3128', '103.116.203.242:43520', '186.0.176.147:80', '128.199.150.150:47503',
            '41.78.243.189:53281', '46.19.225.141:8888', '190.166.249.44:37359', '41.78.243.194:53281']
    pro = ['94.154.208.248:80', '89.252.12.88:80', '13.66.220.17:80', '104.45.11.83:80', '104.45.11.83:443']

    # url1 = {'BTC/USD':'https://api.hotbit.io/api/v1/order.depth?market=BTC/USD&limit=5&interval=1e-8'}
    url2 = {'PZM/USDT': 'https://api.hotbit.io/api/v1/order.depth?market=PZM/USDT&limit=5&interval=1e-8'}
    # url3 = {'ETH/USD':'https://api.hotbit.io/api/v1/order.depth?market=ETH/USD&limit=5&interval=1e-8'}
    url4 = {'PZM/BTC': 'https://api.hotbit.io/api/v1/order.depth?market=PZM/BTC&limit=5&interval=1e-8'}
    # url5 = {'LTC/BTC':'https://api.hotbit.io/api/v1/order.depth?market=LTC/BTC&limit=5&interval=1e-8'}
    # url6 = {'BTC/USDT':'https://api.hotbit.io/api/v1/order.depth?market=BTC/USDT&limit=5&interval=1e-8'}
    # url7 = {'ETH/USDT':'https://api.hotbit.io/api/v1/order.depth?market=ETH/USDT&limit=5&interval=1e-8'}
    # url8 = {'XRP/BTC':'https://api.hotbit.io/api/v1/order.depth?market=XRP/BTC&limit=5&interval=1e-8'}
    # url9 = {'ETH/BTC':'https://api.hotbit.io/api/v1/order.depth?market=ETH/BTC&limit=5&interval=1e-8'}
    # url10 = {'BCH/BTC':'https://api.hotbit.io/api/v1/order.depth?market=BCH/BTC&limit=5&interval=1e-8'}

    urls = [
        # url1,
        url2,
        # url3,
        url4,
        # url5, url6,
        # url7,
        # url8,
        # url9,
        # url10
    ]
    hot = {}

    def set_proxy(session, proxy_candidates=pro, verify=False):
        """
        Configure the session to use one of the proxy_candidates.  If verify is
        True, then the proxy will have been verified to work.
        """
        while True:
            proxy = choice(proxy_candidates)
            # print('NEW PROXY HOT :', proxy)
            session.proxies = {urlparse(proxy).scheme: proxy}
            if not verify:
                return
            try:
                print(session.get('https://httpbin.org/ip').json())
                return
            except Exception:
                session.proxies = {urlparse(next(proxy)).scheme: proxy}
                print("EXCEPTION")
                pass

    def scrape_page():
        # ua = UserAgent()
        # session = requests.Session()
        # session.headers = {'User-Agent': ua.random}
        # set_proxy(session)

        while True:
            # try:
            for i in urls:
                ua = UserAgent()
                session = requests.Session()
                session.headers = {'User-Agent': ua.random}
                set_proxy(session)

                try:
                    for k, item in i.items():
                        resp = session.get(item)
                        v = resp.json()

                        # print('NEW URL HOT :', item)

                        hot.update({k: {
                            'sell': [[v['result']['asks'][0][0], v['result']['asks'][0][1]],
                                     [v['result']['asks'][1][0],
                                      (float(v['result']['asks'][0][1]) + float(v['result']['asks'][1][1]))],
                                     [v['result']['asks'][2][0], (float(v['result']['asks'][0][1]) + float(
                                         v['result']['asks'][1][1]) + float(v['result']['asks'][2][1]))],
                                     [v['result']['asks'][3][0], (float(v['result']['asks'][0][1]) + float(
                                         v['result']['asks'][1][1]) + float(v['result']['asks'][2][1]) + float(
                                         v['result']['asks'][3][1]))]
                                     ],

                            'buy': [[v['result']['bids'][0][0], v['result']['bids'][0][1]],
                                    [v['result']['bids'][1][0],
                                     (float(v['result']['bids'][0][1]) + float(v['result']['bids'][1][1]))],
                                    [v['result']['bids'][2][0], (float(v['result']['bids'][0][1]) + float(
                                        v['result']['bids'][1][1]) + float(v['result']['bids'][2][1]))],
                                    [v['result']['bids'][3][0], (float(v['result']['bids'][0][1]) + float(
                                        v['result']['bids'][1][1]) + float(v['result']['bids'][2][1]) + float(
                                        v['result']['bids'][3][1]))]
                                    ]
                        }})

                except Exception as e:
                    session.headers = {'User-Agent': ua.random}
                    set_proxy(session, verify=True)
                    sleep(0.1)

            break
            # except Exception as e:
            #     session.headers = {'User-Agent': ua.random}
            #     set_proxy(session, verify=True)
            #     sleep(0.1)

    scrape_page()

    # print(hot)
    return hot


def wallet_h():
    a_file = open(main_path_data + "\\keys.json", "r")
    json_object = json.load(a_file)
    a_file.close()

    input1 = json_object["3"]['key']
    input2 = json_object["3"]['api']

    if input1 != "Api key" and input2 != "Api secret":
        str2hash = 'api_key={}&assets=["BTC","ETH","ZEC","USDT","LTC","XRP","PZM","XLM"]&secret_key={}'.format(input1,
                                                                                                               input2)
        result = hashlib.md5(str2hash.encode())
        sign = result.hexdigest().upper()
        url = 'https://api.hotbit.io/api/v1/balance.query?api_key={}&assets=["BTC","ETH","ZEC","USDT","LTC","XRP","PZM","XLM"]&sign={}'.format(
            input1,
            sign)
        res = requests.request("GET", url)
        exam = res.json()

        wallet_h = {}

        for i in exam['result']:
            wallet_h.update({i: exam['result'][i]['available']})

        return wallet_h
    else:
        return {}

# t1 = time.time()
# live = loadRSS()
# print(live)
#
# t2 = time.time()
#
# print(t2 - t1)