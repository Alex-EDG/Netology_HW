import requests
import logging
import json
from DiskException import DiskException
from Common import Config

class GoogleDriveClient:
    """
    According to the documentation for https://developers.google.com/drive/api/reference/rest/v3
    """
    _base_url = 'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart'

    logging.basicConfig(
                       level=logging.INFO,
                       filename='logs.log',
                       filemode='a',
                       format='[%(asctime)s] %(levelname)s - %(message)s'
                       )

    def __init__(self):
        config = Config('settings.ini')
        token = config.read_config()['googledrive']['access_token']
        self.base_headers = {'Authorization': 'Bearer ' + token}

    def create_folder(self, folder_name, folder_id=None):
        """
        :param folder_name: name of folder
        :param folder_id: id parent folder (new folder created in parent folder,
                          if 0 or None - new folder created in disk root)
        :return: id created folder
        """
        params = {
                 'name': folder_name,
                 'mimeType': 'application/vnd.google-apps.folder',
                 'parents': [folder_id],
                 'supportsAllDrives': True,
                 'allowFileDiscovery': True
                 }
        files = {'data': ('metadata', json.dumps(params), 'application/json; charset=UTF-8')}
        try:
            response = requests.post(self._base_url, headers=self.base_headers, files=files)
        except DiskException as exp:
            logging.info(exp)
            pass
        self._check_code(response)
        return response.json().get('id')

    def upload_file_from_url(self, file_name, from_url, folder_id=None):
        """
        Upload file from URL
        :param file_name: name of created file
        :param from_url: URL path from upload file
        :param folder_id: id parent folder (file created in parent folder,
                          if 0 or None - file created in disk root)
        :return: id created file
        """
        params = {
                 'name': file_name,
                 'parents': [folder_id]
                 }
        files = {
                'data': ('metadata', json.dumps(params), 'application/json; charset=UTF-8'),
                'file': requests.get(from_url).content
                }
        try:
            response = requests.post(self._base_url, headers=self.base_headers, files=files)
        except DiskException as exp:
            logging.info(exp)
            pass
        self._check_code(response)
        return response.json().get('id')

    def _check_code(self, req):
        if not str(req.status_code).startswith("2"):
            logging.warning(f'Ошибка операции: Status code:{req.status_code} - {req.json().get('error', {}).get('message')}')
            raise DiskException(req.status_code, req.text)