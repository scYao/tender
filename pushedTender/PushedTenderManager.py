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
from tool.tagconfig import USER_TAG_OPERATOR, USER_TAG_RESPONSIBLEPERSON, USER_TAG_AUDITOR, USER_TAG_BOSS

from models.flask_app import db
from models.PushedTenderInfo import PushedTenderInfo
from models.UserInfo import UserInfo
from models.Tender import Tender

from message.MessageManager import MessageManager

class PushedTenderManager(Util):

    def __init__(self):
        pass

    def createMessage(self, info):
        userID = info['userID']
        pushedID = info['pushedID']
        tag = info['tag']
        userResult = db.session.query(UserInfo).filter(
            UserInfo.userID == userID
        ).first()
        if userResult is None:
            return (False, ErrorInfo['TENDER_23'])
        companyID = userResult.customizedCompanyID
        query = db.session.query(UserInfo).filter(
            and_(UserInfo.customizedCompanyID == companyID,
                 UserInfo.userType == tag)
        )
        responResult = query.first()
        if responResult:
            toUserID = responResult.userID
            # 发送消息给负责人
            messageInfo = {}
            messageInfo['fromUserID'] = userID
            messageInfo['pushedID'] = pushedID
            messageInfo['toUserID'] = toUserID
            messageInfo['tag'] = 1
            messageInfo['description'] = ''
            messageInfo['foreignID'] = info['tenderID']
            messageManager = MessageManager()
            return messageManager.createMessage(messageInfo)
        return (False, None)

    # 经办人 负责人 审核人 创建推送
    def createPushedTender(self, info):
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        pushedID = self.generateID(userID + info['tenderID'])
        info['pushedID'] = pushedID
        info['userID'] = userID
        info['createTime'] = None
        info['responsiblePersonPushedTime'] = None
        info['auditorPushedTime'] = None
        info['state'] = 0
        info['step'] = 0
        tag = info['tag']
        if tag == USER_TAG_OPERATOR:
            info['createTime'] = datetime.now()
        if tag == USER_TAG_AUDITOR:
            info['auditorPushedTime'] = datetime.now()
        if tag == USER_TAG_RESPONSIBLEPERSON:
            info['responsiblePersonPushedTime'] = datetime.now()
        try:
            #判断是否已经创建过推送消息
            result = db.session.query(PushedTenderInfo).filter(
                PushedTenderInfo.tenderID == info['tenderID']
            ).first()
            if result:
                return (False, ErrorInfo['TENDER_25'])
            (status, result) = PushedTenderInfo.create(info)
            #推送消息
            (status, result) = self.createMessage(info=info)
            db.session.commit()
            return (True, pushedID)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    def __generateBrief(self, result):
        res = {}
        res.update(PushedTenderInfo.generateBrief(c=result.PushedTenderInfo))
        res.update(Tender.generateBrief(tender=result.Tender))
        return res

    # 负责人或审核人推送, 从上一级或上两级中继续推送
    def updatePushedTenderInfo(self, info):
        pushedID = info['pushID']
        userType = info['userType']
        try:
            query = db.session.query(PushedTenderInfo).filter(
                PushedTenderInfo.pushedID == pushedID
            )
            result = query.first()
            if not result:
                return (False, ErrorInfo['TENDER_25'])
            updateInfo = {}
            if userType == USER_TAG_AUDITOR:
                updateInfo = {
                    PushedTenderInfo.auditorPushedTime : datetime.now()
                }
            elif userType == USER_TAG_RESPONSIBLEPERSON:
                updateInfo = {
                    PushedTenderInfo.responsiblePersonPushedTime : datetime.now()
                }
            query.update(
                updateInfo, synchronize_session=False
            )
            db.session.commit()
            return (True, None)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)


    # 经办人 获取我的推送列表, 获取经办人推送列表
    def getPushedTenderListByUserID(self, info):
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        userID = info['userID']

        try:
            query = db.session.query(
                PushedTenderInfo, Tender
            ).outerjoin(
                Tender, PushedTenderInfo.tenderID == Tender.tenderID
            ).filter(
                PushedTenderInfo.userID == userID
            )
            countQuery = db.session.query(func.count(PushedTenderInfo.pushedID)).filter(
                PushedTenderInfo.userID == userID
            )
            count = countQuery.first()
            count = count[0]
            allResult = query.offset(startIndex).limit(pageCount).all()
            dataList = [self.__generateBrief(result=result) for result in allResult]
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

    # 获取正在进行中的列表
    def getTenderDoingList(self, info):
        tokenID = info['tokenID']
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        step = info['step']
        (status, logInUserID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        if info.has_key('userID'):
            userID = info['userID']
        else:
            userID = logInUserID
        try:
            query = db.session.query(
                PushedTenderInfo, Tender
            ).outerjoin(
                Tender, PushedTenderInfo.tenderID == Tender.tenderID
            ).filter(
                and_(PushedTenderInfo.userID == userID,
                     PushedTenderInfo.step == step)
            )
            countQuery = db.session.query(func.count(PushedTenderInfo.pushedID)).filter(
                and_(PushedTenderInfo.userID == userID,
                     PushedTenderInfo.step == step)
            )
            count = countQuery.first()
            count = count[0]
            allResult = query.offset(startIndex).limit(pageCount).all()
            dataList = [self.__generateBrief(result=result) for result in allResult]
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

    # 审核人 负责人 获取我的推送
    def getPushedTenderListByUserType(self, info):
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        userType = info['userType']

        try:
            query = db.session.query(
                PushedTenderInfo, Tender
            ).outerjoin(
                Tender, PushedTenderInfo.tenderID == Tender.tenderID
            )
            countQuery = db.session.query(
                func.count(PushedTenderInfo.pushedID)
            )
            # 负责人查询
            if userType == USER_TAG_RESPONSIBLEPERSON:
                query = query.filter(
                    PushedTenderInfo.responsiblePersonPushedTime != None
                ).order_by(desc(
                    PushedTenderInfo.responsiblePersonPushedTime
                ))
                countQuery = countQuery.filter(
                    PushedTenderInfo.responsiblePersonPushedTime != None
                )
            #     审核人查询
            elif userType == USER_TAG_AUDITOR:
                query = query.filter(
                    PushedTenderInfo.auditorPushedTime != None
                ).order_by(desc(
                    PushedTenderInfo.auditorPushedTime
                ))
                countQuery = countQuery.filter(
                    PushedTenderInfo.auditorPushedTime != None
                )
            allResult = query.offset(startIndex).limit(pageCount).all()
            count = countQuery.first()
            dataList = [self.__generateBrief(result=result) for result in allResult]
            callBackInfo = {}
            callBackInfo['dataList'] = dataList
            callBackInfo['count'] = count[0]
            return (True, callBackInfo)
        except Exception as e:

            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)