# coding=utf8
import sys
import traceback
import urllib2
import poster
import requests

sys.path.append("..")
import os
import re
import jieba
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import urllib
from models.flask_app import db, cache
from datetime import datetime, timedelta
from tool.Util import Util
from tool.config import ErrorInfo
from models.SubscribedKey import SubscribedKey
from models.SearchKey import SearchKey
from models.WeChatPush import WeChatPush
from sqlalchemy import desc, and_
from tool.tagconfig import SEARCH_KEY_TAG_SUBSCRIBE

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
                    createInfo = {}
                    createInfo['subscribedID'] = subscribedID
                    createInfo['userID'] = userID
                    createInfo['keywords'] = keywords
                    createInfo['createTime'] = datetime.now()
                    createInfo['frequency'] = frequency
                    createInfo['pushType'] = pushType
                    createInfo['searchName'] = keywords
                    createInfo['foreignID'] = userID
                    createInfo['searchName'] = keywords
                    createInfo['joinID'] = subscribedID
                    createInfo['tag'] = SEARCH_KEY_TAG_SUBSCRIBE
                    SubscribedKey.create(createInfo=createInfo)
                    SearchKey.createSearchInfo(info=createInfo)
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

    #创建招标公告的订阅者列表
    def createWeChatSubscriberList(self, info):
        # '2017-05-03134235bfa1e77b237022551d784165ce6f643c'
        # title = u'（六合分中心）六合区小北门路（长江路至棠城西路）道路改造工程监理'
        # tenderID = '2017-05-03134235bfa1e77b237022551d784165ce6f643c'
        title = info['title']
        tenderID = info['tenderID']
        title = re.sub(r'[\[\]（）]', ' ', title)
        fenciList = jieba.cut_for_search(title)
        userIDList = []
        try:
            #获取所有符合条件的订阅者
            def generate(fenciItem):
                if fenciItem.strip() != '':
                    allResult = SearchKey.query.whoosh_search(
                        fenciItem).filter(
                        SearchKey.tag == SEARCH_KEY_TAG_SUBSCRIBE
                    ).all()
                    if allResult != []:
                        for result in allResult:
                            if result.foreignID not in userIDList:
                                userIDList.append(result.foreignID)
            [generate(fenciItem) for fenciItem in fenciList]
            #创建推送列表
            createInfo = {}
            createInfo['tenderID'] = tenderID
            createInfo['createTime'] = datetime.now()
            def create(toUserID):
                createInfo['toUserID'] = toUserID
                createInfo['pushedID'] = self.generateID(toUserID)
                #判断是否已经推送
                result = db.session.query(WeChatPush).filter(and_(
                    WeChatPush.tenderID == tenderID,
                    WeChatPush.toUserID == toUserID
                )).first()
                if result is None:
                    WeChatPush.create(createInfo=createInfo)
            [create(toUserID) for toUserID in userIDList]
            db.session.commit()
            return (True, None)
        except Exception, Argument:
            return (False, Argument)