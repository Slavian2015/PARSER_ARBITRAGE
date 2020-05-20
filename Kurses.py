import json
import concurrent.futures
import requests
# import time
from random import choice
from fake_useragent import UserAgent
import os


main_path_data = os.path.abspath(r"C:/inetpub/wwwroot/Arbitrage/data")

a_file = open(main_path_data + "\\keys.json", "r")
json_object = json.load(a_file)
a_file.close()

input_hot_key = json_object["3"]['key']
input_hot_api = json_object["3"]['api']

input_live_key = json_object["2"]['key']
input_live_api = json_object["2"]['api']

input_a_key = json_object["1"]['key']
input_a_api = json_object["1"]['api']

def hot_w():
    import hashlib
    if input_hot_key != "Api key" and input_hot_api != "Api secret":
        str2hash = 'api_key={}&assets=["BTC","ETH","ZEC","USDT","LTC","XRP","PZM","XLM"]&secret_key={}'.format(input_hot_key,
                                                                                                               input_hot_api)
        result = hashlib.md5(str2hash.encode())
        sign = result.hexdigest().upper()
        url = 'https://api.hotbit.io/api/v1/balance.query?api_key={}&assets=["BTC","ETH","ZEC","USDT","LTC","XRP","PZM","XLM"]&sign={}'.format(
            input_hot_key,
            sign)
        return url
    else:
        return ''
def live_w(self):
    import hmac
    if input_live_key != "Api key" and input_live_api != "Api secret":
        sign = hmac.new(input_live_api.encode(), digestmod='sha256').hexdigest().upper()
        headers = {
            'Api-key': input_live_key,
            'Sign': sign,
        }
        return headers
    else:
        return {}
def alfa_w(self):
    import hmac
    from time import time
    if input_a_key != "Api key" and input_a_api != "Api secret":
        msg = input_a_key
        sign = hmac.new(input_a_api.encode(), msg.encode(), digestmod='sha256').hexdigest()

        return {
            'X-KEY': input_a_key,
            'X-SIGN': sign,
            'X-NONCE': str(int(time() * 1000)),
        }
    else:
        return {}

url2 = 'https://btc-alpha.com/api/v1/orderbook/PZM_USD'
url3 = 'https://api.livecoin.net/exchange/all/order_book'
url8 = 'https://btc-alpha.com/api/v1/orderbook/PZM_BTC'
url6 = 'https://api.hotbit.io/api/v1/order.depth?market=PZM/BTC&limit=5&interval=1e-8'
url5 = 'https://api.hotbit.io/api/v1/order.depth?market=PZM/USDT&limit=5&interval=1e-8'

url_Alfa = 'https://btc-alpha.com/api/v1/wallets'
url_Hot = hot_w()
url_Live = 'https://api.livecoin.net/payment/balances'

urls = [
    url2,
    url8,
    url3,
url5,
url6,
url_Alfa,
url_Hot,
url_Live
]

def kurs():
    out = dict()
    CONNECTIONS = 100
    TIMEOUT = 5

    pro = ['94.154.208.248:80', '89.252.12.88:80', '13.66.220.17:80', '104.45.11.83:80']
    ua = UserAgent()
    proxy = choice(pro)
    PARAMS = {'User-Agent': ua.random, 'http': proxy, 'https': proxy}
    PARAMS_alfa = alfa_w({})
    # PARAMS_hot = hot_w({})
    PARAMS_live = live_w({})

    def load_url(url, timeout, params, PARAM_alfa, PARAM_live):
        if url == 'https://btc-alpha.com/api/v1/wallets':
            ans = requests.get(url, headers=PARAM_alfa, timeout=timeout)
            return url, ans.json()
        elif url == input_hot_api:
            ans = requests.get(url, timeout=timeout)
            return url, ans.json()
        elif url == 'https://api.livecoin.net/payment/balances':
            ans = requests.get(url, headers=PARAM_live, timeout=timeout)
            return url, ans.json()
        else:
            ans = requests.get(url, data=params, timeout=timeout)
            return url, ans.json()

    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_to_url = (executor.submit(load_url, url, TIMEOUT, PARAMS, PARAMS_alfa, PARAMS_live) for url in urls)

        for future in concurrent.futures.as_completed(future_to_url):
            try:
                data = future.result()
                # print(data)
            except Exception as exc:
                data = str(type(exc))
            finally:
                out.update({data[0]:data[1]})

    return out


# time1 = time.time()
# json = json.dumps(kurses())
# f = open("my_tornado.json","w")
# f.write(json)
# f.close()
#
# time2 = time.time()
# print(f'Took {time2-time1:.2f} s')