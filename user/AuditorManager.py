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


class AuditorManager(Util):

    def __init__(self):
        pass


    # 负责人推送, 创建推送
    def createPushedTenderByAuditor(self, jsonInfo):
        pass

    # 推送经办人来的推送
    def pushedTenderByAuditor(self, jsonInfo):
        pass