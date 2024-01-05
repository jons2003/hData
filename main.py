import time, urllib, hmac, hashlib, requests, json
from urllib.parse import urlparse
import pandas as pd
import numpy as nm
from scipy.stats import pearsonr
from datetime import  datetime, timedelta
import matplotlib.pyplot as plt

class queryBinance:
    methods = {
        # public methods
        'indexPriceKlines': {'url': 'fapi/v1/indexPriceKlines',
                             'params': {'pair': None, 'interval': None, 'startTime': None, 'endTime': None, 'limit': 1500},
                             'data': ['Open Time', 'Open', 'High', 'Low', 'Close', 'Ignore', 'Close Time', 'x0', 'x1', 'x2', 'x3', 'x4'],
                             'private': False},
        'topLongShortPositionRatio': {'url': 'futures/data/topLongShortPositionRatio',
                             'params': {'symbol': None, 'period': None, 'startTime': None, 'endTime': None,'limit': 500},
                             'data': ['symbol', 'longShortRatio', 'longAccount', 'shortAccount', 'timestamp'],
                             'private': False},
              }

    def __init__(self, API_KEY, API_SECRET, API_URL):
        self.API_KEY = API_KEY
        self.API_SECRET = bytearray(API_SECRET, encoding='utf-8')
        self.API_URL = API_URL

    def __getattr__(self, name):
        def wrapper(**kwargs):
            kwargs.update(command=name)
            return self.call_api(**kwargs)
        return wrapper

    def _params_check(self, command, parameters):
        for param in queryBinance.methods[command]['params'].keys():
            if queryBinance.methods[command]['params'][param] \
                and queryBinance.methods[command]['params'][param] < parameters[param]:
                raise ValueError(f"Параметр '{param}' запроса '{command}' превышает допустимое значение {queryBinance.methods[command]['params'][param]}")

    def _convert_data(self, date):
        format = '%d/%m/%y %H:%M'
        if 'startTime' in date.keys():
            a = date['startTime']
            startTime = int((datetime(a[2], a[1], a[0], a[3], a[4]) + timedelta(hours=7)).timestamp()*1000)
            date['startTime'] = startTime
        if 'endTime' in date.keys():
            a = date['endTime']
            endTime = int((datetime(a[2], a[1], a[0], a[3], a[4]) + timedelta(hours=7)).timestamp()*1000)
            date['endTime'] = endTime
        return date

    def call_api(self, **kwargs):
        headers = {}
        command = kwargs.pop('command')
        self._params_check(command, kwargs)
        base_url = self.API_URL
        api_url = base_url + self.methods[command]['url']
        payload = kwargs
        print(payload)
        payload = self._convert_data(payload)
        print(payload)
        payload_str = urllib.parse.urlencode(payload)

        if self.methods[command]['private']:
            payload.update({'timestamp': int(time.time() + self.shift_seconds - 1) * 1000})
            payload_str = urllib.parse.urlencode(payload).encode('utf-8')
            sign = hmac.new(key=self.API_SECRET, msg=payload_str, digestmod=hashlib.sha256).hexdigest()
            payload_str = payload_str.decode("utf-8") + "&signature=" + str(sign)
            headers = {"X-MBX-APIKEY": self.API_KEY, "Content-Type": "application/x-www-form-urlencoded"}
        else:
            api_url += '?' + payload_str
            print(api_url)
        response = requests.request(method='GET', url=api_url, headers=headers)
        if 'code' in response.text:
            print(f'Неудачная попытка выставить ордер: {response.text}')

        dates = queryBinance.methods[command]['data']
        df = pd.DataFrame(json.loads(response.text), columns=dates)
        for date in dates:
            if 'time' in date or 'Time' in date:
                df[date] = pd.to_datetime(df[date], unit='ms')
            elif date != 'symbol'  and date != 'pair':
                df[date] = pd.to_numeric(df[date])
        return nm.array(df).transpose()

bot = queryBinance(API_KEY='',
                   API_SECRET='',
                   API_URL='https://fapi.binance.com/')


arr1 = bot.indexPriceKlines(pair='BTCUSDT', interval='1h',limit=3, startTime=(20,12,2023,10,00), endTime=(22,12,2023,10,00))

arr2 = bot.topLongShortPositionRatio(symbol='BTCUSDT', period='1h',limit=3, startTime=(20,12,2023,10,00), endTime=(22,12,2023,10,00))
print(nm.corrcoef(arr1[1].astype(float), arr2[1].astype(float)))
print(pearsonr(arr1[1].astype(float), arr2[1].astype(float)))
# возвращает коэффициент корреляции Пирсона вместе с двусторонним p-значением.
# Если значение меньше 0,05, мы можем заключить, что существует статистически значимая корреляция между двумя переменными.
print(arr1, arr2)
# y1, y2 = arr2[1], arr1[1]
# x = arr1[0]
#
# # plotting the points
# plt.plot(x, y1)
# plt.plot(x, y2)
# # naming the x axis
# plt.xlabel('x - axis')
# # naming the y axis
# plt.ylabel('y - axis')
#
# # giving a title to my graph
# plt.title('My first graph!')
#
# # function to show the plot
# plt.show()