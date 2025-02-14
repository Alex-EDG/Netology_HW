import requests
import logging
from DiskException import DiskException
from Common import Config

class VKClient:
    """
    According to the documentation for https://dev.vk.com/ru/reference
    """
    _base_url = 'https://api.vk.com/method'

    def __init__(self, user_id):
        """
        :param user_id: user_id of the VK user for whom the methods are applied
        """
        config = Config('settings.ini')
        self.token = config.read_config()['vk']['access_token']
        self.api_version = config.read_config()['vk']['API_version']
        self.user_id = user_id

    def get_common_params(self):
        """
        :return: params key ('access_token' and 'API version')
        """
        return {
               'access_token' : self.token,
               'v' : self.api_version
               }
    def _build_url(self, api_method):
        """
        :return: base url for request
        """
        return f'{self._base_url}/{api_method}?'

    def get_albums(self):
        """
        :return: json format of response for request method 'photos.getAlbums'
        """
        params = self.get_common_params()
        params.update({'owner_id': self.user_id})

        try:
            response = requests.get(self._build_url('photos.getAlbums'), params=params)
        except DiskException as exp:
            logging.info(exp)
            pass
        self._check_code(response)
        return response.json()

    def get_photos(self, album_id = 'profile'):
        """
        :return: json format of response for request method 'photos.get'
        """
        params = self.get_common_params()
        params.update({
            'owner_id': self.user_id,
            'album_id': f'{album_id}',
            'extended': 1,
            'photo_sizes': 1
            })
        try:
            response = requests.get(self._build_url('photos.get'), params=params)
        except DiskException as exp:
            logging.info(exp)
            pass
        self._check_code(response)
        return response.json()

    def _check_code(self, req):
        """
        :param req: json format of response for request method
        """
        if req.json().get('error') != None:
            logging.critical(f'Ошибка операции: Error code:{req.json().get('error', {}).get('error_code')} - {req.json().get('error', {}).get('error_msg')}')
            raise DiskException(req.status_code, req.text)