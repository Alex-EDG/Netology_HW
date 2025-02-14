import json
import sys

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

        logging.basicConfig(
            level=logging.INFO,
            filename='logs.log',
            filemode='a',
            format='[%(asctime)s] %(levelname)s - %(message)s'
            )

    def get_upload_photo_list(self, albm_id, usr_id):
        """
        :return: photos filename list {'number of likes +/-_UNIX time': {'size': 'z', 'url_photo': url}}
        """
        photos_to_filename_list = {}

        logging.info(f'Получение списка фото VK пользователя user_id={usr_id} из album_id={albm_id}')

        p_items = self.vk_client.get_photos(albm_id)

        for photo in p_items['response']['items']:
            file_name = f'{photo['likes']['count']}'
            max_photo_size = max(photo['sizes'], key=lambda x: x.get('height') * x.get('width'))

            if file_name not in photos_to_filename_list.keys():
                photos_to_filename_list.update({
                    f'{file_name}': {'size': f'{max_photo_size['type']}', 'url_photo': f'{max_photo_size['url']}'}
                    })
            else:
                photos_to_filename_list.update({
                    f'{file_name}_{photo['date']}': {'size': f'{max_photo_size['type']}', 'url_photo': f'{max_photo_size['url']}'}
                    })
        logging.info(f'Обнаружено {len(photos_to_filename_list)} фото из альбома album_id={albm_id} VK пользователя user_id={usr_id}')
        return photos_to_filename_list

    def upload_photo_to_cloud(self, filename_list, usr_id):
        """
        :return: result_lst = [{'file_name': 'number of likes +/- _UNIX time'.jpg', 'size': 'z'}]
        """
        while True:
            cloud_name = f'{input(f'Выбрать куда сохранять фото:\nY(y) - Yandex Disk\nG(g) - Google Drive\n\n?').upper()}D'
            if cloud_name not in ['YD', 'GD']:
                continue
            else:
                break
        result_lst = []

        if cloud_name == 'YD':
            cld_name = 'Yandex Disk'
            yd_client = YandexDiskClient()
            yd_client.create_folder('VK_Photos')
            yd_client.create_folder(f'VK_Photos/user_id{usr_id}')

            for file_name, photo_atrib in tqdm(filename_list.items()):
                yd_client.upload_file_from_url(file_name + '.jpg', photo_atrib['url_photo'], f'VK_Photos/user_id{usr_id}')
                result_lst.append({'file_name': file_name + '.jpg', 'size': photo_atrib['size']})

        elif cloud_name == 'GD':
            cld_name = 'Google Drive'
            gd_client = GoogleDriveClient()
            vk_folder_id = gd_client.create_folder('VK_Photos', 'root')
            vk_user_id_folder_id = gd_client.create_folder(f'user_id{usr_id}', f'{vk_folder_id}')

            for file_name, photo_atrib in tqdm(filename_list.items()):
                gd_client.upload_file_from_url(file_name + '.jpg', photo_atrib['url_photo'], f'{vk_user_id_folder_id}')
                result_lst.append({'file_name': file_name + '.jpg', 'size': photo_atrib['size']})

        logging.info(f'На {cld_name} скопировано {len(result_lst)} фото VK пользователя user_id={usr_id}')

        return result_lst

    def create_result_file(self, filename_list):
        """
        :return: write file result.json = [{
                                           'file_name': 'number of likes +/- _UNIX time'.jpg',
                                           'size': 'z'
                                          }]
        """
        with open('result.json', 'w', encoding='utf-8') as f:
            json.dump(filename_list, f, ensure_ascii=False, indent=2)

def select_vk_user_id():
    """
    :return: vk_user_id -> str
    """
    while True:
        try:
            vk_user_id = int(input('Введите числовой id пользователя VK, фото которого необходимо сохранить:\n?'))
        except ValueError:
            print('Неверный ввод, должно быть число')
            continue
        else:
            break
    return vk_user_id

def select_vk_album_id():
    """
    :return: vk_album_id -> str
    """
    while True:
        try:
            vk_album_id = int(input('Введите числовой album_id пользователя VK,'
                                    'фото из которого необходимо сохранить (0 - фото профиля):\n?'))
            if vk_album_id == 0:
                vk_album_id = 'profile'
            else:
                vk_album_id = str(vk_album_id)
        except ValueError as ve:
            print(f'{str(ve)} - Неверный ввод, должно быть число')
            sys.exit()
        else:
            break
    return vk_album_id

if __name__ == '__main__':

    user_id = select_vk_user_id()
    album_id = select_vk_album_id()

    backup_to_cloud = BackupPhotoToCloud()
    filename_lst = backup_to_cloud.get_upload_photo_list(album_id, user_id)
    result_list = backup_to_cloud.upload_photo_to_cloud(filename_lst, user_id)
    backup_to_cloud.create_result_file(result_list)