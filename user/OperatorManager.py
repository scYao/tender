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

from ResponsiblePersonManager import ResponsiblePersonManager
from pushedTender.PushedTenderManager import PushedTenderManager


class OperatorManager(Util):
    def __init__(self):
        pass

    # 经办人推送
    def createPushedTenderByOperator(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['tag'] = USER_TAG_RESPONSIBLEPERSON
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.createPushedTender(info)

    # 记录动作, 打保证金等
    def createOperation(self, jsonInfo):
        pass

    # 获取经办人推送列表
    def getPushedListByOperator(self, jsonInfo):
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.getPushedTenderListByUserID(jsonInfo)

    # 经办人特殊, 获取自己参与的, 正在进行中的列表
    # 考虑策略模式
    def getTenderDoingListByOperator(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['step'] = DOING_STEP
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.getTenderDoingList(info=info)

    def getTenderDoingDetail(self, jsonInfo):
        pass

    # 经办人特殊, 获取自己参与的, 已完成的列表
    def getTenderDoneListByOperator(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['step'] = DONE_STEP
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.getTenderDoingList(info=info)

    def getTenderDoneDetail(self, jsonInfo):
        pass

    # 经办人特殊, 获取自己参与的, 历史记录
    def getTenderHistoryListByOperator(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['step'] = HISTORY_STEP
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.getTenderDoingList(info=info)

    def getTenderHistoryDetail(self, jsonInfo):
        pass