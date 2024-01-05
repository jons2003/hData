import numpy

import requests
import json, os
import pandas as pd
import scipy
from scipy.stats import pearsonr

# Константы для запроса
symbol = 'BTCUSDT'  # Торговая пара
interval, period = '30m', '30m'  # Интервал свечи (1 минута - '1m', 1 час - '1h', 1 день - '1d' и т.д.)
limit = 500 # Лимит количества свечей (максимум 1000)



# URL для запроса
url1 = f'https://fapi.binance.com/fapi/v1/indexPriceKlines?pair={symbol}&interval={interval}&limit={limit}'
url2 = f'https://fapi.binance.com/futures/data/topLongShortPositionRatio?symbol={symbol}&period={interval}&limit={limit}'

# Выполняем GET-запрос
response1 = requests.get(url1)
data1 = json.loads(response1.text)
df1 = pd.DataFrame(data1, columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Ignore', 'Close Time', 'x', 'x', 'x', 'x', 'x'])
# Преобразование типов данных
df1['Open Time'] = pd.to_datetime(df1['Open Time'], unit='ms')
df1['Open'] = pd.to_numeric(df1['Open'])
df1['High'] = pd.to_numeric(df1['High'])
df1['Low'] = pd.to_numeric(df1['Low'])
df1['Close'] = pd.to_numeric(df1['Close'])
df1['Close Time'] = pd.to_datetime(df1['Close Time'], unit='ms')

url2 = f'https://fapi.binance.com/futures/data/topLongShortPositionRatio?symbol={symbol}&period={interval}&limit={limit}'
response2 = requests.get(url2)
data2 = json.loads(response2.text)
df2 = pd.DataFrame(data2, columns=['symbol', 'longShortRatio', 'longAccount', 'shortAccount', 'timestamp'])
# Преобразование типов данных
df2['longShortRatio'] = pd.to_numeric(df2['longShortRatio'])
df2['longAccount'] = pd.to_numeric(df2['longAccount'])
df2['shortAccount'] = pd.to_numeric(df2['shortAccount'])
df2['timestamp'] = pd.to_datetime(df2['timestamp'], unit='ms')

data_array1 = numpy.array(df1).transpose()
# print(data_array1)

data_array2 = numpy.array(df2).transpose()
# print(data_array2)


# print(data_array2[1].astype(float) > data_array1[1].astype(float))
print(numpy.corrcoef(data_array2[1].astype(float), data_array1[1].astype(float)))

# возвращает коэффициент корреляции Пирсона вместе с двусторонним p-значением.
# Если значение меньше 0,05, мы можем заключить, что существует статистически значимая корреляция между двумя переменными.
print(pearsonr(data_array2[1].astype(float), data_array1[1].astype(float)))