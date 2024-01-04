from bs4 import BeautifulSoup
import requests, json
from datetime import datetime, timedelta
import time

def show_time():
    return time.strftime("%d/%m/%Y, %H:%M:%S", time.localtime())

print("Начало работы", show_time())

dic = {}
start_time = datetime(2020, 1, 1)
end_time = datetime(2023, 12, 31)
for delta in range((end_time - start_time).days + 1):
    data = (start_time + timedelta(days=delta))
    data_now = data.strftime("%Y-%m-%d")
    url = f'https://coincodex.com/historical-data/crypto/?date={data}T05:00:00Z'
    query = BeautifulSoup(requests.get(url=url).text, 'html.parser').findAll('script', id='coincodex-state')
    msg = json.loads(query[0].text)
    [dic.setdefault(data_now, msg[key]['data']['body']['coins']) for key in msg.keys() if 'get_historical_snapshot' in key]

    print(show_time(), "Скачано", data_now)
    ends = {"2020-12-31","2021-12-31","2022-12-31", "2023-12-31"}
    if data_now in ends:
        name = f"./data/data_{data_now}.json"
        print(show_time(), "Запись на диск")
        with open(name, 'a') as f:
            json.dump(dic, f, indent=4)
        dic.clear()

print(show_time(), "Конец работы")

