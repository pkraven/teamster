import os
from os.path import dirname, abspath

import pytest
import psycopg2
import yaml


@pytest.fixture(scope='session')
def url_prefix():
    return "http://teamster:8080"


@pytest.fixture(scope='session')
def config():
    path = dirname(abspath(__file__))
    with open(os.path.join(path, 'config.yaml')) as conf_file:
        _config = yaml.load(conf_file.read())
    return _config


@pytest.fixture(scope='session')
def db(config):
    connect = psycopg2.connect(
        host=config['db']['host'],
        database=config['db']['database'],
        user=config['db']['user'],
        password=config['db']['password']
    )
    return connect


@pytest.fixture(autouse=True)
def clean_db(db):
    cur = db.cursor()
    cur.execute("TRUNCATE TABLE users, schedule;")
    db.commit()
    cur.close()
