import os
from os.path import dirname, abspath

import yaml


def get_config():
    path = dirname(dirname(dirname(abspath(__file__))))
    with open(os.path.join(path, 'config.yaml')) as conf_file:
        config = yaml.load(conf_file.read())
    return config
