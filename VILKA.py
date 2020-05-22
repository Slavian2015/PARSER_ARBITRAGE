import pandas as pd
import json
import os
import datetime as dt
# import Hot_parser
# import Live_parser
# import A_parser
import requests
import Avtomat
import time
import Kurses
from functools import reduce
import re

##################################   SHOW ALL ROWS & COLS   ####################################
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', None)

main_path_data = os.path.abspath(r"C:/inetpub/wwwroot/Arbitrage/data")


#################################   COMMISSIONS   ##########################################
if os.path.isfile(main_path_data + "\\commis.json"):
    f = open(main_path_data + "\\commis.json")
    com = json.load(f)
    pass
else:
    dictionary= {"main": {
        "hot": 1.0006,
        "alfa": 1.002,
        "live": 1.0018
                        }}
    com = json.dumps(dictionary, indent=4)

    # Writing to sample.json
    with open(main_path_data + "\\commis.json", "w") as outfile:
        outfile.write(com)
        outfile.close()
        pass

def restart():
    start11 = time.process_time()
    my_col = ['TIME', 'birga_x', 'birga_y', 'rates_x', 'rates_y', 'valin_x', 'valin_y', 'valout_y', 'volume_x',
              'volume_y', 'start', 'step', 'back', 'profit', 'perc', 'volume']
    if os.path.isfile(main_path_data + "\\all_data.csv"):
        pass
    else:
        final2 = pd.DataFrame(columns=my_col)
        final2.to_csv(main_path_data + "\\all_data.csv", header=True)
        pass
    # t31 = time.time()
    # hot = Hot_parser.loadRSS()
    # t32 = time.time()
    # print("HOT  :", (t32 - t31))
    # live = Live_parser.restart()
    # t33 = time.time()
    # print("LIVE  :", (t33 - t32))
    # alfa = A_parser.loadRSS()
    # t34 = time.time()
    # print("ALFA  :", (t34 - t33))


    t31 = time.time()


    dictionary2 = json.dumps(Kurses.kurs())

    t34 = time.time()
    loaded_time = (t34 - t31)
    print("KURSES  :", loaded_time)

    if loaded_time > 3:
        print("########      BIGGER")
        return
    else:
        print("########     SMALLER")
        pass

    dictionary = json.loads(dictionary2)
    def live2(exam):

        valuta = ['BTC/USD', 'LTC/USD', 'ETH/USD', 'XRP/USD', 'USDT/USD', 'BTC/USDT', 'ETH/USDT', 'XRP/BTC', 'ETH/BTC',
                  'LTC/BTC', 'BCH/BTC', 'ZEC/BTC', 'PZM/USD', 'PZM/USDT', 'PZM/BTC', ]
        live = {}

        for i in valuta:
            for k, v in exam.items():
                if k == i:
                    del v['timestamp']
                    v['sell'] = v.pop('asks')
                    v['buy'] = v.pop('bids')
                    live.update({k: {
                        'sell': [[v['sell'][0][0], v['sell'][0][1]],
                                 [v['sell'][1][0], (float(v['sell'][0][1]) + float(v['sell'][1][1]))],
                                 [v['sell'][2][0],
                                  (float(v['sell'][0][1]) + float(v['sell'][1][1]) + float(v['sell'][2][1]))],
                                 [v['sell'][3][0], (float(v['sell'][0][1]) + float(v['sell'][1][1]) + float(
                                     v['sell'][2][1]) + float(v['sell'][3][1]))]],
                        'buy': [[v['buy'][0][0], v['buy'][0][1]],
                                [v['buy'][1][0], (float(v['buy'][0][1]) + float(v['buy'][1][1]))],
                                [v['buy'][2][0],
                                 (float(v['buy'][0][1]) + float(v['buy'][1][1]) + float(v['buy'][2][1]))],
                                [v['buy'][3][0], (float(v['buy'][0][1]) + float(v['buy'][1][1]) + float(
                                    v['buy'][2][1]) + float(v['buy'][3][1]))]
                                ]}})

        return live
    def a(k, v):
        alpha = {}
        alpha.update(
            {k: {'sell':
                     [[float(v['sell'][0]["price"]), float(v['sell'][0]["amount"])],
                      [float(v['sell'][1]["price"]), (float(v['sell'][0]["amount"]) + float(v['sell'][1]["amount"]))],
                      [float(v['sell'][2]["price"]),
                       (float(v['sell'][0]["amount"]) + float(v['sell'][1]["amount"]) + float(v['sell'][2]["amount"]))],
                      [float(v['sell'][3]["price"]), (float(v['sell'][0]["amount"]) + float(
                          v['sell'][1]["amount"]) + float(v['sell'][2]["amount"]) + float(v['sell'][3]["amount"]))],
                      ],
                 'buy':
                     [[float(v['buy'][0]["price"]), float(v['buy'][0]["amount"])],
                      [float(v['buy'][1]["price"]), (float(v['buy'][0]["amount"]) + float(v['buy'][1]["amount"]))],
                      [float(v['buy'][2]["price"]),
                       (float(v['buy'][0]["amount"]) + float(v['buy'][1]["amount"]) + float(v['buy'][2]["amount"]))],
                      [float(v['buy'][3]["price"]), (float(v['buy'][0]["amount"]) + float(
                          v['buy'][1]["amount"]) + float(v['buy'][2]["amount"]) + float(v['buy'][3]["amount"]))],

                      ]}})
        return alpha
    def ho(k, v):

        hot = {}
        hot.update({k: {
            'sell': [[v['result']['asks'][0][0], v['result']['asks'][0][1]],
                     [v['result']['asks'][1][0], (float(v['result']['asks'][0][1]) + float(v['result']['asks'][1][1]))],
                     [v['result']['asks'][2][0], (
                             float(v['result']['asks'][0][1]) + float(v['result']['asks'][1][1]) + float(
                         v['result']['asks'][2][1]))],
                     [v['result']['asks'][3][0], (
                             float(v['result']['asks'][0][1]) + float(v['result']['asks'][1][1]) + float(
                         v['result']['asks'][2][1]) + float(v['result']['asks'][3][1]))]
                     ],

            'buy': [[v['result']['bids'][0][0], v['result']['bids'][0][1]],
                    [v['result']['bids'][1][0], (float(v['result']['bids'][0][1]) + float(v['result']['bids'][1][1]))],
                    [v['result']['bids'][2][0], (
                            float(v['result']['bids'][0][1]) + float(v['result']['bids'][1][1]) + float(
                        v['result']['bids'][2][1]))],
                    [v['result']['bids'][3][0], (
                            float(v['result']['bids'][0][1]) + float(v['result']['bids'][1][1]) + float(
                        v['result']['bids'][2][1]) + float(v['result']['bids'][3][1]))]
                    ]
        }})
        return hot

    alfa = {}
    hot = {}
    live = {}
    for k, v in dictionary.items():
        if 'livecoin.net/exchange' in f'**{k}**':
            live = live2(dictionary[k])
        elif 'PZM/BTC&limit=5' in f'**{k}**':
            hot.update(ho('PZM/BTC', dictionary[k]))
        elif 'PZM/USDT&limit=5' in f'**{k}**':
            hot.update(ho('PZM/USDT', dictionary[k]))

        elif 'orderbook/PZM_BTC' in f'**{k}**':
            alfa.update(a('PZM/BTC', dictionary[k]))
        elif 'orderbook/PZM_USD' in f'**{k}**':
            alfa.update(a('PZM/USD', dictionary[k]))
        else:
            pass
    if callable(live) == True:
        live = {'live': {}}
    else:
        pass


    birgi = {'alfa': alfa, 'live': live, 'hot': hot}

    birga = []
    valin = []
    valout = []
    rates = []
    volume = []


    ###########   Collected all kurses  ############
    def tab(item, value):
        # print('ITEM     ################', item)

        for k, v in item.items():
            list = k.split('/')


            abc = [0, 1, 2]
            for i in abc:
                birga.append(value)
                valin.append(list[0])
                valout.append(list[1])


                r = ("{0:,.10f}".format(float((item[k]['buy'][i][0]))))
                r2 = r.replace(',', '')
                v = ("{0:,.10f}".format(float((item[k]['buy'][i][1]))))
                v2 = v.replace(',', '')

                rates.append(r2)
                volume.append(v2)

                birga.append(value)
                valin.append(list[1])
                valout.append(list[0])
                r21 = ("{0:,.10f}".format(float((item[k]['sell'][i][0]))))
                r22 = r21.replace(',', '')
                v21 = ("{0:,.10f}".format(float((item[k]['sell'][i][1]))))
                v22 = v21.replace(',', '')
                rates.append(r22)
                volume.append(v22)

        return

    for value, item in birgi.items():
        tab(item,value)

    dw = {'birga': birga, 'valin': valin, 'valout': valout, 'rates': rates, 'volume': volume}
    df = pd.DataFrame(data=dw)

    dfs2 = pd.merge(df, df, left_on=df['valout'], right_on=df['valin'], how='outer')
    dfs2['rates_x'] = dfs2['rates_x'].apply(pd.to_numeric, errors='coerce')
    dfs2['rates_y'] = dfs2['rates_y'].apply(pd.to_numeric, errors='coerce')
    dfs2['volume_x'] = dfs2['volume_x'].apply(pd.to_numeric, errors='coerce')
    dfs2['volume_y'] = dfs2['volume_y'].apply(pd.to_numeric, errors='coerce')
    dfs2.drop(['key_0'], axis = 1, inplace = True)
    dfs2['rates_y'] = dfs2['rates_y'].map('{:,.10f}'.format)
    dfs2['rates_x'] = dfs2['rates_x'].map('{:,.10f}'.format)


    ###############       Main dataframe with all data      ####################
    result = dfs2[(dfs2['valin_x'] == dfs2['valout_y'])]
    usdt = dfs2[(dfs2['valin_x'] == 'USD') & (dfs2['valout_y'] == 'USDT')]
    usd = dfs2[(dfs2['valin_x'] == 'USDT') & (dfs2['valout_y'] == 'USD')]
    final = result.append([usdt, usd])
    final.reset_index(inplace=True, drop = True)
    final.reset_index(level=0, inplace=True)
    filter = final[(final['birga_x'] == final['birga_y']) &
                   (final['rates_x'] < final['rates_y']) &
                   (final['valin_x'] == final['valout_y'])]
    final = final.drop(filter['index'], axis=0)

    t7 = time.time()
    print("ALL DATA  :", (t7 - t34))


    ########################      ADD  COMMISSION       ##############################

    var1 = final[final["valin_x"].isin(["USD", "USDT"])]
    var2 = final[final["valin_y"].isin(["USD", "USDT"])]
    var3 = final[(final["valin_x"] == "BTC") & (~final["valin_y"].isin(["USD", "USDT"]))]
    var4 = final[(final["valin_y"] == "BTC") & (~final["valin_x"].isin(["USD", "USDT"]))]
    var = {'var1': var1, 'var2': var2, 'var3': var3, 'var4': var4}



    def calc1(result):
        f = open(main_path_data + "\\commis.json")
        com = json.load(f)
        result.loc[:, 'start'] = "100"
        result.loc[:, "start"] = result["start"].str.replace(",", "").astype(float)
        result.loc[:, "rates_x"] = result["rates_x"].str.replace(",", "").astype(float)
        result.loc[:, "rates_y"] = result["rates_y"].str.replace(",", "").astype(float)
        result.loc[:, 'step'] = (result['start']) / ((result['rates_x'] * com['main'][result.iloc[0]['birga_x']]))
        result.loc[:, 'back'] = result['step'] * ((result['rates_y']) / com['main'][result.iloc[0]['birga_y']])
        result.loc[:, 'profit'] = result['back'] - result['start']
        result.loc[:, 'perc'] = (((result['profit']) / (result['start'])) * 100)
        f.close()
        return result


    def calc2(result):

        f = open(main_path_data + "\\commis.json")
        com = json.load(f)
        result.loc[:, 'start'] = "100"
        result.loc[:, "start"] = result["start"].str.replace(",", "").astype(float)
        result.loc[:, "rates_x"] = result["rates_x"].str.replace(",", "").astype(float)
        result.loc[:, "rates_y"] = result["rates_y"].str.replace(",", "").astype(float)
        result.loc[:, 'step'] = (result['start']) * ((result['rates_x'] / com['main'][result.iloc[0]['birga_x']]))
        result.loc[:, 'back'] = result['step'] / ((result['rates_y']) * com['main'][result.iloc[0]['birga_y']])
        result.loc[:, 'profit'] = result['back'] - result['start']
        result.loc[:, 'perc'] = (((result['profit']) / (result['start'])) * 100)
        f.close()
        return result


    dft = pd.DataFrame()
    for i, v in var.items():
        if v.shape[0] > 0:
            if i == 'var1' or i == 'var3':
                dft = dft.append(calc1(v))
            else:
                dft = dft.append(calc2(v))
    t8 = time.time()

    now = dt.datetime.now()
    dft.loc[:, 'TIME'] = now.strftime("%H:%M:%S")
    dft.drop(['index'], axis=1, inplace=True)
    dft = dft[['TIME', 'birga_x', 'birga_y', 'rates_x', 'rates_y','valin_x','valin_y','valout_y','volume_x','volume_y','start','step','back','profit','perc']]
    dfs = dft
    # dfs.to_csv(main_path_data + "\\MY_DATA.csv")
    f = open("my_tornado.json", "w")
    f.write(dictionary2)
    f.close()

    def wall_a():
        wallet_a = {}
        for k, v in dictionary.items():
            if 'api/v1/wallets' in f'**{k}**':
                Alfa = dictionary[k]
                for i in Alfa:
                    wallet_a.update({i['currency']: (float(i['balance']) - float(i['reserve']))})
            else:
                pass
        return wallet_a

    def wall_h():
        wallet_h = {}
        for k, v in dictionary.items():
            if 'balance.query' in f'**{k}**':
                Hot = dictionary[k]
                for i in Hot['result']:
                    wallet_h.update({i: Hot['result'][i]['available']})
            else:
                pass
        return wallet_h
    def wall_l():
        wallet_l = {}
        for k, v in dictionary.items():
            if 'payment/balances' in f'**{k}**':
                Live = dictionary[k]
                for i in Live:
                    if i['type'] == "available" and i['value'] > 0:
                        wallet_l.update({i['currency']: i['value']})
            else:
                pass
        return wallet_l

    Alfa2 = wall_a()
    Hot2 = wall_h()
    Live2 = wall_l()

    def balance():

        dfa = pd.DataFrame(Alfa2.items(), columns=['Valuta', 'alfa'])
        dfh = pd.DataFrame(Hot2.items(), columns=['Valuta', 'hot'])
        dfl = pd.DataFrame(Live2.items(), columns=['Valuta', 'live'])

        data_frames = [dfl, dfh, dfa]
        valuta = reduce(lambda left, right: pd.merge(left, right, on=['Valuta'],
                                                     how='outer'), data_frames).fillna('0')

        valuta['alfa'] = valuta['alfa'].apply(pd.to_numeric, errors='coerce')
        valuta['live'] = valuta['live'].apply(pd.to_numeric, errors='coerce')
        valuta['hot'] = valuta['hot'].apply(pd.to_numeric, errors='coerce')

        fil1 = valuta[valuta['Valuta'] == 'USD']
        fil2 = valuta[valuta['Valuta'] == 'USDT']

        al = (float(fil1.iloc[0]['alfa']) + float(fil2.iloc[0]['alfa']))
        li = (float(fil1.iloc[0]['live']) + float(fil2.iloc[0]['live']))
        ho = (float(fil1.iloc[0]['hot']) + float(fil2.iloc[0]['hot']))

        valuta = valuta.append({'Valuta': 'USDT + USD', 'alfa': al, 'live': li, 'hot': ho}, ignore_index=True)

        valuta.loc[:, "Summa"] = (valuta.loc[:, "alfa"] + valuta.loc[:, "live"] + valuta.loc[:, "hot"])
        valuta = valuta[['Valuta', 'alfa', 'live', 'hot', 'Summa']]
        valuta = valuta[(valuta['Summa'] != 0)]

        return valuta

    valuta_main = balance()
    valuta_main.to_csv(main_path_data + "\\balance.csv", index=False)

    t9 = time.time()
    print("Balances  :", (t9 - t8))


    def regim_filter():
        fids = pd.DataFrame()

        #################################      REGIMS      ##########################################

        if os.path.isfile(main_path_data + "\\regim.json"):
            f = open(main_path_data + "\\regim.json")
            regim = json.load(f)
            pass
        else:
            regim = {1: {"option": "off",
                         "avtomat": "off",
                         "val1": "",
                         "val2": "",
                         "val3": "",
                         "birga1": "",
                         "birga2": "",
                         "profit": "",
                         "order": "",
                         "per": ""}}
            ooo = json.dumps(regim, indent=4)
            # Writing to sample.json
            with open(main_path_data + "\\regim.json", "w") as outfile:
                outfile.write(ooo)
                outfile.close()
                pass

        dfs['volume_x'] = dfs['volume_x'].apply(pd.to_numeric, errors='coerce')
        dfs['volume_y'] = dfs['volume_y'].apply(pd.to_numeric, errors='coerce')

        for i in regim:
            if regim[i]["option"] == 'active':
                if not regim[i]["per"]:
                    dfs["volume_x"] = dfs["volume_x"].astype(float)
                    dfs["volume_y"] = dfs["volume_y"].astype(float)
                    filterx = dfs[dfs["volume_x"] < dfs["volume_y"]].index
                    dfs.loc[filterx, "volume"] = dfs.loc[filterx, "volume_x"]
                    filtery = dfs[dfs["volume_x"] > dfs["volume_y"]].index
                    dfs.loc[filtery, "volume"] = dfs.loc[filtery, "volume_y"]
                    dfs["volume"] = dfs["volume"].astype(float)

                    dft = dfs[(dfs["birga_x"] == regim[i]["birga1"]) &
                              (dfs["birga_y"] == regim[i]["birga2"]) &
                              (dfs["valin_x"] == regim[i]["val1"]) &
                              (dfs["valin_y"] == regim[i]["val2"]) &
                              (dfs["valout_y"] == regim[i]["val3"]) &
                              (dfs["perc"] > regim[i]["profit"]) &
                              (dfs["volume"] > float(regim[i]["order"]))]

                    if dft.shape[0] > 0:
                        dft = dft[dft['volume'] == dft['volume'].max()]
                        dft = dft.head(n=1)
                        dft["regim"] = i
                        if regim[i]["avtomat"] == 'on':
                            if fids.shape[0] > 0:
                                done = (time.process_time() - start11)
                                dft["timer"] = done

                                fids_b1 = fids[(fids['birga_x'] == dft.iloc[0]['birga_x']) & (fids['valin_x'] == dft.iloc[0]['valin_x']) & (fids['valin_y'] == dft.iloc[0]['valin_y'])]
                                fids_b11 = fids[(fids['birga_x'] == dft.iloc[0]['birga_y']) & (fids['valin_x'] == dft.iloc[0]['valin_y']) & (fids['valin_y'] == dft.iloc[0]['valout_y'])]
                                fids_b2 = fids[(fids['birga_y'] == dft.iloc[0]['birga_y']) & (fids['valin_x'] == dft.iloc[0]['valin_x']) & (fids['valin_y'] == dft.iloc[0]['valin_y'])]
                                fids_b22 = fids[(fids['birga_y'] == dft.iloc[0]['birga_x']) & (fids['valin_y'] == dft.iloc[0]['valin_x']) & (fids['valout_y'] == dft.iloc[0]['valin_y'])]

                                if fids_b1.shape[0] > 0:
                                    add_vol1 = float(fids_b1.iloc[0]['volume'])
                                else:
                                    add_vol1 = 0
                                if fids_b11.shape[0] > 0:
                                    add_vol11 = float(fids_b1.iloc[0]['volume'])
                                else:
                                    add_vol11 = 0
                                if fids_b2.shape[0] > 0:
                                    add_vol2 = float(fids_b1.iloc[0]['volume'])
                                else:
                                    add_vol2 = 0
                                if fids_b22.shape[0] > 0:
                                    add_vol22 = float(fids_b1.iloc[0]['volume'])
                                else:
                                    add_vol22 = 0

                                dft['volume'] = float(dft.iloc[0]['volume']) - add_vol1 - add_vol11 - add_vol2 - add_vol22
                                if dft.iloc[0]['volume'] > 0:
                                    valuta_new = pd.read_csv(main_path_data + "\\balance.csv")
                                    Avtomat.avtomat(dft, valuta_new, start11)
                                    fids = pd.concat([dft, fids], ignore_index=True, join='outer')
                                    continue
                                else:
                                    done = (time.process_time() - start11)
                                    dft["timer"] = done
                                    fids = pd.concat([dft, fids], ignore_index=True, join='outer')
                                    continue
                            else:
                                done = (time.process_time() - start11)
                                dft["timer"] = done
                                valuta_new = pd.read_csv(main_path_data + "\\balance.csv")
                                Avtomat.avtomat(dft, valuta_new, start11)
                                fids = pd.concat([dft, fids], ignore_index=True, join='outer')
                                continue
                        else:
                            done = (time.process_time() - start11)
                            dft["timer"] = done
                            fids = pd.concat([dft, fids], ignore_index=True, join='outer')
                            continue
                    else:
                        done = (time.process_time() - start11)
                        dft["timer"] = done
                        fids = pd.concat([dft, fids], ignore_index=True, join='outer')
                        continue
                else:
                    dfs["volume_x"] = dfs["volume_x"].astype(float)
                    dfs["volume_y"] = dfs["volume_y"].astype(float)
                    filterx = dfs[dfs["volume_x"] < dfs["volume_y"]].index
                    dfs.loc[filterx, "volume"] = dfs.loc[filterx, "volume_x"] * float(regim[i]["per"]) / 100
                    filtery = dfs[dfs["volume_x"] > dfs["volume_y"]].index
                    dfs.loc[filtery, "volume"] = dfs.loc[filtery, "volume_y"] * float(regim[i]["per"]) / 100
                    dfs["volume"] = dfs["volume"].astype(float)
                    dft = dfs[(dfs["birga_x"] == regim[i]["birga1"]) &
                              (dfs["birga_y"] == regim[i]["birga2"]) &
                              (dfs["valin_x"] == regim[i]["val1"]) &
                              (dfs["valin_y"] == regim[i]["val2"]) &
                              (dfs["valout_y"] == regim[i]["val3"]) &
                              (dfs["perc"] > regim[i]["profit"]) &
                              (dfs["volume"] > float(regim[i]["order"]))]

                    if dft.shape[0] > 0:
                        dft = dft[dft['volume'] == dft['volume'].max()]
                        dft = dft.head(n=1)
                        dft["regim"] = i
                        if regim[i]["avtomat"] == 'on':
                            if fids.shape[0] > 0:
                                done = (time.process_time() - start11)
                                dft["timer"] = done

                                fids_b1 = fids[(fids['birga_x'] == dft.iloc[0]['birga_x']) & (
                                            fids['valin_x'] == dft.iloc[0]['valin_x']) & (
                                                       fids['valin_y'] == dft.iloc[0]['valin_y'])]
                                fids_b11 = fids[(fids['birga_x'] == dft.iloc[0]['birga_y']) & (
                                            fids['valin_x'] == dft.iloc[0]['valin_y']) & (
                                                        fids['valin_y'] == dft.iloc[0]['valout_y'])]
                                fids_b2 = fids[(fids['birga_y'] == dft.iloc[0]['birga_y']) & (
                                            fids['valin_x'] == dft.iloc[0]['valin_x']) & (
                                                       fids['valin_y'] == dft.iloc[0]['valin_y'])]
                                fids_b22 = fids[(fids['birga_y'] == dft.iloc[0]['birga_x']) & (
                                            fids['valin_y'] == dft.iloc[0]['valin_x']) & (
                                                        fids['valout_y'] == dft.iloc[0]['valin_y'])]

                                if fids_b1.shape[0] > 0:
                                    add_vol1 = float(fids_b1.iloc[0]['volume'])
                                else:
                                    add_vol1 = 0
                                if fids_b11.shape[0] > 0:
                                    add_vol11 = float(fids_b11.iloc[0]['volume'])
                                else:
                                    add_vol11 = 0
                                if fids_b2.shape[0] > 0:
                                    add_vol2 = float(fids_b2.iloc[0]['volume'])
                                else:
                                    add_vol2 = 0
                                if fids_b22.shape[0] > 0:
                                    add_vol22 = float(fids_b22.iloc[0]['volume'])
                                else:
                                    add_vol22 = 0

                                dft['volume'] = float(dft['volume']) - add_vol1 - add_vol11 - add_vol2 - add_vol22
                                if dft.iloc[0]['volume'] > 0:
                                    valuta_new = pd.read_csv(main_path_data + "\\balance.csv")
                                    Avtomat.avtomat(dft, valuta_new, start11)
                                    fids = pd.concat([dft, fids], ignore_index=True, join='outer')
                                    continue
                                else:
                                    done = (time.process_time() - start11)
                                    dft["timer"] = done
                                    fids = pd.concat([dft, fids], ignore_index=True, join='outer')
                                    continue
                            else:
                                done = (time.process_time() - start11)
                                dft["timer"] = done
                                valuta_new = pd.read_csv(main_path_data + "\\balance.csv")
                                Avtomat.avtomat(dft, valuta_new, start11)
                                fids = pd.concat([dft, fids], ignore_index=True, join='outer')
                                continue
                        else:
                            done = (time.process_time() - start11)
                            dft["timer"] = done
                            fids = pd.concat([dft, fids], ignore_index=True, join='outer')
                            continue
                    else:
                        done = (time.process_time() - start11)
                        dft["timer"] = done
                        fids = pd.concat([dft, fids], ignore_index=True, join='outer')
                        continue
            else:
                pass
        return fids

    fdf = regim_filter()
    t10 = time.time()

    print("REGIMS  :",( t10 - t9))
    fdf.to_csv(main_path_data + "\\chains.csv", index=False)
    return


if __name__ == "__main__":
    def bot_sendtext(bot_message):
        ### Send text message
        bot_chatID = "494797976"
        bot_token = "1106019018:AAGboAxP5aa5_14IbSxxzLOz9PrbjkwALs8"
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
        requests.get(send_text)

        return

    while True:
        # try:
            # start_1 = time.process_time()
        t0 = time.time()
        print('##############################   START   ############################')
        restart()
        t1 = time.time()

        done = t1-t0
        # done = (time.process_time() - start_1)
        print('\n', f'##########################   {done}   ############################','\n')
        print('##########################   SLEEP TIME   ############################')
        time.sleep(0.1)
        # except Exception as e:
        #     now = dt.datetime.now()
        #     timer2 = now.strftime("%H:%M:%S")
        #     print('EXCEPTION :',e)
        #     nl = '\n'
        #     bot_sendtext(
        #         f" BIRGA EXCEPTION: {nl} {nl} {timer2} {nl} {e}")
        #     time.sleep(10.0)
