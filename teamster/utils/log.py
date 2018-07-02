import os
from os.path import dirname, abspath
import logging
import logging.config

import yaml


def set_logger_config():
    path = dirname(dirname(dirname(abspath(__file__))))
    with open(os.path.join(path, 'logging_config.yaml')) as f:
        _config = yaml.load(f.read())
    logging.config.dictConfig(_config)
