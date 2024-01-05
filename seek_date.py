# Поиск недостающих данных в файле и догрузка с сайта

import json, requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

data_in = f'data_2020-2023.json'
data_out = f"./data_2020-2023.json_add.json"
start_time = datetime(2022, 1, 1)
end_time = datetime(2023, 12, 31)

 # Поиск
with open(data_in) as file:
    date = json.load(file)
print(len(date.keys()))

lst = []
for delta in range((end_time - start_time).days + 1):
    data = (start_time + timedelta(days=delta))
    data_str = data.strftime("%Y-%m-%d")
    if data_str not in date.keys():
        lst.append(data_str)
print(sorted(lst))

# Догрузка
dic = {}
for dates in lst:
    url =  f'https://coincodex.com/historical-data/crypto/?date={dates}T05:00:00Z'
    query = BeautifulSoup(requests.get(url).text, 'html.parser').findAll('script', id='coincodex-state')
    msg = json.loads(query[0].text)
    [dic.setdefault(dates, msg[key]['data']['body']['coins']) for key in msg.keys() if 'get_historical_snapshot' in key]

with open(data_out, 'a') as f:
    json.dump(dic, f, indent=4)

