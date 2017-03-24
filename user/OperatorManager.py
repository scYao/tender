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
from tool.tagconfig import OPERATOR_TAG_CREATED

from ResponsiblePersonManager import ResponsiblePersonManager
from pushedTender.PushedTenderManager import PushedTenderManager


class OperatorManager(Util):
    def __init__(self):
        pass

    # 经办人推送
    def createPushedTenderByOperator(self, jsonInfo):
        pass

    # 记录动作, 打保证金等
    def createOperation(self, jsonInfo):
        pass

    # 获取经办人推送列表
    def getOperatorPushedList(self, jsonInfo):
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.getPushedTenderListByUserID(jsonInfo)

    # 经办人特殊, 获取自己参与的, 正在进行中的列表
    # 考虑策略模式
    def getTenderDoingListByOperator(self, jsonInfo):
        pass

    def getTenderDoingDetail(self, jsonInfo):
        pass

    # 经办人特殊, 获取自己参与的, 已完成的列表
    def getTenderDoneListByOperator(self, jsonInfo):
        pass

    def getTenderDoneDetail(self, jsonInfo):
        pass