# coding=utf8
import sys
import traceback
import urllib2
import poster
import requests
from sqlalchemy import desc

sys.path.append("..")
import os
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from models.flask_app import db
from datetime import datetime

from tool.Util import Util
from tool.config import ErrorInfo

from models.Type1 import Type1

class Type1Manager(Util):
    def __init__(self):
        pass

    # 后台管理, 创建一级类型
    def createType1Background(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, reason) = self.isTokenValid(tokenID)
        if status is not True:
            return (False, reason)

        type1Name = info['typeName']

        type1ID = self.generateID(type1Name)

        type1 = Type1(typeID=type1ID, typeName=type1Name)

        try:
            db.session.add(type1)
            db.session.commit()
            return (Type1, type1ID)
        except Exception as e:
            print e
            traceback.print_stack()
            db.session.rollback()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)

    def __generate(self, t):
        type1 = t
        res = {}
        res.update(Type1.generate(type1=type1))
        return res

    # 获取一级列表
    def getType1List(self):
        allResult = db.session.query(Type1).all()

        typeList = [self.__generate(t=t) for t in allResult]
        return (True, typeList)