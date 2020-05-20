# import requests
import os
import time
import faster_than_requests.src.faster_than_requests as requests

main_path_data = os.path.abspath(r"C:/inetpub/wwwroot/Arbitrage/data")



def restart():
    url = 'https://api.livecoin.net/exchange/all/order_book'
    res = requests.request("GET", url)
    exam = res.json()

    valuta = ['BTC/USD','LTC/USD','ETH/USD','XRP/USD','USDT/USD','BTC/USDT','ETH/USDT','XRP/BTC','ETH/BTC','LTC/BTC','BCH/BTC','ZEC/BTC', 'PZM/USD', 'PZM/USDT', 'PZM/BTC',]
    live = {}

    for i in valuta:
        for k,v in exam.items():
            if k == i:
                del v['timestamp']
                v['sell'] = v.pop('asks')
                v['buy'] = v.pop('bids')
                live.update({k: {
                        'sell': [[v['sell'][0][0], v['sell'][0][1]],
             [v['sell'][1][0], (float(v['sell'][0][1]) + float(v['sell'][1][1]))],
             [v['sell'][2][0], (float(v['sell'][0][1]) + float(v['sell'][1][1]) + float(v['sell'][2][1]))],
                                 [v['sell'][3][0], (float(v['sell'][0][1]) + float(v['sell'][1][1]) + float(v['sell'][2][1]) + float(v['sell'][3][1]))]],
                    'buy': [[v['buy'][0][0], v['buy'][0][1]],
            [v['buy'][1][0], (float(v['buy'][0][1]) + float(v['buy'][1][1]))],
            [v['buy'][2][0], (float(v['buy'][0][1]) + float(v['buy'][1][1]) + float(v['buy'][2][1]))],
                            [v['buy'][3][0], (float(v['buy'][0][1]) + float(v['buy'][1][1]) + float(v['buy'][2][1]) + float(v['buy'][3][1]))]
                            ]}})

    return live

def wallet_l():
    import hmac
    import json

    a_file = open(main_path_data + "\\keys.json", "r")
    json_object = json.load(a_file)
    a_file.close()

    input1 = json_object["2"]['key']
    input2 = json_object["2"]['api']

    if input1 != "Api key" and input2 != "Api secret":

        # Свой класс исключений
        class ScriptError(Exception):
            pass
        class ScriptQuitCondition(Exception):
            pass

        sign = hmac.new(input2.encode(), digestmod='sha256').hexdigest().upper()
        headers = {
            'Api-key': input1,
            'Sign': sign,
        }
        response = requests.get('https://api.livecoin.net/payment/balances', headers=headers)

        def resm():
            try:
                # Полученный ответ переводим в строку UTF, и пытаемся преобразовать из текста в объект Python
                obj = json.loads(response.text)
                # Смотрим, есть ли в полученном объекте ключ "error"
                if 'error' in obj and obj['error']:
                    # Если есть, выдать ошибку, код дальше выполняться не будет
                    raise ScriptError(obj['error'])
                # Вернуть полученный объект как результат работы ф-ции
                return obj
            except ValueError:
                # Если не удалось перевести полученный ответ (вернулся не JSON)
                raise ScriptError('Ошибка анализа возвращаемых данных, получена строка', response)

        resm = resm()

        wallet_l = {}

        for i in resm:
            if i['type'] == "available" and i['value'] > 0:
                wallet_l.update({i['currency']: i['value']})

        return wallet_l

    else:
        return {}




t1 = time.time()
# requests.get("http://httpbin.org/get")

url = 'https://api.livecoin.net/exchange/all/order_book'
res = requests.get(url)
exam = res.json()


# live = restart()
# print(live)

t2 = time.time()
e1 = 1
print(t2 - t1)