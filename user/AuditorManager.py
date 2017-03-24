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

from pushedTender.PushedTenderManager import PushedTenderManager

class AuditorManager(Util):

    def __init__(self):
        pass


    # 负责人推送, 创建推送
    def createPushedTenderByAuditor(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['tag'] = USER_TAG_BOSS
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.createPushedTender(info=info)

    # 推送经办人来的推送
    def pushedTenderByAuditor(self, jsonInfo):
        pass