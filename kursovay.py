import json
import time
import requests
from tqdm import tqdm
from pprint import pprint


#URL_id = 'https://api.vk.com/method/users.get'

with open('token.txt', 'r') as file_object:
    token = file_object.read().strip()

with open('tokenYD.txt', 'r') as file_object:
    tokenYD = file_object.read().strip()

def get_lagest(size_dict):
    if size_dict['width'] >= size_dict['height']:
        return size_dict['width']
    else:
        return size_dict['height']

def get_photo(user_name, count):
    URL_photo = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_id': user_name,
        'access_token': token,
        'album_id': 'profile',
        'extended': 'likes',
        'photo_sizes': '1',
        'v': '5.131',
        'count': count
    }
    foto = {}
    res = requests.get(URL_photo, params=params)
    res_photo = res.json()['response']['items']
    info_photo = []
    for photo in res_photo:
        date = photo['date']
        likes = photo['likes']
        file_name = likes.get('count')
        sizes = photo['sizes']
        max_size_url = max(sizes, key=get_lagest)['url']
        max_size_photo = max(sizes, key=get_lagest)['type']
        time.sleep(0.1)
        foto[max_size_url] = (f'{file_name}.jpg', date)
        info_photo.append({'file_name': f'{file_name}.jpg', 'size': max_size_photo})

    """Запись информации по фотографиям в файл json"""
    with open('info.json', 'w') as outfile:
        outfile.write(f'{info_photo}\n')
    return foto
q = get_photo('2526736', '3')
#pprint(q)

def get_headers():
    return {
        'Content-Type': 'application/json',
        'Authorization': 'OAuth {}'.format(tokenYD)
    }

def upload_file(path):
    url = 'https://cloud-api.yandex.net/v1/disk/resources/'
    url_z = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {tokenYD}'}
    download_YD = []
    c = 0
    """Создание папки.  path: Путь к создаваемой папке."""
    create = requests.put(f'{url}?path={path}', headers=headers).json()
    folder = create.get('method')
    if folder == 'GET':
        """Сохраняю фотографии в указанную папку. """
        for k, v in q.items():
            name = v[0]
            params = {
            "path": f'/{path}/{name}',
            "url": k,
            "overwrite": "true",
            }
            c += 1
            download_YD.append(c)
            for i in tqdm(download_YD):
                time.sleep(0.5)
            res = requests.post(url=url_z, params=params, headers=headers).json()
    else:
        print('Такая папка существует, создайте другую папку')

if __name__ == '__main__':
    get_photo('2526736', '3')
    upload_file('77')
