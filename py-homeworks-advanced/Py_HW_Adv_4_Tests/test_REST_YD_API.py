import configparser
import pytest
import requests
import yadisk

# 2 часть домашнего задания
class TestYDCreateFolder:
    def setup_method(self) -> None:
        config = configparser.ConfigParser()
        config.read('settings.ini')
        self.yd_token = 'OAuth ' + config['yandexdisk']['access_token']
        self.headers = {'Accept': 'application/json',
                        'Authorization': self.yd_token,
                        'Host': 'cloud-api.yandex.net'}
        self._base_url = 'https://cloud-api.yandex.net:443/v1/disk/resources'
        yd = yadisk.YaDisk(token=self.yd_token)
        self.test_folder_name = 'TestFolder'
        i = 0
        while yd.exists(f'/{self.test_folder_name}/'):
            i += 1
            self.test_folder_name = 'TestFolder' + f'({i})'
        self.test_data = (('path', self.test_folder_name, 201),
                          ('path', self.test_folder_name, 409),
                          ('pathh', self.test_folder_name, 400))

    def teardown_method(self):
        params = {'path': self.test_folder_name}
        requests.delete(self._base_url,
                        params=params,
                        headers=self.headers)

    def test_create_folder(self):
        for param in self.test_data:
            params = {param[0]: param[1]}
            response = requests.put(self._base_url,
                                    params=params,
                                    headers=self.headers)
            assert response.status_code == param[2]
        params2 = {'path': self.test_folder_name}
        response = requests.get(self._base_url + '/download',
                                params=params2,
                                headers=self.headers)
        assert response.status_code == 200

    @pytest.mark.xfail
    def test_folder_exist2 (self):
        params = {'path': self.test_folder_name + '_'}
        response = requests.get(self._base_url + '/download',
                                 params=params,
                                 headers=self.headers)
        assert response.status_code == 200

if __name__ == '__main__':

    test_yd_api = TestYDCreateFolder()
    test_yd_api.test_create_folder()
    test_yd_api.test_folder_exist2()