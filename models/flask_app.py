# -*- coding: utf-8 -*-
import sys
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from tool.config import WHOOSH_BASE

reload(sys)
sys.setdefaultencoding('utf-8')
app = Flask(__name__)
app.config['WHOOSH_BASE'] = WHOOSH_BASE
# app.config["SQLALCHEMY_ECHO"] = True

CORS(app)


app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://yz:yz@192.168.30.156:3306/tender?charset=utf8mb4'
# app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://sjsecondhand:Zhushijie219211l@rdsptsk6v7h7s4bfo107.mysql.rds.aliyuncs.com:3306/sjsecondhand?charset=utf8mb4'
db = SQLAlchemy(app)