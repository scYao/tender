# coding=utf8
import sys
import json
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
from models.UserInfo import UserInfo
from models.Operator import Operator
from models.PushedTenderInfo import PushedTenderInfo

from pushedTender.PushedTenderManager import PushedTenderManager

class ResponsiblePersonManager(Util):
    def __init__(self):
        pass

    # 经办人推送
    def createPushedTenderByResp(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['tag'] = USER_TAG_AUDITOR
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.createPushedTender(info=info)

    # 负责人从经办人推送列表推送
    def updatePushedTenderByResp(self, jsonInfo):
        # 负责人从经办人列表推送
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        pushedTenderManager = PushedTenderManager()
        info['userType'] = USER_TAG_RESPONSIBLEPERSON
        return pushedTenderManager.updatePushedTenderInfo(info=info)

    @staticmethod
    def isResponsiblePerson(info):
        userID = info['userID']
        try:
            result = db.session.query(UserInfo).filter(
                UserInfo.userID == userID
            ).first()
        except Exception as e:
            print str(e)
            # traceback.print_stack()
            db.session.rollback()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)

        if result is None:
            return (False, ErrorInfo['TENDER_23'])

        tag = UserInfo.userType
        if tag == USER_TAG_RESPONSIBLEPERSON:
            return (True, None)
        return (False, None)

    # 创建经办人, 分配工作
    def createOperator(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        # 验证登录信息
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            return (False, userID)
        # 检查是否是负责人
        info['userID'] = userID
        (status, reason) = ResponsiblePersonManager.isResponsiblePerson(info=info)
        if status is not True:
            return (False, ErrorInfo['TENDER_24'])
        toUserID = info['userID'].replace('\'', '\\\'').replace('\"', '\\\"')
        tenderID = info['tenderID'].replace('\'', '\\\'').replace('\"', '\\\"')
        operatorID = self.generateID(tenderID)
        operator = Operator(
            operatorID=operatorID, userID=toUserID,
            tenderID=tenderID, state=OPERATOR_TAG_CREATED
        )
        try:
            db.session.add(operator)
            db.session.commit()
        except Exception as e:
            print str(e)
            # traceback.print_stack()
            db.session.rollback()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        return (True, None)

    # 经办人被否定, 重新分配经办人
    def updateOperator(self, jsonInfo):
        pass

    #获取经办人列表
    def getOperatorList(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        # 验证登录信息
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            return (False, userID)
        try:
            query = db.session.query(UserInfo).filter(
                UserInfo, UserInfo.userType == USER_TAG_OPERATOR
            )
            allResult = query.all()
            countQuery = db.session.query(func.count(UserInfo.userID)).filter(
                UserInfo.userType == USER_TAG_OPERATOR
            )
            count = countQuery.first()[0]
            dataList = [UserInfo.generate(result) for result in allResult]
            callBackInfo = {}
            callBackInfo['dataList'] = dataList
            callBackInfo['count'] = count
            return (True, callBackInfo)
        except Exception as e:
            print str(e)
            # traceback.print_stack()
            db.session.rollback()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)



    # 负责人 获取某个经办人的推送列表
    def getOperatorPushedListByResp(self, jsonInfo):
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
            try:
                dataList = tenderResult['dataList']
                tenderIDTuple = (o['tenderID'] for o in dataList)

                pushedResult = db.session.query(PushedTenderInfo).filter(and_(
                    PushedTenderInfo.responsiblePersonPushedTime != None,
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

    # 负责人获取我的推送列表
    def getPushedListByResp(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userType'] = USER_TAG_RESPONSIBLEPERSON
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.getPushedTenderListByUserType(info=info)

    # 负责人获取待分配列表
    def getUndistributedTenderListByResp(self, jsonInfo):
        info = json.loads(jsonInfo)
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.getUndistributedTenderList(info=info)