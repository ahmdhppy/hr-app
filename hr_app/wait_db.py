import pymysql
import os
import time


DB_HOST = os.environ['DB_HOST']
DB_USER = os.environ['MYSQL_USER']
DB_PASSWD = os.environ['MYSQL_ROOT_PASSWORD']
DB_NAME = os.environ['MYSQL_DATABASE']

is_ready = False

while not is_ready:
    time.sleep(3)
    db_connection = None
    try:
        db_connection = pymysql.connect(host=DB_HOST,
                                        db=DB_NAME,
                                        port=3306,
                                        user=DB_USER,
                                        password=DB_PASSWD,
                                        charset='utf8mb4',
                                        connect_timeout=3)
        db_connection.ping()
        is_ready = True
    except:
        pass
    finally:
        if db_connection is not None and db_connection.open:
            db_connection.close()
