"""
    读写配置文件的信息
"""
from utils.io import yaml

class Config:

    def __init__(self, file='config/settings.yaml'):
        self.file = file
        self.config = yaml.read(self.file)

    def get_item(self, item):
        return self.config[item]

    def set_item(self, item, data):
        self.config[item] = data

    def save(self):
        yaml.write(self.file, self.config)


config = Config()
