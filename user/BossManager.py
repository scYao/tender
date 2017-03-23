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


class BossManager(Util):

    def __init__(self):
        pass

    # 决定是否投标
    def operatePushedTenderInfo(self, jsonInfo):
        pass

    # 决定是否采用该经办人
    def operateCreatedOperator(self, jsonInfo):
        pass