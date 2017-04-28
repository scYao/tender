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
import urllib
from models.flask_app import db, cache
from datetime import datetime, timedelta
from tool.Util import Util
from tool.config import ErrorInfo
from models.SubscribedKey import SubscribedKey
from sqlalchemy import desc

class SubscribedKeyManager(Util):
    def __init__(self):
        pass



    #创建订阅记录
    def createSubscribedKey(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        searchList = info['searchList']
        frequency = info['frequency']
        pushType = info['mode']
        #删除之前的订阅信息
        try:
            query = db.session.query(SubscribedKey).filter(
                SubscribedKey.userID == userID
            )
            query.delete(synchronize_session=False)
            def create(keywords):
                keywords = keywords.strip()
                if len(keywords) > 0:
                    subscribedID = self.generateID(keywords)
                    now = datetime.now()
                    subscribedKey = SubscribedKey(subscribedID=subscribedID,
                                                  userID=userID, keywords=keywords,
                                                  createTime=now, frequency=frequency,
                                                  pushType=pushType)
                    db.session.add(subscribedKey)
            [create(keywords=keywords.encode('utf-8')) for keywords in searchList]
            db.session.commit()
            return (True, None)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)


    #获取个人订阅信息
    def getSubscribeInfo(self, jsonInfo):
        #测试在小程序中获取微信公众号的信息
        postUrl = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxe56d1e66d153e211&redirect_uri=http://1b6d01ea.ngrok.io/callback/&response_type=code&scope=snsapi_base&state=123#wechat_redirect"
        urlResp = urllib.urlopen(postUrl)
        print urlResp
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        try:
            query = db.session.query(SubscribedKey).filter(
                SubscribedKey.userID == userID
            ).order_by(desc(SubscribedKey.createTime))
            allResult = query.all()
            count = len(allResult)
            callBackData = [SubscribedKey.generate(o=result) for result in allResult]
            callBackInfo = {}
            callBackInfo['dataList'] = callBackData
            callBackInfo['count'] = count
            return (True, callBackInfo)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)