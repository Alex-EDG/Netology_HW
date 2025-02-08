import json
from tqdm import tqdm
import logging

from  VKClient import VKClient
from  YandexDiskClient import YandexDiskClient
from  GoogleDriveClient import GoogleDriveClient

class BackupPhotoToCloud:
    def __init__(self):
        self.vk_client = VKClient(user_id)
        self.yd_client = YandexDiskClient()
        self.gd_client = GoogleDriveClient()

    def get_upload_photo_list(self, album_id):
        """
        :return: photos filename list [{
                                        'file_name': number of likes(_UNIX date).jpg',
                                        'size': 'z',
                                        'url_photo': url
                                      }]
        """
        photos_to_filename_list = []

        logging.info(f'Получение списка фото VK пользователя user_id={user_id} из album_id={album_id}')

        for photo in self.vk_client.get_photos(album_id)['response']['items']:
            file_name = f'{photo['likes']['count']}.jpg'
            temp_dict = {}
            for size in photo['sizes']:
                if size['type'] == 'z':
                    url = f'{size['url']}'
                    temp_dict = {'file_name': f'{photo['likes']['count']}.jpg',
                                 'size': 'z',
                                 'url_photo': url
                                 }
                    if file_name not in [item.get('file_name') for item in photos_to_filename_list]:
                        photos_to_filename_list.append(temp_dict)
                    else:
                        photos_to_filename_list.append({'file_name': f'{photo['likes']['count']}_{photo['date']}.jpg',
                                                        'size': 'z',
                                                        'url_photo': url
                                                        })
        logging.info(f'Обнаружено {len(photos_to_filename_list)} фото из альбома album_id={album_id} VK пользователя user_id={user_id}')
        return photos_to_filename_list

    def upload_photo_to_cloud(self, filename_list):

        while True:
            cloud_name = f'{input(f'Выбрать куда сохранять фото:\nY(y) - Yandex Disk\nG(g) - Google Drive\n\n?').upper()}D'
            if cloud_name not in ['YD', 'GD']:
                continue
            else:
                break
        if cloud_name == 'YD':
            yd_client = YandexDiskClient()
            yd_client.create_folder('VK_Photos')
            yd_client.create_folder(f'VK_Photos/user_id{user_id}')
            for photo in tqdm(filename_list):
                yd_client.upload_file_from_url(
                                               photo['file_name'],
                                               photo['url_photo'],
                                       f'VK_Photos/user_id{user_id}'
                                              )
        elif cloud_name == 'GD':
            gd_client = GoogleDriveClient()
            vk_folder_id = gd_client.create_folder(
                                          'VK_Photos',
                                             'root'
                                                     )
            vk_user_id_folder_id = gd_client.create_folder(
                                                   f'user_id{user_id}',
                                                     f'{vk_folder_id}'
                                                              )
            for photo in tqdm(filename_list):
                gd_client.upload_file_from_url(
                                               photo['file_name'],
                                               photo['url_photo'],
                                       f'{vk_user_id_folder_id}'
                                               )

    def create_result_file(self, filename_list):
        """
        :return: write file result.json = [{
                                           'file_name': number of likes +/- '_UNIX date'.jpg',
                                           'size': 'z'
                                          }]
        """
        result_list = [{'file_name': photo['file_name'], 'size': photo['size']} for photo in filename_list]
        with open('result.json', 'w', encoding='utf-8') as f:
            json.dump(result_list, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':

    logging.basicConfig(
                        level=logging.INFO,
                        filename='logs.log',
                        filemode='a',
                        format='[%(asctime)s] %(levelname)s - %(message)s'
                       )

    while True:
        try:
            user_id = int(input('Введите числовой id пользователя VK, фото которого необходимо сохранить:\n?'))
        except ValueError:
            print('Неверный ввод, должно быть число')
            continue
        else:
            break

    while True:
        try:
            album_id = int(input('Введите числовой album_id пользователя VK, фото из которого необходимо сохранить (0 - фото профиля):\n?'))
            if album_id == 0:
                album_id = 'profile'
            else:
                album_id = str(album_id)
        except ValueError:
            print('Неверный ввод, должно быть число')
            continue
        else:
            break

    backup_to_cloud = BackupPhotoToCloud()
    filename_list = backup_to_cloud.get_upload_photo_list(album_id)
    backup_to_cloud.upload_photo_to_cloud(filename_list)
    backup_to_cloud.create_result_file(filename_list)