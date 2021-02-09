import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import SECRET_KEY

DB_HOST = os.environ['DB_HOST']
DB_USER = os.environ['MYSQL_USER']
DB_PASSWD = os.environ['MYSQL_ROOT_PASSWORD']
DB_NAME = os.environ['MYSQL_DATABASE']

app = Flask(__name__)
app.config.update(SQLALCHEMY_TRACK_MODIFICATIONS=False)
app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWD}@{DB_HOST}:3306/{DB_NAME}'
db = SQLAlchemy(app)

from . import models 

engine = db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'],{})
db.create_all()
db.session.commit()

from . import route

   
