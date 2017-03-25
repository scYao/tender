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

    # 审定人获取所有的招标信息列表
    def getTenderListWithPushedTagByBoss(self, jsonInfo):
        pass