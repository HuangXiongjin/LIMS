import configparser
import os
import pymssql

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, 'config_db.ini')
config = configparser.ConfigParser()
config.read(CONFIG_DIR, encoding='utf-8')

USERNAME = config['DATABASE']['USERNAME']
PASSWORD = config['DATABASE']['PASSWORD']
HOST = config['DATABASE']['HOST']
PORT = config['DATABASE']['PORT']
DB_NAME = config['DATABASE']['DB_NAME']

CONNECT_DATABASE = f"mssql+pymssql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}?charset=utf8"

