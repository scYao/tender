# coding=utf8
import sys
import json
import traceback

sys.path.append("..")
import os, random, requests
reload(sys)
sys.setdefaultencoding('utf-8')

from datetime import datetime
from sqlalchemy import and_, text, func, desc

from tool.Util import Util
from tool.config import ErrorInfo
from tool.tagconfig import OPERATOR_TAG_CREATED, DOING_STEP, DONE_STEP, HISTORY_STEP
from tool.tagconfig import USER_TAG_OPERATOR, USER_TAG_RESPONSIBLEPERSON, USER_TAG_AUDITOR, USER_TAG_BOSS

from models.flask_app import db
from models.Operator import Operator
from models.Message import Message
from models.UserInfo import UserInfo
from models.Token import Token
from models.PushedTenderInfo import PushedTenderInfo

from pushedTender.PushedTenderManager import PushedTenderManager

class AuditorManager(Util):

    def __init__(self):
        pass

    # 负责人推送, 创建推送
    def createPushedTenderByAuditor(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_AUDITOR
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['tag'] = USER_TAG_BOSS
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.createPushedTender(info=info)

    # 推送经办人来的推送
    def pushedTenderByAuditor(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_AUDITOR
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)


    # 审核人获取我的推送列表
    def getPushedListByAuditor(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_AUDITOR
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userType'] = USER_TAG_AUDITOR
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.getPushedTenderListByUserType(info=info)

    # 审核人 获取某个经办人的推送列表
    def getOperatorPushedListByAuditor(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_AUDITOR
        operatorUserID = info['userID']
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userID'] = operatorUserID
        pushedTenderManager = PushedTenderManager()
        (status, tenderResult) = pushedTenderManager.getPushedTenderListByUserID(info=info)
        if status is True:
            try:
                dataList = tenderResult['dataList']
                tenderIDTuple = (o['tenderID'] for o in dataList)

                pushedResult = db.session.query(PushedTenderInfo).filter(and_(
                    PushedTenderInfo.auditorPushedTime != None,
                    PushedTenderInfo.tenderID.in_(tenderIDTuple)
                )).all()
                pushedTenderIDList = [o.tenderID for o in pushedResult]
                for o in dataList:
                    if o['tenderID'] in pushedTenderIDList:
                        o['pushed'] = True
                    else:
                        o['pushed'] = False
                return (True, tenderResult)
            except Exception as e:
                print str(e)
                # traceback.print_stack()
                db.session.rollback()
                errorInfo = ErrorInfo['TENDER_02']
                errorInfo['detail'] = str(e)
                return (False, errorInfo)

    # 审核人人从经办人推送列表, 或负责人推送列表推送
    def updatePushedTenderByAuditor(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_AUDITOR
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        pushedTenderManager = PushedTenderManager()
        info['userType'] = USER_TAG_AUDITOR
        return pushedTenderManager.updatePushedTenderInfo(info=info)

    # 审核人获取所有的招标信息列表
    def getTenderListWithPushedTagByAuditor(self, jsonInfo):
        pass

    # 审核人 获取负责人推送列表
    def getRespPushedListByAuditor(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_AUDITOR
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userType'] = USER_TAG_RESPONSIBLEPERSON
        pushedTenderManager = PushedTenderManager()
        (status, tenderResult) = pushedTenderManager.getPushedTenderListByUserType(info=info)
        if status is True:
            try:
                dataList = tenderResult['dataList']
                tenderIDTuple = (o['tenderID'] for o in dataList)

                pushedResult = db.session.query(PushedTenderInfo).filter(and_(
                    PushedTenderInfo.auditorPushedTime != None,
                    PushedTenderInfo.tenderID.in_(tenderIDTuple)
                )).all()
                pushedTenderIDList = [o.tenderID for o in pushedResult]
                for o in dataList:
                    if o['tenderID'] in pushedTenderIDList:
                        o['pushed'] = True
                    else:
                        o['pushed'] = False
                return (True, tenderResult)
            except Exception as e:
                print str(e)
                traceback.print_stack()
                db.session.rollback()
                errorInfo = ErrorInfo['TENDER_02']
                errorInfo['detail'] = str(e)
                return (False, errorInfo)
        return (False, tenderResult)