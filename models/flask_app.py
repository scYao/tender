# -*- coding: utf-8 -*-
import sys
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from tool.config import WHOOSH_BASE
from flask_cache import Cache
from concurrent.futures import ThreadPoolExecutor
from functools import partial, wraps
import tornado.ioloop
import tornado.web
reload(sys)
sys.setdefaultencoding('utf-8')

cache_config = {
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_HOST': '127.0.0.1',
    'CACHE_REDIS_PORT': 6379,
    'CACHE_REDIS_DB': '',
    'CACHE_REDIS_PASSWORD': '',
    'CACHE_REDIS_URL' : 'redis://localhost:6379'
}

app = Flask(__name__)

cache = Cache(app=app, config=cache_config)
# app.config.from_object(cache_config)
# cache.init_app(app)

app.config['WHOOSH_BASE'] = WHOOSH_BASE
# app.config["SQLALCHEMY_ECHO"] = True
app.config['SQLALCHEMY_POOL_SIZE'] = 1

CORS(app)


# app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://zero:Zhushijie219211l@192.168.30.114:3306/tender?charset=utf8mb4'
# app.config['SQLALCHEMY_POOL_SIZE'] = 60
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://tender:Zhushijie219211l@rdsptsk6v7h7s4bfo107.mysql.rds.aliyuncs.com:3306/tender?charset=utf8mb4'
db = SQLAlchemy(app)

EXECUTOR = ThreadPoolExecutor(max_workers=4)
def unblock(f):
    @tornado.web.asynchronous
    @wraps(f)
    def wrapper(*args, **kwargs):
        self = args[0]
        def callback(future):
            self.write(future.result())
            self.finish()
        EXECUTOR.submit(
            partial(f, *args, **kwargs)
        ).add_done_callback(
            lambda future: tornado.ioloop.IOLoop.instance().add_callback(
                partial(callback, future)))