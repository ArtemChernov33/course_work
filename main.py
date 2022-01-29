import json
import time
import requests
import yadisk
from tqdm import tqdm
import os
from datetime import datetime
from pprint import pprint

y = yadisk.YaDisk(token="")
URL_id = 'https://api.vk.com/method/users.get'
URL_photo = 'https://api.vk.com/method/photos.get'

with open('token.txt', 'r') as file_object:
    token = file_object.read().strip()

def get_lagest(size_dict):
    if size_dict['width'] >= size_dict['height']:
        return size_dict['width']
    else:
        return size_dict['height']

def get_photo():
    params = {
        'owner_id': '2526736',
        'access_token': token,
        'album_id' : 'profile',
        'extended' : 'likes',
        'photo_sizes' : '1',
        'v':'5.131'
    }
    foto = {}
    res = requests.get(URL_photo, params=params)
    res_photo = res.json()['response']['items']
    PC_download = []
    q = 0
    info_photo = []
    for photo in res_photo:
        date = photo['date']
        likes = photo['likes']
        file_name = likes.get('count')
        sizes = photo['sizes']
        max_size_url = max(sizes, key=get_lagest)['url']
        max_size_photo = max(sizes, key=get_lagest)['type']
        time.sleep(0.1)
        foto[max_size_url] = (file_name, date)
        info_photo.append({'file_name': f'{file_name}.jpg', 'size':max_size_photo})

#Запись информации по фотографиям в файл json
    with open('info.json', 'w') as outfile:
        outfile.write(f'{info_photo}\n')

# Сохранение фотографий на компьютер и создание прогресс-бар для сохранения
    #print('Загрузка файлов на компьютер:')
    for k, v in foto.items():
        api = requests.get(k)
        name_foto = v[0]
        q += 1
        PC_download.append(q)

        with open(f'{name_foto}.jpg', 'bw') as file:

            for i in tqdm(PC_download):
                time.sleep(0.5)
            file.write(api.content)


#Сохранение фотографий на Яндекс Диск и создание прогресс-бара для загрузки
def load(path):
    download_YD = []
    c = 0
    date = datetime.strftime(datetime.now(), "%d.%m.%Y-%H.%M.%S")
    y.mkdir(f'/test/{date}')
    p = os.getcwd()
    #print('Загрузка файлов на яндекс диск:')
    for file in os.listdir():
        if file.endswith('.jpg'):
            c += 1
            download_YD.append(c)
            for i in tqdm(download_YD):
                time.sleep(0.5)
            #print(f'Файл {file} загружен')
            y.upload(f'{p}/{file}', f'/test/{date}/{file}')


if __name__ == '__main__':
    get_photo()
    load(os.getcwd())


