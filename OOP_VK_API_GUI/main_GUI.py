from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import json
from tqdm import tqdm
import logging

from  VKClient import VKClient
from  YandexDiskClient import YandexDiskClient
from  GoogleDriveClient import GoogleDriveClient

class BackupPhotoToCloud:
    def __init__(self):
        self.vk_client = VKClient(user_id_tf.get())
        self.yd_client = YandexDiskClient()
        self.gd_client = GoogleDriveClient()

    def get_upload_photo_list(self, album_id):
        """
        :param album_id: album_id for VK user -> str
        :return: photos_to_filename_list [{
                                        'file_name': 'number of likes(_UNIX date).jpg',
                                        'size': 'z',
                                        'url_photo': url
                                      }]
        """
        photos_to_filename_list = []

        logging.info(f'Получение списка фото VK пользователя user_id={user_id_tf.get()} из album_id={album_id_tf.get()}')

        for photo in self.vk_client.get_photos(album_id)['response']['items']:
            file_name = f'{photo['likes']['count']}.jpg'
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
        logging.info(f'Обнаружено {len(photos_to_filename_list)} фото из альбома album_id={album_id_tf.get()} VK пользователя user_id={user_id_tf.get()}')
        return photos_to_filename_list

    def upload_photo_to_cloud(self, filename_list, cloud_id):
        """
        :param: filename_list: [{
                               'file_name': 'number of likes(_UNIX date).jpg',
                               'size': 'z',
                               'url_photo': url
                                }]
        :param: cloud_id: name of Cloud Service -> str
        """
        if cloud_id == 'Yandex Disk':
            yd_client = YandexDiskClient()
            yd_client.create_folder('VK_Photos')
            yd_client.create_folder(f'VK_Photos/user_id{user_id_tf.get()}')
            for photo in tqdm(filename_list):
                yd_client.upload_file_from_url(
                                               photo['file_name'],
                                               photo['url_photo'],
                                       f'VK_Photos/user_id{user_id_tf.get()}'
                                              )
        elif cloud_id == 'Google Drive':
            gd_client = GoogleDriveClient()
            vk_folder_id = gd_client.create_folder(
                                       'VK_Photos',
                                          'root'
                                                  )
            vk_user_id_folder_id = gd_client.create_folder(
                                               f'user_id{user_id_tf.get()}',
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
       :param: filename_list: [{
                              'file_name': 'number of likes(_UNIX date).jpg',
                              'size': 'z',
                              'url_photo': url
                              }]
       :return: write file result.json = [{
                                       'file_name': number of likes +/- '_UNIX date'.jpg',
                                       'size': 'z'
                                        }]
        """
       result_list = [{'file_name': photo['file_name'], 'size': photo['size']} for photo in filename_list]
       with open('result.json', 'w', encoding='utf-8') as f:
           json.dump(result_list, f, ensure_ascii=False, indent=2)

def select():
    header.config(text=f"Выбран {cloud_id.get()}")

def start_main_code():

    logging.basicConfig(
                        level=logging.INFO,
                        filename='logs.log',
                        filemode='a',
                        format='[%(asctime)s] %(levelname)s - %(message)s'
                       )

    backup_to_cloud = BackupPhotoToCloud()
    file_list = backup_to_cloud.get_upload_photo_list(album_id_tf.get())
    backup_to_cloud.upload_photo_to_cloud(file_list, cloud_id.get())
    backup_to_cloud.create_result_file(file_list)

    messagebox.showinfo(f'Копирование на {cloud_id.get()}',
                     f'Скопировано на {cloud_id.get()}\n'
                             f'из альбома album_id{album_id_tf.get()}\n'
                             f'VK пользователя user_id{user_id_tf.get()}\n'
                             f'Информация о файлах в Result.json\n'
                             f'Логирование процесса в Logs.log')

window = Tk()
window.title('Backup VK user photo to Cloud storage')
window.geometry('450x200')

clouds = ["Yandex Disk", "Google Drive"]
cloud_id = StringVar(value=clouds[0])  # по умолчанию выбран Yandex Disk

for i, c in enumerate(clouds):
    cloud_btn = ttk.Radiobutton(
                               text=c,
                               value=c,
                               variable=cloud_id,
                               command=select
                               )
    cloud_btn.grid(
                  row=3 + i,
                  column=0,
                  sticky='w'
                  )

header = ttk.Label(
                  text="Выберите Cloud Service",
                  justify="left"
                  )
header.grid(row=3, column=1)

user_id_lb = Label(
                  text="Введите VK user_id=(натуральное число)",
                  justify="left"
                  )
user_id_lb.grid(row=6, column=1)
user_id_tf = Entry()
user_id_tf.grid(row=6, column=0, padx=1)

album_id_lb = Label(
                   text="Введите album_id=(натуральное число)\n0 - использовать profile",
                   justify="left"
                   )
album_id_lb.grid(row=7, column=1)
album_id_tf = Entry()
album_id_tf.grid(row=7, column=0)
album_id_tf.insert(0, "0")

params = Label(
              text=f'Выбрано копирования из альбома album_id{album_id_tf.get()}\n'
                   f'VK пользователя user_id{user_id_tf.get()}',
              justify="left",
              foreground="#03A010"
              )
params.grid(row=8, column=1)

copy_btn = Button(
                  text=f'Начать',
                  command=start_main_code
                  )
copy_btn.grid(row=9, column=1)

window.mainloop()