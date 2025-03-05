import configparser

class Config:

    def __init__(self, config_file):
        """
        :param config_file: filename for reading program settings
        """
        self.config_file = config_file

    def read_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)
        return config