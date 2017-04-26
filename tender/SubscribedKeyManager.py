# coding=utf8
import sys
import traceback
import urllib2
import poster
import requests

sys.path.append("..")
import os
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from models.flask_app import db, cache
from datetime import datetime, timedelta
from tool.Util import Util
from tool.config import ErrorInfo
from models.SubscribedKey import SubscribedKey

class SubscribedKeyManager(Util):
    def __init__(self):
        pass


    def createSubscribedKey(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)


        userID = info['userID'].replace('\'', '\\\'').replace('\"', '\\\"')
        keywords = info['keywords'].replace('\'', '\\\'').replace('\"', '\\\"').strip()
        frequency = info['frequency']
        pushType = info['pushType']

        subscribedID = self.generateID(keywords)
        now = datetime.now()
        try:
            subscribedKey = SubscribedKey(subscribedID=subscribedID,
                                          userID=userID, keywords=keywords,
                                          createTime=now, frequency=frequency,
                                          pushType=pushType)
            db.session.add(subscribedKey)
            db.session.commit()
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)