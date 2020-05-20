import Hot_parser
import Live_parser
import A_parser
import pandas as pd
from functools import reduce

##################################   SHOW ALL ROWS & COLS   ####################################
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', None)

##############################        BALANCE          #############################

def balance():
    Alfa = A_parser.wallet_a()
    Hot = Hot_parser.wallet_h()
    Live = Live_parser.wallet_l()

    dfa = pd.DataFrame(Alfa.items(), columns=['Valuta', 'alfa'])
    dfh = pd.DataFrame(Hot.items(), columns=['Valuta', 'hot'])
    dfl = pd.DataFrame(Live.items(), columns=['Valuta', 'live'])


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

    valuta.loc[:,"Summa"] = (valuta.loc[:,"alfa"] + valuta.loc[:,"live"] + valuta.loc[:,"hot"])
    valuta = valuta[['Valuta', 'alfa', 'live', 'hot', 'Summa']]
    valuta = valuta[(valuta['Summa'] != 0)]


    return valuta

# print(balance())