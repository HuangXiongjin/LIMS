import configparser
import os
import pymssql
import pymysql
#
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# CONFIG_DIR = os.path.join(BASE_DIR, 'config_db.ini')
# config = configparser.ConfigParser()
# config.read(CONFIG_DIR, encoding='utf-8')
#
# USERNAME = config['DATABASE']['USERNAME']
# PASSWORD = config['DATABASE']['PASSWORD']
# HOST = config['DATABASE']['HOST']
# PORT = config['DATABASE']['PORT']
# DB_NAME = config['DATABASE']['DB_NAME']
#
# REDIS_HOST = config['REDIS']['HOST']
#
# REDIS_TABLENAME = config['REDIS']['REDIS_TABLENAME']
# REDIS_PASSWORD = config['REDIS']['REDIS_PASSWORD']

# CONNECT_DATABASE = f"mssql+pymssql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}?charset=utf8"
CONNECT_DATABASE = f"mssql+pymssql://sa:Qcsw@758@192.168.2.4:1433/LIMS?charset=utf8"
# CONNECT_DATABASE = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}?charset=utf8"
# conn = pymssql.connect(user='sa', host='127.0.0.1', port='1433', password='1qaz2wsx', charset='utf8')
# conn = pymssql.connect(user='sa', host='192.168.7.100', port='1433', password='xea@123', charset='utf8')
