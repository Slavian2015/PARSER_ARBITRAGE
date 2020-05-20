from random import choice
import os
import requests
from time import sleep
import time
from urllib.parse import urlparse
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
from fake_useragent import UserAgent
import json
main_path_data = os.path.abspath(r"C:/inetpub/wwwroot/Arbitrage/data")


def proxies():
    if os.path.isfile('proxies.txt'):
        pass
    else:
        req_proxy = RequestProxy()
        PROXIES = "{0}".format(list(map(lambda x: x.get_address(), req_proxy.get_proxy_list())))
        # Open the file for writing
        F = open('proxies.txt', 'w')
        F.writelines(PROXIES)
        F.close()
        pass

def loadRSS():

    # file1 = open("proxies.txt", "r")
    # PROXIES2 = file1.readlines()

    prox = ['36.74.205.128:3128', '103.116.203.242:43520', '186.0.176.147:80', '41.78.243.194:53281']
    pro = ['94.154.208.248:80','89.252.12.88:80', '13.66.220.17:80', '104.45.11.83:80', '104.45.11.83:443']

    # url1 = {'BTC/USD':'https://btc-alpha.com/api/v1/orderbook/BTC_USD'}
    url2 = {'PZM/USD':'https://btc-alpha.com/api/v1/orderbook/PZM_USD'}
    # url3 = {'ETH/USD':'https://btc-alpha.com/api/v1/orderbook/ETH_USD'}
    # url4 = {'XRP/USD':'https://btc-alpha.com/api/v1/orderbook/XRP_USD'}
    # url5 = {'USD/USDT':'https://btc-alpha.com/api/v1/orderbook/USD_USDT'}
    # url6 = {'BTC/USDT':'https://btc-alpha.com/api/v1/orderbook/BTC_USDT'}
    # url7 = {'ETH/USDT':'https://btc-alpha.com/api/v1/orderbook/ETH_USDT'}
    url8 = {'PZM/BTC':'https://btc-alpha.com/api/v1/orderbook/PZM_BTC'}
    # url9 = {'ETH/BTC':'https://btc-alpha.com/api/v1/orderbook/ETH_BTC'}
    # url10 = {'LTC/BTC':'https://btc-alpha.com/api/v1/orderbook/LTC_BTC'}
    # url11 = {'BCH/BTC':'https://btc-alpha.com/api/v1/orderbook/BCH_BTC'}
    # url12 = {'ZEC/BTC':'https://btc-alpha.com/api/v1/orderbook/ZEC_BTC'}


    urls = [
        # url1,
            url2,
        # url3,
            # url4, url5, url6,
            # url7,
        url8,
        # url9,
            # url10,url11,url12
            ]
    alpha = {}

    def set_proxy(session, proxy_candidates=pro, verify=False):
        """
        Configure the session to use one of the proxy_candidates.  If verify is
        True, then the proxy will have been verified to work.
        """
        while True:
            proxy = choice(proxy_candidates)

            # print('NEW PROXY ALFA :', proxy)
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
                            alpha.update(
                                {k: {'sell':
                                         [[float(v['sell'][0]["price"]), float(v['sell'][0]["amount"])],
                                          [float(v['sell'][1]["price"]), (float(v['sell'][0]["amount"]) + float(v['sell'][1]["amount"]))],
                                          [float(v['sell'][2]["price"]), (float(v['sell'][0]["amount"]) + float(v['sell'][1]["amount"]) + float(v['sell'][2]["amount"]))],
                                          [float(v['sell'][3]["price"]), (float(v['sell'][0]["amount"]) + float(
                                              v['sell'][1]["amount"]) + float(v['sell'][2]["amount"]) + float(v['sell'][3]["amount"]))],
                                          ],
                                          'buy':
                                          [[float(v['buy'][0]["price"]), float(v['buy'][0]["amount"])],
                                          [float(v['buy'][1]["price"]), (float(v['buy'][0]["amount"]) + float(v['buy'][1]["amount"]))],
                                          [float(v['buy'][2]["price"]), (float(v['buy'][0]["amount"]) + float(v['buy'][1]["amount"]) + float(v['buy'][2]["amount"]))],
                                           [float(v['buy'][3]["price"]), (float(v['buy'][0]["amount"]) + float(
                                               v['buy'][1]["amount"]) + float(v['buy'][2]["amount"]) + float(v['buy'][3]["amount"]))],

                                           ]}})



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
    return alpha


#################  Get Currency Balance   ###################

def wallet_a():
    import hmac
    from time import time

    def keys():
        if os.path.isfile(main_path_data + "\\keys.json"):
            pass
        else:

            dictionary = {"1": {"key": "Api key",
                                "api": "Api secret"},
                          "2": {"key": "Api key",
                                "api": "Api secret"},
                          "3": {"key": "Api key",
                                "api": "Api secret"},
                          "4": {"key": "Chat id", "api": "Token"}}

            keys1 = json.dumps(dictionary, indent=4)
            # print(' JSON DOESNT EXIST :', keys1)
            # Writing to sample.json
            with open(main_path_data + "\\keys.json", "w") as outfile:
                outfile.write(keys1)
                outfile.close()
                pass

    keys()


    a_file = open(main_path_data + "\\keys.json", "r")
    json_object = json.load(a_file)
    a_file.close()

    input1 = json_object["1"]['key']
    input2 = json_object["1"]['api']

    if input1 != "Api key" and input2 != "Api secret":
        # Свой класс исключений
        class ScriptError(Exception):
            pass

        class ScriptQuitCondition(Exception):
            pass

        def get_auth_headers(self):
            # print('input 1  :', input1)
            # print('input 2  :', input2)

            msg = input1
            sign = hmac.new(input2.encode(), msg.encode(), digestmod='sha256').hexdigest()

            return {
                'X-KEY': input1,
                'X-SIGN': sign,
                'X-NONCE': str(int(time() * 1000)),
            }

        response = requests.get('https://btc-alpha.com/api/v1/wallets/', headers=get_auth_headers({}))

        def resm():
            try:
                # Полученный ответ переводим в строку UTF, и пытаемся преобразовать из текста в объект Python
                obj = json.loads(response.text)
                # Смотрим, есть ли в полученном объекте ключ "error"
                if 'error' in obj and obj['error']:
                    # Если есть, выдать ошибку, код дальше выполняться не будет
                    raise ScriptError(obj['error'])
                # Вернуть полученный объект как результат работы ф-ции


                wallet_a = {}
                # print("APARSER   Wallet    :", '\n', obj)
                for i in obj:
                    # print(i)
                    wallet_a.update({i['currency']: (float(i['balance'])-float(i['reserve']))})

                # print(wallet_a['USDT'])

                return wallet_a
            except ValueError:
                # Если не удалось перевести полученный ответ (вернулся не JSON)
                raise ScriptError('Ошибка анализа возвращаемых данных, получена строка', response)

        return resm()

    else:
        return {}

# t1 = time.time()
# live = loadRSS()
# print(live)
#
# t2 = time.time()
#
# print(t2 - t1)