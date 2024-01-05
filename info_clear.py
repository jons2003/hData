import json, time


data_in = f'data_2020-2023.json'

keys = ["price_change_1H_percent", "price_change_1D_percent", "price_change_7D_percent",  "price_change_30D_percent",
        "price_change_90D_percent", "price_change_180D_percent", "price_change_365D_percent",  "price_change_YTD_percent",
        "display", "last_update", "ico_end", "include_supply", "use_volume", "aliases",
        "price_change_1D_percent_BTC", "price_change_1D_percent_ETH", "price_change_7D_percent_BTC",
        "price_change_7D_percent_ETH", "price_change_30D_percent_BTC", "price_change_30D_percent_ETH"
        ]

start = time.time()
with open(data_in) as file:
    info = json.load(file)
for date in info.keys():
    for currency in info[date]:
        for key in keys:
                try: currency.pop(key)
                except KeyError:
                        print(f"{date}  {currency} не имеет аттрибута {key}")

dic_out = {}
for key in sorted(info):
    dic_out.setdefault(key, info[key])

print(time.time() - start)
with open('data.json', 'a') as f:
    json.dump(dic_out, f, indent=4)

print(time.time() - start)