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
from models.TenderComment import TenderComment
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
        info['userType'] = USER_TAG_BOSS
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['tag'] = USER_TAG_BOSS
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.createPushedTender(info=info)

    # 审定人填写进行中项目的报价信息
    def createQuotedPriceByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_BOSS
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userID'] = userID
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.createQuotedPrice(info=info)

    # 审定人批注正在进行中的项目
    def createTenderComment(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_BOSS
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        tenderID = info['tenderID']
        commentID = self.generateID(userID + tenderID)
        createTime = datetime.now()
        commentInfo = {}
        commentInfo['userID'] = userID
        commentInfo['createTime'] = createTime
        commentInfo['tenderID'] = tenderID
        commentInfo['commentID'] = commentID
        commentInfo['description'] = info['description'].replace('\'', '\\\'').replace('\"', '\\\"')
        try:
            TenderComment.generate(c=commentInfo)
            db.session.commit()
            return (True, None)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    # 决定是否投标
    def operatePushedTenderInfo(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_BOSS
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        pushedTenderManager = PushedTenderManager()
        info['userType'] = USER_TAG_BOSS
        return pushedTenderManager.updatePushedTenderInfo(info=info)

    # 决定是否采用该经办人
    def validateOperator(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_BOSS
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
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
        info['userType'] = USER_TAG_BOSS
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userType'] = USER_TAG_RESPONSIBLEPERSON
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.getPushedTenderListByUserType(info=info)

    # 审定人获取 审核人的推送列表
    def getAuditorPushedListByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_BOSS
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userType'] = USER_TAG_AUDITOR
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.getPushedTenderListByUserType(info=info)

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
        return pushedTenderManager.getPushedTenderListByUserID(info=info)

    # 审定人获取待分配列表
    def getUndistributedTenderListByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_BOSS
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.getUndistributedTenderList(info=info)

    # 审定人获取已分配列表
    def getDistributedTenderListByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_BOSS
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.getDistributedTenderList(info=info)