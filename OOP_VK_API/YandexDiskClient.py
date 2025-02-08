import requests
import logging
from DiskException import DiskException
from Common import Config

class YandexDiskClient:
    """
    According to the documentation for https://tech.yandex.ru/disk/poligon/
    """
    _base_url = 'https://cloud-api.yandex.net:443/v1/disk'

    logging.basicConfig(
                        level=logging.INFO,
                        filename='logs.log',
                        filemode='a',
                        format='[%(asctime)s] %(levelname)s - %(message)s'
                        )

    def __init__(self):
        config = Config('settings.ini')
        token = config.read_config()['yandexdisk']['access_token']
        self.base_headers = {
                             'Accept': 'application/json',
                             'Authorization': 'OAuth ' + token,
                             'Host': 'cloud-api.yandex.net'
                             }

    def create_folder(self, path_to_folder):
        """
        :param path_to_folder: path to folder
        :return: created folder
        """
        url = self._base_url + '/resources'
        payload = {'path': path_to_folder}
        try:
            response = requests.put(url, headers=self.base_headers, params=payload)
        except DiskException as exp:
            logging.info(exp)
            pass
        self._check_code(response)

    def upload_file_from_url(self, file_name, from_url, path_to):
        """
        Upload file from URL
        :param file_name: name of created file
        :param from_url: URL path from upload file
        :param path_to: path to yandex disk
        """
        url = self._base_url + '/resources/upload'
        payload = {'path': f'{path_to}/{file_name}', 'url': from_url}
        try:
            response = requests.post(url, headers=self.base_headers, params=payload)
        except DiskException as exp:
            logging.info(exp)
            pass
        self._check_code(response)

    def _check_code(self, req):
        if not str(req.status_code).startswith('2'):
            if req.json().get('error') =='DiskPathPointsToExistentDirectoryError':
                logging.warning(f'Ошибка операции: Status code:{req.status_code} - {req.json().get('message')}')
            else:
                logging.critical(f'Ошибка операции: Status code:{req.status_code} - {req.json().get('message')}')
                raise DiskException(req.status_code, req.text)