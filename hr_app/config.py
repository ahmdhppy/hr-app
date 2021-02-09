"""
Configuration File

"""
import os
DEBUG = False
FILE_STORE_METHOD = 'local'
FILE_STORE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),'files')
LOG_FILE = '/var/log/flask-hr-app.log'
SECRET_KEY = '123xzz'
ACCESS_KEY_AWS = ''
SECRET_KEY_AWS = ''
BUCKET_AWS = ''
