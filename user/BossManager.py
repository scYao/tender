# coding=utf8
import sys
import json
sys.path.append("..")
import os, random, requests
reload(sys)
sys.setdefaultencoding('utf-8')

from datetime import datetime
from sqlalchemy import and_, text, func, desc

from models.flask_app import db
from models.Operator import Operator
from models.Message import Message
from models.PushedTenderInfo import PushedTenderInfo
from tool.Util import Util
from tool.config import ErrorInfo
from tool.tagconfig import OPERATOR_TAG_CREATED, DOING_STEP, DONE_STEP, HISTORY_STEP
from tool.tagconfig import USER_TAG_OPERATOR, USER_TAG_RESPONSIBLEPERSON, USER_TAG_AUDITOR, USER_TAG_BOSS

from pushedTender.PushedTenderManager import PushedTenderManager


class BossManager(Util):

    def __init__(self):
        pass

    # 审定人创建推送
    def createPushedTenderByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['tag'] = USER_TAG_BOSS
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.createPushedTender(info=info)

    # 决定是否投标
    def operatePushedTenderInfo(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        pushedTenderManager = PushedTenderManager()
        info['userType'] = USER_TAG_BOSS
        return pushedTenderManager.updatePushedTenderInfo(info=info)

    # 决定是否采用该经办人
    def validateOperator(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        pushedTenderManager = PushedTenderManager()
        info['userType'] = USER_TAG_BOSS
        return pushedTenderManager.validateOperator(info=info)

    # 老板确定推送消息后,  获取推送消息列表
    def getCertainPushedList(self, jsonInfo):
        pass

    # 审定人 获取负责人推送列表
    def getRespPushedListByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userType'] = USER_TAG_RESPONSIBLEPERSON
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.getPushedTenderListByUserType(info=info)

    # 审定人获取 审核人的推送列表
    def getAuditorPushedListByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userType'] = USER_TAG_AUDITOR
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.getPushedTenderListByUserType(info=info)

    # 判断是否已经投过该标
    def getApprovedState(self, info):
        dataList = info['dataList']
        try:
            tenderIDTuple = (o['tenderID'] for o in dataList)

            pushedResult = db.session.query(PushedTenderInfo).filter(and_(
                PushedTenderInfo.responsiblePersonPushedTime != None,
                PushedTenderInfo.tenderID.in_(tenderIDTuple)
            )).all()
            pushedTenderIDList = [o.tenderID for o in pushedResult]
            for o in dataList:
                if o['tenderID'] not in pushedTenderIDList:
                    o['state'] = -1
            return (True, info)
        except Exception as e:
            print str(e)
            # traceback.print_stack()
            db.session.rollback()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)

    # 审定人 获取某个经办人的推送列表
    def getOperatorPushedListByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        operatorUserID = info['userID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userID'] = operatorUserID
        pushedTenderManager = PushedTenderManager()
        (status, tenderResult) = pushedTenderManager.getPushedTenderListByUserID(info=info)
        if status is True:
            return self.getApprovedState(info=tenderResult)
        return (False, tenderResult)