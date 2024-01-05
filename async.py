# Асинхронный запрос исторических торговых данных с https://coincodex.com

import asyncio, aiohttp,json, time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

class Async:
  Storage ={}

  def __init__(self):
    self.start_time = datetime(2022, 1, 1)
    self.end_time = datetime(2023, 12, 31)
    self.f_name = f"./data_2022-2023.json"
    self.url = f'https://coincodex.com/historical-data/crypto/?date='

  @staticmethod
  def show_time():
    return time.strftime("%d/%m/%Y, %H:%M:%S", time.localtime())

  async def async_scrape(self, session, url, data_str):
    async with session.get(url) as response:
      html = await response.text()
      print(data_str, response.status)
      query = BeautifulSoup(html, 'html.parser').findAll('script', id='coincodex-state')
      msg = json.loads(query[0].text)
      [Async.Storage.setdefault(data_str, msg[key]['data']['body']['coins']) for key in msg.keys() if 'get_historical_snapshot' in key]

  async def main(self):
    async with aiohttp.ClientSession() as session:
      print(self.show_time(), "Начало работы")
      tasks = []

      for delta in range((self.end_time - self.start_time).days + 1):
        data = (self.start_time + timedelta(days=delta))
        data_str = data.strftime("%Y-%m-%d")
        url = self.url + f'{data_str}T05:00:00Z'
        tasks.append(self.async_scrape(session, url, data_str))

      print(self.show_time(), "Старт отправки запросов серверу")
      try:
        await asyncio.gather(*tasks)
      except aiohttp.ClientError as err:
        print(err)
        await asyncio.sleep(120)

      print(self.show_time(), "Старт записи в файл")
      with open(self.f_name, 'a') as f:
        json.dump(Async.Storage, f, indent=4)
      print(self.show_time(), "Конец записи в файл")

sample = Async()
asyncio.run(sample.main())



