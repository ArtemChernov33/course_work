import json
import time
import requests
from tqdm import tqdm
from pprint import pprint

class VK:

    def __init__(self, user_ids):
        self.token = ''
        self.user_ids = []
        self.foto = {}
        self.foto_new = {}
        self.info_photo = []
        self.file_name = []
        self.date = []
        self.url_foto = []
        self.max_size_photo = []

    def get_photo(self, count):
        URL_user = 'https://api.vk.com/method/users.get'
        URL_photo = 'https://api.vk.com/method/photos.get'
        params = {
            'user_ids': self.user_ids,
            'access_token': self.token,
            'v': '5.131',
        }
        res = requests.get(URL_user, params=params)
        items = res.json()['response']
        for id in items:
            id_user = id['id']
            params = {
                'owner_id': id_user,
                'access_token': self.token,
                'album_id': 'profile',
                'extended': 'likes',
                'photo_sizes': '1',
                'v': '5.131',
                'count': count
            }
        res = requests.get(URL_photo, params=params)
        res_photo = res.json()['response']['items']
        for photo in res_photo:
            self.date.append(photo['date'])
            likes = photo['likes']
            self.file_name.append(likes.get('count'))
            self.sizes = photo['sizes']

    def comparison_name(self):
        for count_i, i in enumerate(self.file_name):
            for count_t, t in enumerate(self.file_name):
                if str(i) == str(t):
                    if count_t != count_i:
                        self.file_name[count_i] = str(self.file_name[count_i]) + '_' + str(self.date[count_i])
        for u in self.sizes:
            self.url_foto = u['url']
        for a in self.file_name:
            self.foto[self.url_foto] = (f'{a}.jpg')
            pprint(self.foto)
        time.sleep(0.1)
    """Запись информации по фотографиям в файл json"""
    # with open('info.json', 'w') as outfile:
    #     outfile.write(f'{self.info_photo}\n')

class YD(VK):
    def __init__(self):
        self.tokenYD = ''
        self.foto = vk.foto
        #self.f = vk.foto
        self.download_YD = []
        pprint(self.foto)
    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.tokenYD)
        }
    def upload_file(self, path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        url_z = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
                   'Authorization': f'OAuth {self.tokenYD}'}
        c = 0
        """Создание папки.  path: Путь к создаваемой папке."""
        create = requests.put(f'{url}?path={path}', headers=headers).json()
        folder = create.get('method')
        if folder == 'GET':
            """Сохраняю фотографии в указанную папку. """
            for k, v in self.foto.items():

                params = {
                    "path": f'/{path}/{v}',
                    "url": k,
                    "overwrite": "true",
                }
                c += 1
                self.download_YD.append(c)
                for i in tqdm(self.download_YD):
                    time.sleep(0.5)
                res = requests.post(url=url_z, params=params, headers=headers).json()
        else:
            print('Такая папка существует, создайте другую папку')

if __name__ == '__main__':
    id_vk_user = input('Введите id пользователя: ')
    count = input('Введите кол-во фото для загрузки: ')
    path = input('Введите адрес для загрузки фотографий: ')
    vk = VK(id_vk_user)
    yd = YD()
    vk.get_photo(count)
    vk.comparison_name()
    yd.upload_file(path)
