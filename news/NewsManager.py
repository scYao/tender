# coding=utf8
import sys
import traceback
import urllib2
import poster
import requests
from sqlalchemy import desc

sys.path.append("..")
import os
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from datetime import datetime
from sqlalchemy import desc, and_
from models.flask_app import db
from models.News import News

from tool.Util import Util
from tool.config import ErrorInfo
from sqlalchemy import func


class NewsManager(Util):

    def __init__(self):
        pass

    def createNews(self, jsonInfo, imgFileList):
        info = json.loads(jsonInfo)
        title = info['title'].replace('\'', '\\\'').replace('\"', '\\\"')
        content = info['content'].replace('\'', '\\\'').replace('\"', '\\\"')
        createTime = datetime.now()

        newsID = self.generateID(title)