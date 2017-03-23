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
from models.Operation import Operation
from models.Message import Message
from tool.Util import Util
from tool.config import ErrorInfo
from tool.tagconfig import OPERATOR_TAG_CREATED

class OperationManager(Util):
    def __init__(self):
        pass

    # 根据tenderid 获取 操作列表, 是否已报名等
    def getOperationList(self, jsonInfo):
        pass

