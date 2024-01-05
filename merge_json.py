# Слияние json-файлов
import json

# Пути к сливаемым json-файлам
paths = ['data_2020-2021.json', 'data_2022-2023.json']

def merge_json_files(file_paths):
    dic = {}
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file_in:
            dic.update(json.load(file_in))
    with open('data_2020-2023.json', 'w', encoding='utf-8') as file_out:
        json.dump(dic, file_out, indent=4)

merge_json_files(paths)
