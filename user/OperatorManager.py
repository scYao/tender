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
from models.Operator import Operator
from models.Message import Message
from models.UserInfo import UserInfo
from models.Token import Token

from ResponsiblePersonManager import ResponsiblePersonManager
from pushedTender.PushedTenderManager import PushedTenderManager


class OperatorManager(Util):
    def __init__(self):
        pass

    def __isTokenValid(self, info):
        tokenID = info['tokenID']
        query = db.session.query(
            Token, UserInfo
        ).outerjoin(
            UserInfo, Token.userID == UserInfo.userID
        ).filter(and_(
                UserInfo.userType == USER_TAG_OPERATOR,
                Token.tokenID == tokenID
            ))
        result = query.first()
        if result is None:
            errorInfo = ErrorInfo['TENDER_01']
            errorInfo['detail'] = result
            return (False, errorInfo)
        token = result.Token
        now = datetime.now()
        # 将token登录时间更新为最近的一次操作时间
        db.session.query(Token).filter(
            Token.tokenID == tokenID
        ).update(
            {Token.createTime: now},
            synchronize_session=False)
        try:
            db.session.commit()
        except Exception as e:
            print e
            errorInfo = ErrorInfo['SPORTS_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)
        days = (now - token.createTime).days
        if days > token.validity:
            errorInfo = ErrorInfo['SPORTS_01']
            errorInfo['detail'] = result
            return (False, errorInfo)
        return (True, result.Token.userID)


    # 经办人推送
    def createPushedTenderByOperator(self, jsonInfo):
        info = json.loads(jsonInfo)
        (status, userID) = self.__isTokenValid(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['tag'] = USER_TAG_RESPONSIBLEPERSON
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.createPushedTender(info)

    # 记录动作, 打保证金等
    def createOperation(self, jsonInfo):
        pass

    # 经办人获取我的推送列表
    def getPushedListByOperator(self, jsonInfo):
        info = json.loads(jsonInfo)
        (status, userID) = self.__isTokenValid(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userID'] = userID
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.getPushedTenderListByUserID(info=info)

    # 经办人特殊, 获取自己参与的, 正在进行中的列表
    # 考虑策略模式
    def getTenderDoingList(self, jsonInfo):
        info = json.loads(jsonInfo)
        (status, userID) = self.__isTokenValid(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        userType = info['userType']
        info['step'] = DOING_STEP
        pushedTenderManager = PushedTenderManager()
        if userType == USER_TAG_OPERATOR:
            return pushedTenderManager.getTenderDoingList(info=info)
        else:
            return pushedTenderManager.getAllTenderDoingList(info=info)

    def getTenderDoingDetail(self, jsonInfo):
        pass

    # 经办人特殊, 获取自己参与的, 已完成的列表
    def getTenderDoneList(self, jsonInfo):
        info = json.loads(jsonInfo)
        (status, userID) = self.__isTokenValid(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        userType = info['userType']
        info['step'] = DONE_STEP
        pushedTenderManager = PushedTenderManager()
        if userType == USER_TAG_OPERATOR:
            return pushedTenderManager.getTenderDoingList(info=info)
        else:
            return pushedTenderManager.getAllTenderDoingList(info=info)

    def getTenderDoneDetail(self, jsonInfo):
        pass

    # 经办人特殊, 获取自己参与的, 历史记录
    def getTenderHistoryList(self, jsonInfo):
        info = json.loads(jsonInfo)
        (status, userID) = self.__isTokenValid(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        userType = info['userType']
        info['step'] = HISTORY_STEP
        pushedTenderManager = PushedTenderManager()
        if userType == USER_TAG_OPERATOR:
            return pushedTenderManager.getTenderDoingList(info=info)
        else:
            return pushedTenderManager.getAllTenderDoingList(info=info)

    def getTenderHistoryDetail(self, jsonInfo):
        pass


    def __generateUserInfo(self, o):
        res = {}
        res['userID'] = o.userID
        res['userName'] = o.userName
        return res

    # 获取员工列表
    def getUserList(self, jsonInfo):
        info = json.loads(jsonInfo)
        (status, userID) = self.__isTokenValid(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        try:
            result = db.session.query(UserInfo).filter(
                UserInfo.userID == userID
            ).first()
            companyID = result.customizedCompanyID
            allResult = db.session.query(UserInfo).filter(
                and_(UserInfo.customizedCompanyID == companyID,
                     UserInfo.userType == USER_TAG_OPERATOR)
            ).all()
            dataList = [self.__generateUserInfo(o=o) for o in allResult]
            count = db.session.query(func.count(UserInfo.userID)).filter(
                UserInfo.customizedCompanyID == companyID
            ).first()
            count = count[0]
            userResult = {}
            userResult['dataList'] = dataList
            userResult['count'] = count
            return (True, userResult)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)


    # 经办人获取所有的招标信息列表
    def getTenderListWithPushedTagByOperator(self, jsonInfo):
        pass
