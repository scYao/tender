# coding=utf8
import sys
import traceback
import urllib2
import poster
import requests
from sqlalchemy import desc
from tool.tagconfig import USER_TAG_RESPONSIBLEPERSON
from tool.Util import Util
from tool.config import ErrorInfo

sys.path.append("..")
import os
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from datetime import datetime
from sqlalchemy import func, desc, and_
from models.flask_app import db
from models.PushedTenderInfo import PushedTenderInfo
from models.UserInfo import UserInfo
from message.MessageManager import MessageManager

class PushedTenderManager(Util):

    def __init__(self):
        pass

    def createPushedTender(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        pushedID = self.generateID(userID + info['tenderID'])
        info['pushedID'] = pushedID
        info['userID'] = userID
        info['createTime'] = datetime.now()
        info['responsiblePersonPushedTime'] = None
        info['auditorPushedTime'] = None
        info['state'] = None
        (status, result) = PushedTenderInfo.create(info)
        try:
            companyID = db.session.query(UserInfo).filter(
                UserInfo.userID == userID
            ).first().customizedCompanyID
            query = db.session.query(UserInfo).filter(
                and_(UserInfo.customizedCompanyID == companyID,
                     UserInfo.tag == USER_TAG_RESPONSIBLEPERSON)
            ).first()
            toUserID = query.userID
            #发送消息给负责人
            messageInfo = {}
            messageInfo['fromUserID'] = userID
            messageInfo['pushedID'] = pushedID
            messageInfo['toUserID'] = toUserID
            messageInfo['tag'] = 1
            messageInfo['description'] = ''
            messageManager = MessageManager()
            messageManager.createMessage(messageInfo)
            db.session.commit()
            return (True, pushedID)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    def getPushedTenderListByUserID(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        (status, logInUserID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        if info.has_key('userID'):
            userID = info['userID']
        else:
            userID = logInUserID
        try:
            query = db.session.query(PushedTenderInfo).filter(
                PushedTenderInfo.userID == userID
            )
            countQuery = db.session.query(func.count(PushedTenderInfo.pushedID)).filter(
                PushedTenderInfo.userID == userID
            )
            count = countQuery.first()
            count = count[0]
            allResult = query.offset(startIndex).limit(pageCount).all()
            dataList = [ PushedTenderInfo.generate(result) for result in allResult ]
            callBackInfo = {}
            callBackInfo['dataList'] = dataList
            callBackInfo['count'] = count
            return (True, callBackInfo)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)


